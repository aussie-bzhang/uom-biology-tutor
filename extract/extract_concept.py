#!/usr/bin/env python3
"""
Batch concept extractor: slide-text chunk -> gold-pattern concept note via
GLM-4-flash. Mirrors the AutoKB-Bench stack (zhipuai, glm-4-flash, temp 0.1).

  export ZHIPUAI_API_KEY=...                       # key only in env / HF Secrets
  python extract_concept.py chunk.txt --topic 1 --out vault/concepts/<id>.md

Use --out (writes UTF-8 directly) rather than the shell `>` redirect: on Windows
PowerShell `>` re-encodes to UTF-16 and corrupts the file. Without a key (or if
the API is down) it writes a template stub so the pipeline never blocks.
"""
import os, sys, json, argparse, pathlib

# Windows consoles/pipes default to the locale codec (GBK on zh-CN), which both
# breaks reading these UTF-8 files and mangles non-ASCII output. Force UTF-8.
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


def read_text_utf8(p):
    return pathlib.Path(p).read_text(encoding="utf-8")


def read_chunk(p):
    """Slide text may be saved as UTF-8 (modern Notepad) or GBK (legacy ANSI)."""
    data = pathlib.Path(p).read_bytes()
    for enc in ("utf-8", "gbk"):
        try:
            return data.decode(enc)
        except UnicodeDecodeError:
            continue
    return data.decode("utf-8", errors="replace")


SYSTEM = read_text_utf8(pathlib.Path(__file__).with_name("GLM_EXTRACT_PROMPT.md"))


def stub():
    return read_text_utf8(pathlib.Path(__file__).parents[1] / "vault/_templates/concept.md")


def call_glm(system, user):
    from zhipuai import ZhipuAI
    client = ZhipuAI(api_key=os.environ["ZHIPUAI_API_KEY"])
    r = client.chat.completions.create(
        model="glm-4-flash",
        temperature=0.1,
        messages=[{"role": "system", "content": system},
                  {"role": "user", "content": user}],
    )
    return r.choices[0].message.content


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("chunk")
    ap.add_argument("--topic", type=int, required=True)
    ap.add_argument("--objectives", default=None, help="JSON list of {id,text}")
    ap.add_argument("--existing", default=None, help="newline list of concept ids")
    ap.add_argument("--out", default=None, help="write note here (UTF-8); else stdout")
    a = ap.parse_args()

    chunk = read_chunk(a.chunk)
    objectives = json.loads(read_text_utf8(a.objectives)) if a.objectives else []
    existing = read_text_utf8(a.existing).split() if a.existing else []
    user = (f"topic: {a.topic}\n"
            f"syllabus_objectives: {json.dumps(objectives, ensure_ascii=False)}\n"
            f"existing_concept_ids: {existing}\n"
            f"--- SLIDE TEXT TO REWRITE (do not copy) ---\n{chunk}\n")

    if not os.environ.get("ZHIPUAI_API_KEY"):
        sys.stderr.write("[warn] no ZHIPUAI_API_KEY; emitting template stub\n")
        note = stub()
    else:
        try:
            note = call_glm(SYSTEM, user)
        except Exception as e:                    # never crash the batch
            sys.stderr.write(f"[warn] GLM call failed ({e}); emitting template stub\n")
            note = stub()

    if a.out:
        pathlib.Path(a.out).write_text(note, encoding="utf-8")
        sys.stderr.write(f"[ok] wrote {a.out}\n")
    else:
        print(note)


if __name__ == "__main__":
    main()
