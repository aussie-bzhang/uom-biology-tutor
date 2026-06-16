# Environment setup — reuse Project 2, add two things

The BioChem-Tutor stack overlaps almost entirely with the existing LLM-Wiki /
Project 2 environment. You do NOT need a fresh environment.

## 1. Python (reuse Project 2's conda env)
Project 2's env already has gradio + pyswip + huggingface_hub. Add the two
Layer-1 pieces:

    conda activate <project2-env>        # or `llmwiki`
    pip install "markitdown[all]" zhipuai PyYAML   # PDF->md + GLM extraction + frontmatter
    # pyswip is optional; verify.py falls back to pure Python if swipl is absent

API key never in code — only env / HF Secrets:

    export ZHIPUAI_API_KEY=...           # used by extract/extract_concept.py

## 2. Node + Quartz v4 (the one genuinely new toolchain — JS, parallel to conda)
Quartz v4 requires Node >= 22 and npm >= 10.9.2.

    nvm install 22 && nvm use 22         # or download from nodejs.org
    node --version                       # v22.x+
    npm --version                        # 10.9.2+
    git clone https://github.com/jackyzha0/quartz.git
    cd quartz && npm i && npx quartz create   # point content at ../vault

## 3. Run the 4C gate (always works, no key needed)
    python verify/verify.py vault

## Copyright / privacy guardrails (unchanged)
- raw PPT/PDF: local only, never committed (.gitignore).
- verify/wiki.pl: private method layer, never committed (.gitignore).
- review questions: publish:false (not on the public site); flip the
  `vault/questions/` line in .gitignore if you want them out of the repo entirely.
