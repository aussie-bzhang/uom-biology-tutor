#!/usr/bin/env python3
"""
Post-batch STITCH: make a freshly GLM-generated vault 4C-clean. Run after a topic
batch, before verify:

    python verify/stitch.py vault

Three deterministic passes (no GLM):
  1. Normalize YAML frontmatter on concept notes: quote `title:` and every
     learning_objective item, so titles like "Amino Acids: Building Blocks of
     Proteins" no longer break the YAML parser.
  2. Prune dangling prerequisites: drop [[id]] links to concepts that do not exist
     (GLM invents prereq ids per-lecture that don't align across the vault).
  3. Rebuild topic notes from the concepts actually present: concepts list +
     syllabus_objectives (ids from concepts' covers_objectives, text from
     raw/topic-<N>-objectives.json where available). Guarantees C4 is self-consistent.

Then it runs the 4C check and prints the report.
"""
import sys, re, json, pathlib
from collections import defaultdict

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))


def quote_scalar(s):
    s = s.strip()
    if len(s) >= 2 and s[0] == '"' and s[-1] == '"':
        return s                       # already quoted
    return json.dumps(s, ensure_ascii=False)


def split_fm(text):
    parts = text.split("---", 2)
    if len(parts) < 3:
        return None, None
    return parts[1].strip("\n"), parts[2]   # frontmatter (no edge blanks), body


def normalize_and_prune(path, valid_ids):
    text = path.read_text(encoding="utf-8")
    fm, body = split_fm(text)
    if fm is None:
        return
    out = []
    for line in fm.splitlines():
        if line.startswith("title:"):
            out.append("title: " + quote_scalar(line[len("title:"):]))
        elif re.match(r"^\s*-\s+\S", line):                 # block-list item (learning_objectives)
            indent = line[:len(line) - len(line.lstrip())]
            out.append(f"{indent}- " + quote_scalar(line.lstrip()[2:]))
        elif line.startswith("prerequisites:"):
            ids = re.findall(r"\[\[([^\]]+)\]\]", line)
            kept = [i for i in ids if i in valid_ids]
            out.append("prerequisites: [" + ", ".join(json.dumps(f"[[{i}]]") for i in kept) + "]")
        else:
            out.append(line)
    path.write_text("---\n" + "\n".join(out) + "\n---" + body, encoding="utf-8")


def rebuild_topic_notes(vault):
    import yaml
    cdir, tdir = vault / "concepts", vault / "topics"
    concepts = {}
    for f in cdir.glob("*.md"):
        fm, _ = split_fm(f.read_text(encoding="utf-8"))
        d = yaml.safe_load(fm) or {}
        if "id" in d:
            concepts[d["id"]] = d

    by_topic = defaultdict(list)
    for cid, d in concepts.items():
        by_topic[d.get("topic", 0)].append(cid)

    tdir.mkdir(exist_ok=True)
    for tf in tdir.glob("*.md"):
        tf.unlink()                                          # rebuild fresh

    for topic, ids in sorted(by_topic.items()):
        objids = sorted({o for cid in ids for o in (concepts[cid].get("covers_objectives") or [])})
        objmap = {}
        oj = vault.parent / "raw" / f"topic-{topic}-objectives.json"
        if oj.exists():
            for o in json.loads(oj.read_text(encoding="utf-8")):
                if isinstance(o, dict) and "id" in o:
                    objmap[o["id"]] = o.get("text", o["id"])
        clist = "\n".join(f'  - "[[{c}]]"' for c in sorted(ids))
        syll = "\n".join(f'  - id: {oid}\n    text: {quote_scalar(objmap.get(oid, oid))}'
                         for oid in objids)
        (tdir / f"topic-{topic}.md").write_text(
            f"""---
id: topic-{topic}
type: topic
topic: {topic}
title: "Topic {topic}"
concepts:
{clist}
syllabus_objectives:
{syll}
---
# Topic {topic}

Auto-assembled from {len(ids)} concept notes.
""", encoding="utf-8")
    return len(concepts), len(by_topic)



def _prereq_ids(line):
    return re.findall(r"\[\[([^\]]+)\]\]", line)


def rewrite_prereqs(path, kept):
    text = path.read_text(encoding="utf-8")
    fm, body = split_fm(text)
    if fm is None:
        return
    out = []
    for line in fm.splitlines():
        if line.startswith("prerequisites:"):
            out.append("prerequisites: [" + ", ".join(json.dumps(f"[[{i}]]") for i in kept) + "]")
        else:
            out.append(line)
    path.write_text("---\n" + "\n".join(out) + "\n---" + body, encoding="utf-8")


def break_cycles(vault):
    """Greedily build an acyclic prereq graph; drop edges that would close a cycle."""
    import yaml
    cdir = vault / "concepts"
    prereqs = {}
    for f in cdir.glob("*.md"):
        fm, _ = split_fm(f.read_text(encoding="utf-8"))
        d = yaml.safe_load(fm) or {}
        cid = d.get("id")
        if cid:
            prereqs[cid] = [i for p in (d.get("prerequisites") or [])
                            for i in _prereq_ids(f"[[{p}]]" if "[[" not in str(p) else str(p))]
    kept = {c: [] for c in prereqs}

    def reaches(start, target):
        seen, stack = set(), [start]
        while stack:
            n = stack.pop()
            if n == target:
                return True
            for m in kept.get(n, []):
                if m not in seen:
                    seen.add(m); stack.append(m)
        return False

    dropped = 0
    for cid in sorted(prereqs):
        for p in sorted(prereqs[cid]):
            if p == cid or reaches(p, cid):     # self-loop or would close a cycle
                dropped += 1
            else:
                kept[cid].append(p)
    for f in cdir.glob("*.md"):
        fm, _ = split_fm(f.read_text(encoding="utf-8"))
        d = yaml.safe_load(fm) or {}
        if d.get("id") in kept:
            rewrite_prereqs(f, kept[d["id"]])
    return dropped


def main():
    vault = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "vault")
    cdir = vault / "concepts"
    valid_ids = {f.stem for f in cdir.glob("*.md")}

    print(f"stitch: {len(valid_ids)} concept notes")
    print("  pass 1/2: normalize YAML quoting + prune dangling prerequisites ...")
    for f in cdir.glob("*.md"):
        normalize_and_prune(f, valid_ids)
    print("  pass 2b: break prerequisite cycles ...")
    dropped = break_cycles(vault)
    print(f"  dropped {dropped} cycle-closing prerequisite edge(s)")
    print("  pass 3: rebuild topic notes ...")
    n, t = rebuild_topic_notes(vault)
    print(f"  rebuilt {t} topic note(s) from {n} concepts")

    print("  running 4C ...")
    import verify
    r = verify.run(str(vault))
    for key, label in [("C1_correctness", "C1"), ("C2_consistency", "C2"),
                       ("C4_completeness", "C4")]:
        msgs = r[key]
        print(f"  [{'PASS' if not msgs else 'FAIL'}] {label}")
        for m in msgs[:8]:
            print(f"      - {m}")
        if len(msgs) > 8:
            print(f"      ... (+{len(msgs)-8} more)")
    print(f"  [{'ok' if not r['C3_currency'] else 'WARN'}] C3")


if __name__ == "__main__":
    main()
