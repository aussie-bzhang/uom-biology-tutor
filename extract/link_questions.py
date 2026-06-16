#!/usr/bin/env python3
"""
link_questions.py -- wrap the converted review-question markdown (md-questions/)
into publish:false question notes linked to the matching lecture's concepts.
OFFLINE: no GLM, no network.

    python extract/link_questions.py vault

- Chapter/Lecture number is parsed from the filename:
  Chapter10 / Chapter_6 / Chapter2 / Lecture_19 / Biology_Chapter9 / 第5章.
- A file for chapter N links to EVERY concept whose `lecture: N`
  (concept = first such concept, also_tests = the rest) so verify's C2 resolves.
- Files with no chapter number (whole-course / comprehensive banks) become
  course-level question notes with no concept link.
- Chapters whose concepts don't exist yet (Topics 2-4 not generated) are skipped;
  just re-run this after those topics are built.
- Everything is publish:false; the AI source is kept locally (source_ai) and is
  never surfaced on the public site.
"""
import sys, re, json, pathlib
import yaml


def split_fm(text):
    parts = text.split("---", 2)
    if len(parts) < 3:
        return None, None
    return parts[1], parts[2]


def load_concepts(vault):
    out = {}
    for f in (vault / "concepts").glob("*.md"):
        fm, _ = split_fm(f.read_text(encoding="utf-8"))
        if fm is None:
            continue
        d = yaml.safe_load(fm) or {}
        if d.get("type") == "concept" and "id" in d:
            out[d["id"]] = d
    return out


def chapter_of(name):
    m = re.search(r"(?:chapter|lecture)[_ ]?(\d+)", name, re.I)
    if m:
        return int(m.group(1))
    m = re.search(r"第\s*(\d+)\s*章", name)
    return int(m.group(1)) if m else None


def ai_of(name):
    for a in ("claude", "gpt", "kimi"):
        if name.lower().startswith(a + "-"):
            return a
    return "unknown"


def slug(name):
    s = re.sub(r"\.md$", "", name)
    s = re.sub(r"^(claude|gpt|kimi)-", "", s, flags=re.I)
    s = re.sub(r"[^A-Za-z0-9]+", "-", s).strip("-").lower()
    return (s[:40] or "bank")


def q_inline(ids):
    return "[" + ", ".join(json.dumps(f"[[{i}]]") for i in ids) + "]"


def main():
    vault = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "vault")
    mq = vault.parent / "md-questions"
    if not mq.exists():
        print(f"! not found: {mq}"); sys.exit(0)
    qdir = vault / "questions"; qdir.mkdir(exist_ok=True)

    concepts = load_concepts(vault)
    by_lec = {}
    for cid, d in concepts.items():
        by_lec.setdefault(d.get("lecture"), []).append(cid)

    created = course = 0
    skipped = []
    for f in sorted(mq.glob("*.md")):
        name, ai = f.name, ai_of(f.name)
        body = f.read_text(encoding="utf-8")
        ch = chapter_of(name)

        if ch is None:                                   # whole-course bank
            course += 1                                  # defer: spans all topics
            continue

        ids = sorted(by_lec.get(ch, []))
        if not ids:                                      # concepts not built yet
            skipped.append(ch)
            continue
        primary, also = ids[0], ids[1:]
        topic = concepts[primary].get("topic", "")
        qid = f"q-ch{ch}-{ai}"
        note = (f"---\nid: {qid}\ntype: question\ntopic: {topic}\nlecture: {ch}\n"
                f'concept: "[[{primary}]]"\n'
                f"also_tests: {q_inline(also)}\n"
                f"publish: false\nsource_ai: {ai}\n---\n"
                f"<!-- review bank: {name} | publish:false, not surfaced -->\n\n{body}")
        (qdir / f"{qid}.md").write_text(note, encoding="utf-8")
        created += 1

    print(f"link_questions: {created} chapter question notes; deferred {course} whole-course "
          f"banks; skipped {len(skipped)} chapters (no concepts yet)")
    if skipped:
        print(f"  skipped chapters (build their topics, then re-run): "
              f"{sorted(set(skipped))}")
    print("  next: python verify/verify.py vault")


if __name__ == "__main__":
    main()
