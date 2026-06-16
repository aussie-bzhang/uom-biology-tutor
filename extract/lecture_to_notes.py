#!/usr/bin/env python3
"""
One lecture -> a SET of gold-pattern concept notes, via MarkItDown + GLM-4-flash.
Prompt is EMBEDDED (single source of truth). Idempotent per lecture: re-running a
lecture first removes that lecture's previously generated notes (by the `lecture`
tag), so re-runs overwrite cleanly instead of piling up.

  pip install 'markitdown[all]'
  set ZHIPUAI_API_KEY=...        (VPN/proxy OFF for Zhipu)
  python extract/lecture_to_notes.py "md/LECTURE 2 - What is Life.md" --topic 1 --md
  python verify/verify.py vault
"""
import os, sys, re, json, time, argparse, datetime, pathlib

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

BUILD = "embedded-prompt-4"
HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
VAULT = ROOT / "vault"

SYSTEM = r'''You convert ONE university biology lecture (Markdown produced by MarkItDown from
the slides) into a SET of Obsidian concept notes for a wiki. Output ONE JSON
object and nothing else (no prose, no code fences).

ABSOLUTE RULES
1. REWRITE in your own words. Never copy slide sentences, bullets, or layout.
   Facts, numbers and equations may be stated; specific slide wording may not.
2. EXPLAIN, do not announce. "overview" must TEACH the concept directly in 3-5
   substantive sentences. NEVER begin with "This concept introduces / covers /
   discusses / explains ..." -- just explain the thing itself.
3. Capture the KEY facts and the relationships that matter, not generic filler.
   If a slide makes a defining contrast or states a "most important" point, it
   MUST appear (e.g. for the domains of life: Archaea are more closely related
   to Eukarya than to Bacteria).
4. "learning_objectives" are FULL SENTENCES you phrase yourself -- what a student
   should be able to DO. They are NOT objective ids.
5. "covers_objectives" are the objective IDS only. Harvest the lecture's
   "Learning Outcomes" slide into objectives[], id'd LO<lecture-number>.<n>,
   taking the lecture number from the deck (e.g. "Lecture 2" -> LO2.1, LO2.2 ...).
6. prerequisites: add a concept ONLY if a student genuinely must understand it
   first. If the concept stands on its own, use []. Prefer real conceptual
   dependence over loose topical association.
7. ids must be SHORT (1-3 words, kebab-case). No filler suffixes like
   -classification, -characteristics, -history, -evolution.

OUTPUT SCHEMA (one JSON object):
{
  "objectives": [ {"id": "LO<lec>.<n>", "text": "<the lecture's stated outcome, reworded>"} ],
  "concepts": [
    {
      "id": "kebab-case-id",
      "title": "Human Readable Title",
      "prerequisites": ["other-id"],
      "learning_objectives": ["full sentence", "full sentence"],
      "covers_objectives": ["LO<lec>.<n>"],
      "difficulty": 2,
      "tags": ["..."],
      "overview": "3-5 explaining sentences; name related concepts where relevant.",
      "key_points": ["a specific fact or relationship", "another"]
    }
  ]
}

GRANULARITY: one concept per real idea; a concept usually spans several slides.
Aim for ~4-8 concepts per lecture, not one-note-per-slide.

WORKED EXAMPLE -- produce notes at THIS depth and shape:
{
  "objectives": [{"id":"LO2.4","text":"Interpret a phylogenetic classification of life"}],
  "concepts": [{
    "id":"domains-of-life","title":"The Three Domains of Life",
    "prerequisites":["evolution-of-life"],
    "learning_objectives":["Distinguish Bacteria, Archaea and Eukarya by cell type","Explain why Archaea are evolutionarily closer to Eukarya than to Bacteria"],
    "covers_objectives":["LO2.4"],"difficulty":3,"tags":["taxonomy","evolution"],
    "overview":"All cellular life is sorted into three domains. Bacteria and Archaea are both prokaryotic, lacking a nucleus and membrane-bound organelles, whereas Eukarya have both. Although Archaea superficially resemble bacteria, their molecular machinery places them closer to Eukarya than to Bacteria -- the central insight that the three-domain system was built to capture. Archaea are also notable for thriving in extreme environments such as hot springs and hypersaline water.",
    "key_points":["Two of the three domains (Bacteria, Archaea) are prokaryotic; only Eukarya are eukaryotic","Archaea are more closely related to Eukarya than to Bacteria","Archaea frequently occupy extreme environments"]
  }]
}'''


def log(msg):
    print(msg, file=sys.stderr, flush=True)


def to_markdown(src):
    p = pathlib.Path(src)
    if p.suffix.lower() == ".md":
        return p.read_text(encoding="utf-8")
    from markitdown import MarkItDown
    return MarkItDown().convert(str(p)).text_content


def existing_ids():
    return sorted(f.stem for f in (VAULT / "concepts").glob("*.md"))


def clear_lecture(lecture):
    """Idempotency: remove notes previously generated from THIS lecture."""
    if lecture <= 0:
        return 0
    removed = 0
    for f in (VAULT / "concepts").glob("*.md"):
        head = f.read_text(encoding="utf-8")[:500]
        m = re.search(r"(?m)^lecture:\s*(\d+)\s*$", head)
        if m and int(m.group(1)) == lecture:
            f.unlink()
            removed += 1
    return removed


def call_glm(system, user):
    from zhipuai import ZhipuAI
    client = ZhipuAI(api_key=os.environ["ZHIPUAI_API_KEY"])
    r = client.chat.completions.create(
        model="glm-4-flash", temperature=0.1,
        messages=[{"role": "system", "content": system},
                  {"role": "user", "content": user}])
    return r.choices[0].message.content


def parse_json(text):
    t = re.sub(r"^```(?:json)?|```$", "", text.strip(), flags=re.M).strip()
    s, e = t.find("{"), t.rfind("}")
    if s != -1 and e != -1:
        t = t[s:e + 1]
    return json.loads(t)


def _yaml_inline(items):
    return "[" + ", ".join(json.dumps(x, ensure_ascii=False) for x in items) + "]"


def resolve_los(c, objmap):
    """LOs must be full sentences; swap any bare objective id for its text."""
    out = []
    for x in c.get("learning_objectives", []):
        xs = str(x).strip()
        if re.fullmatch(r"LO\d+\.\d+", xs):
            if xs in objmap:
                out.append(objmap[xs])
        else:
            out.append(x)
    if not out:
        for cid in c.get("covers_objectives", []):
            if cid in objmap:
                out.append(objmap[cid])
    return out


def build_note(c, topic, lecture, objmap):
    # json.dumps quotes every free-text field -> always valid YAML (colons safe)
    prereqs = _yaml_inline([f"[[{p}]]" for p in c.get("prerequisites", [])])
    los = "\n".join(f"  - {json.dumps(x, ensure_ascii=False)}"
                    for x in resolve_los(c, objmap)) or "  []"
    kp = "\n".join(f"- {x}" for x in c.get("key_points", [])) or "-"
    title = json.dumps(c.get("title", c["id"]), ensure_ascii=False)
    cid = json.dumps(c["id"], ensure_ascii=False)
    return f"""---
id: {cid}
type: concept
topic: {topic}
lecture: {lecture}
title: {title}
prerequisites: {prereqs}
learning_objectives:
{los}
covers_objectives: {_yaml_inline(c.get('covers_objectives', []))}
difficulty: {int(c.get('difficulty', 2))}
tags: {_yaml_inline(c.get('tags', []))}
source_provenance: rewritten
source_edition: "UoM BIOL10002 Topic {topic}"
last_reviewed: {datetime.date.today().isoformat()}
status: draft
---
# {c.get('title', c['id'])}

## Overview
{c.get('overview', '').strip()}

## Key points
{kp}

## Linked questions
-
"""


def merge_objectives(topic, objs):
    p = ROOT / "raw" / f"topic-{topic}-objectives.json"
    byid = {}
    if p.exists():
        for o in json.loads(p.read_text(encoding="utf-8")):
            if isinstance(o, dict) and "id" in o:
                byid[o["id"]] = o
    for o in objs:
        if isinstance(o, dict) and "id" in o:
            byid[o["id"]] = o
    p.write_text(json.dumps([byid[k] for k in sorted(byid)], ensure_ascii=False, indent=2),
                 encoding="utf-8")
    return len(byid)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("lecture")
    ap.add_argument("--topic", type=int, required=True)
    ap.add_argument("--md", action="store_true")
    a = ap.parse_args()

    name = pathlib.Path(a.lecture).name
    m = re.search(r"lecture\s*(\d+)", name, re.I)
    lecture = int(m.group(1)) if m else 0
    log(f"lecture_to_notes [{BUILD}]")
    log(f"[{name}]  (topic {a.topic}, lecture {lecture})")

    log("  - reading markdown ..." if a.md else "  - converting to markdown ...")
    try:
        md = to_markdown(a.lecture)
    except ImportError:
        log("  ! MarkItDown not installed: pip install 'markitdown[all]'"); sys.exit(0)
    except FileNotFoundError:
        log(f"  ! file not found: {a.lecture}"); sys.exit(0)
    log(f"    {len(md)} chars of source text")

    if not os.environ.get("ZHIPUAI_API_KEY"):
        log("  ! ZHIPUAI_API_KEY not set; no notes generated."); sys.exit(0)

    user = (f"topic: {a.topic}\n"
            f"existing_concept_ids: {existing_ids()}\n"
            f"--- LECTURE MARKDOWN TO REWRITE (do not copy) ---\n{md}\n")

    log("  - calling GLM-4-flash (10-60s; VPN/proxy must be OFF) ...")
    t0 = time.time()
    try:
        raw = call_glm(SYSTEM, user)
    except Exception as e:
        log(f"  ! GLM failed after {time.time()-t0:.0f}s: {type(e).__name__}")
        log("    if it timed out, turn OFF VPN/proxy and retry."); sys.exit(0)
    log(f"    GLM responded in {time.time()-t0:.0f}s ({len(raw)} chars)")

    log("  - parsing response ...")
    try:
        data = parse_json(raw)
    except Exception as e:
        dump = ROOT / "raw" / "_last_glm_output.txt"
        dump.write_text(raw, encoding="utf-8")
        log(f"  ! could not parse GLM JSON ({e}); raw saved to {dump}"); sys.exit(0)

    objs = data.get("objectives", [])
    objmap = {o["id"]: o["text"] for o in objs if isinstance(o, dict) and "id" in o}

    n_removed = clear_lecture(lecture)
    if n_removed:
        log(f"  - cleared {n_removed} old notes from lecture {lecture}")

    cdir = VAULT / "concepts"
    written = []
    for c in data.get("concepts", []):
        if "id" not in c:
            continue
        (cdir / f"{c['id']}.md").write_text(
            build_note(c, a.topic, lecture, objmap), encoding="utf-8")
        written.append(c["id"])
    total = merge_objectives(a.topic, objs)

    log(f"  [ok] wrote {len(written)} concept notes: {', '.join(written)}")
    log(f"  [ok] objectives now {total} total -> raw/topic-{a.topic}-objectives.json")


if __name__ == "__main__":
    main()
