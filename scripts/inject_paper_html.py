# -*- coding: utf-8 -*-
"""Inject paper-body-fragments.html into index.html paper-fold-body divs."""
import re
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent


def main():
    frag = (BASE / "static/paper-body-fragments.html").read_text(encoding="utf-8")

    def extract_block(name: str) -> str:
        m = re.search(
            rf"<!-- BEGIN {name} -->(.*?)<!-- END {name} -->", frag, re.DOTALL
        )
        return m.group(1).strip() if m else ""

    idx = (BASE / "index.html").read_text(encoding="utf-8")
    mapping = [
        ("paper-intro", "intro"),
        ("paper-related", "related"),
        ("paper-method", "method"),
        ("paper-experiments", "experiment"),
        ("paper-conclusion", "conclusion"),
        ("paper-ack", "ack"),
    ]
    for dom_id, block in mapping:
        inner = extract_block(block)
        pat = (
            rf'(<details class="paper-fold[^"]*" id="{re.escape(dom_id)}">\s*'
            r"<summary>.*?</summary>\s*"
            r'<div class="paper-fold-body content has-text-justified">\s*)'
            r"[\s\S]*?"
            r"(\s*</div>\s*</details>)"
        )

        def repl(m, _inner=inner):
            return m.group(1) + _inner + m.group(2)

        new_idx, n = re.subn(pat, repl, idx, count=1, flags=re.DOTALL)
        if n != 1:
            raise SystemExit(f"inject failed for {dom_id}, n={n}")
        idx = new_idx
    (BASE / "index.html").write_text(idx, encoding="utf-8")
    print("Injected 6 paper sections into index.html")


if __name__ == "__main__":
    main()
