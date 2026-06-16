# BioChem-Tutor — implementation brief (hand to the Claude Code session)

This folder is the **gold pattern** for Topic 1. Replicate its quality across all
topics, then publish Layer 1 and deploy Layer 2.

## What is here
```
vault/_templates/      concept.md / topic.md / question.md  (ontology schema)
vault/topics/          one overview per Topic (carries official syllabus_objectives)
vault/concepts/        10 gold concept notes for Topic 1 (rewrites, prereq DAG)
vault/questions/       publish:false question notes linked back to concepts
verify/verify.py       4C gate (pure-Python; optional pyswip+wiki.pl)
verify/wiki.pl         PRIVATE Prolog rules (gitignored)
extract/GLM_EXTRACT_PROMPT.md   the rewrite contract
extract/extract_concept.py      GLM-4-flash extractor (zhipuai, temp 0.1, env key)
.gitignore             keeps raw PPT/PDF + *.pl out of the public repo
```

## Layer 1 — public wiki
1. Convert each lecture with MarkItDown (Microsoft): PDF/PPTX -> markdown.
   The copyright source PDFs stay under `raw/` (gitignored) and are never committed.
       markitdown "raw/LECTURE 3 - Water ....pdf" -o raw/lecture3.md
2. Per lecture, run `extract/lecture_to_notes.py "raw/LECTURE N ....pdf" --topic T`
   (it can call MarkItDown itself, or take `--md raw/lectureN.md`). GLM-4-flash
   rewrites the lecture into several concept notes (own words, prereq wikilinks to
   existing ids only, learning_objectives + covers_objectives, difficulty 1-5,
   source_provenance: rewritten) and harvests the Learning Outcomes slide to
   raw/topic-T-objectives.json. (`extract/extract_concept.py` remains for single-chunk tests.)
3. Schema-validate, then run `python verify/verify.py vault`. **Do not publish
   anything that fails C1/C2/C4.** Fix dangling links / cycles / coverage gaps.
4. Build with **Quartz v4** and deploy to GitHub Pages. The public site contains
   ONLY the wiki (and, via `publish:false`, NOT the question notes). `.gitignore`
   keeps `raw/` and `*.pl` out of the repo.

## Layer 2 — private HF agent
- KB = read the same vault (.md frontmatter prereqs + body + linked questions).
- Mastery tracking (start with a simple heuristic; DKT/SAKT later).
- Prereq gating: never serve a concept whose prerequisites are unmet — reuse the
  graph logic in verify.py (or wiki.pl via pyswip with the pure-Python fallback).
- Gradio app -> PRIVATE HF Space `repo_id="bailing1961/biochem-tutor", private=True`.
  Pin gradio in requirements.txt; `hf auth login`; key only in Secrets; must run
  with no key (deterministic/keyword path first). (Project 2 deployment lessons.)

## Milestones (thin slices, each shippable)
1. (done) schema + templates + 1 gold topic + 4C gate
2. batch-extract remaining topics via GLM, 4C-green
3. Quartz publish public wiki
4. agent: vault-as-KB + mastery + prereq-gated questions
5. deploy private HF Space

## Subject structure (4 Topics across 35 lectures)
Group concept notes by `topic` (1-4); keep an optional `lecture:` field for provenance.
Review questions are per-lecture ("Chapter N" == Lecture N in the three AI banks).

- Topic 1  The Chemistry of Life      = Lectures 2-9
- Topic 2  Energy / Metabolism        = Lectures 10-18
- Topic 3  Genetics                   = Lectures 19-27
- Topic 4  Multicellularity / Physiology / Development = Lectures 28-36
(Confirm exact boundaries against the subject guide if needed.)

## C4 completeness basis — auto-harvested, no manual LO input
Every lecture deck has a "Learning Outcomes" slide. The extractor harvests those
verbatim-in-meaning (rewritten) into each topic note's `syllabus_objectives`, and
concept notes set `covers_objectives` to the matching ids. verify.py then checks
that every harvested objective is covered by >=1 concept. No hand-supplied LO list
is required.
