# -*- coding: utf-8 -*-
"""Convert paper .tex sections to HTML for project page (full text, MathJax)."""
import re
import html as html_module

from cite_map import format_cite_html

PAPER = r"E:\Desktop\test\paper\sec"


def esc(s: str) -> str:
    return html_module.escape(s, quote=False)


def take_braced(s: str, start: int):
    """start at position of '{', return (content, end_after_brace)."""
    if start >= len(s) or s[start] != "{":
        return None, start
    depth = 0
    j = start
    while j < len(s):
        if s[j] == "{":
            depth += 1
        elif s[j] == "}":
            depth -= 1
            if depth == 0:
                return s[start + 1 : j], j + 1
        j += 1
    return None, start


def tex_to_html_inline(s: str) -> str:
    """Recursive LaTeX inline to HTML; preserves \\( \\) and $ $ for MathJax."""
    if not s:
        return ""
    out = []
    i = 0
    while i < len(s):
        if s.startswith("\\(", i):
            j = s.find("\\)", i + 2)
            if j != -1:
                out.append(s[i : j + 2])
                i = j + 2
                continue
        if i < len(s) and s[i] == "$" and (i == 0 or s[i - 1] != "\\"):
            j = s.find("$", i + 1)
            if j != -1:
                out.append(s[i : j + 1])
                i = j + 1
                continue
        if s.startswith("\\textbf{", i):
            inner, j = take_braced(s, i + 7)
            if inner is not None:
                out.append("<strong>" + tex_to_html_inline(inner) + "</strong>")
                i = j
                continue
        if s.startswith("\\emph{", i):
            inner, j = take_braced(s, i + 5)
            if inner is not None:
                out.append("<em>" + tex_to_html_inline(inner) + "</em>")
                i = j
                continue
        if s.startswith("\\textit{", i):
            inner, j = take_braced(s, i + 7)
            if inner is not None:
                out.append("<em>" + tex_to_html_inline(inner) + "</em>")
                i = j
                continue
        m_bf = re.match(r"\{\\bf\s*([^}]*)\}", s[i:])
        if m_bf:
            out.append("<strong>" + tex_to_html_inline(m_bf.group(1)) + "</strong>")
            i += m_bf.end()
            continue
        if s.startswith("{\\bf ", i) or s.startswith("\\noindent{\\bf ", i):
            m = re.match(r"\\?noindent?\{\\bf\s+([^}]*)\}", s[i:])
            if m:
                out.append("<strong>" + tex_to_html_inline(m.group(1)) + "</strong>")
                i += m.end()
                continue
        if s.startswith("\\cite{", i):
            inner, j = take_braced(s, i + 5)
            if inner is not None:
                out.append(format_cite_html(inner))
                i = j
                continue
        if s.startswith("~", i):
            out.append(" ")
            i += 1
            continue
        if s.startswith("\\%", i):
            out.append("%")
            i += 2
            continue
        c = s[i]
        if c in "&<>":
            out.append(esc(c))
        else:
            out.append(c)
        i += 1
    return "".join(out)


def strip_tex_comments(tex: str) -> str:
    lines = []
    for line in tex.splitlines():
        if line.strip().startswith("%") and not line.strip().startswith("%\\"):
            continue
        if "%" in line and not line.strip().startswith("%"):
            # keep escaped \%
            idx = 0
            while True:
                p = line.find("%", idx)
                if p == -1:
                    break
                if p > 0 and line[p - 1] == "\\":
                    idx = p + 1
                    continue
                line = line[:p].rstrip()
                break
        lines.append(line)
    return "\n".join(lines)


def ref_replace(s: str) -> str:
    s = re.sub(r"Fig\.~?\s*\\ref\s*\{([^}]+)\}", r"Fig. [\1]", s)
    s = re.sub(r"Table~?\s*\\ref\s*\{([^}]+)\}", r"Table [\1]", s)
    s = re.sub(r"Tab\.~?\s*\\ref\s*\{([^}]+)\}", r"Table [\1]", s)
    s = re.sub(r"Eq\.~?\s*\\ref\s*\{([^}]+)\}", r"Eq. (\1)", s)
    s = re.sub(r"Sec\.~?\s*\\ref\s*\{([^}]+)\}", r"Sec. [\1]", s)
    s = re.sub(r"\\ref\s*\{([^}]+)\}", r"[\1]", s)
    return s


def env_equation_to_html(block: str) -> str:
    inner = re.sub(r"\\begin\{equation\}|\\end\{equation\}", "", block, flags=re.DOTALL).strip()
    inner = re.sub(r"\\label\{[^}]+\}", "", inner).strip()
    return f'<div class="math-display">\\[{inner}\\]</div>'


def env_aligned_to_html(block: str) -> str:
    inner = re.sub(r"\\begin\{aligned\}|\\end\{aligned\}", "", block, flags=re.DOTALL)
    inner = re.sub(r"\\label\{[^}]+\}", "", inner).strip()
    return f'<div class="math-display">\\[\\begin{{aligned}}{inner}\\end{{aligned}}\\]</div>'


def process_paragraph(p: str) -> str:
    p = p.strip()
    if not p:
        return ""
    if p.startswith("<figure") or p.startswith('<div class="table-container') or p.startswith('<div class="math-display'):
        return p
    p = ref_replace(p)
    p = re.sub(r"\\noindent\s*", "", p)
    p = re.sub(r"\\label\{[^}]+\}\s*", "", p)
    p = tex_to_html_inline(p)
    return p


def split_paragraphs(t: str):
    return [x.strip() for x in re.split(r"\n\s*\n+", t) if x.strip()]


BLOCK_HTML_PAT = re.compile(
    r'<figure\b[\s\S]*?</figure>|<div class="table-container[\s\S]*?</div>|<div class="math-display[\s\S]*?</div>',
    re.IGNORECASE,
)


def extract_tex_caption(block: str) -> str:
    k = block.find("\\caption{")
    if k == -1:
        return ""
    brace = k + len("\\caption{") - 1
    inner, _ = take_braced(block, brace)
    return inner if inner is not None else ""


def read(fp):
    with open(fp, "r", encoding="utf-8") as f:
        return f.read()


def intro():
    t = strip_tex_comments(read(f"{PAPER}/1_intro.tex"))
    t = re.sub(r"\\section\{[^}]*\}", "", t)
    t = re.sub(r"\\label\{[^}]+\}", "", t)
    pre, _, rest = t.partition("\\begin{itemize}")
    items_block = rest.split("\\end{itemize}")[0]
    paras = split_paragraphs(pre)
    html = [f"<p>{process_paragraph(p)}</p>" for p in paras if p]
    raw_items = items_block.split("\\item")
    lis = []
    for it in raw_items[1:]:
        it = it.strip()
        if not it or it.startswith("%"):
            continue
        lis.append(f"<li>{process_paragraph(it)}</li>")
    html.append("<ul>" + "".join(lis) + "</ul>")
    return "\n".join(html)


def method_overview_figure_html() -> str:
    """Fig.~\\ref{fig:method}: framework diagram; caption from 2_realated_work.tex figure*."""
    t = strip_tex_comments(read(f"{PAPER}/2_realated_work.tex"))
    _end = t.find("\\end{figure*}")
    if _end == -1:
        _end = t.find("\\end{figure}")
    if _end == -1:
        _end = len(t)
    cap_raw = extract_tex_caption(t[:_end])
    cap = ""
    if cap_raw:
        cap = cap_raw.replace("\n", " ")
        cap = re.sub(r"\s+", " ", cap)
        cap = ref_replace(cap)
        cap = tex_to_html_inline(cap)
    return f"""<figure class="paper-figure">
<img src="static/images/method.png" alt="Framework overview" loading="lazy" width="1600" height="720">
<figcaption class="is-size-7 has-text-grey">{cap}</figcaption>
</figure>"""


def related():
    t = strip_tex_comments(read(f"{PAPER}/2_realated_work.tex"))
    t = re.sub(r"\\begin\{figure\*\}.*?\\end\{figure\*\}", "", t, flags=re.DOTALL)
    t = re.sub(r"\\section\{Related Work\}", "", t)
    t = re.sub(r"\\label\{[^}]+\}", "", t)
    paras = split_paragraphs(t)
    ps = [f"<p>{process_paragraph(p)}</p>" for p in paras if p.strip()]
    return "\n".join(ps)


def extract_equations_and_text(chunk: str):
    """Split chunk into alternating text and equation blocks."""
    parts = []
    pos = 0
    while pos < len(chunk):
        m = re.search(r"\\begin\{equation\}", chunk[pos:])
        if not m:
            parts.append(("text", chunk[pos:]))
            break
        s = pos + m.start()
        if s > pos:
            parts.append(("text", chunk[pos:s]))
        m_end = re.search(r"\\end\{equation\}", chunk[s:])
        if not m_end:
            parts.append(("text", chunk[s:]))
            break
        e = s + m_end.end()
        parts.append(("eq", chunk[s:e]))
        pos = e
    return parts


def method():
    t = strip_tex_comments(read(f"{PAPER}/3_method.tex"))
    t = re.sub(r"\\section\{Method\}", "", t)
    # figures
    def sub_fig(m):
        block = m.group(0)
        c = extract_tex_caption(block) or ""
        c = ref_replace(c)
        c = tex_to_html_inline(c.replace("\n", " "))
        src = "RCPQ.png" if "RCPQ" in block else "method.png"
        return f'<figure class="paper-figure"><img src="static/images/{src}" alt="" loading="lazy"><figcaption class="is-size-7 has-text-grey">{c}</figcaption></figure>'

    t = re.sub(r"\\begin\{figure\}.*?\\end\{figure\}", sub_fig, t, flags=re.DOTALL)
    # subsections
    pieces = re.split(r"(\\subsection\{[^}]+\})", t)
    out = [method_overview_figure_html()]
    i = 0
    while i < len(pieces):
        piece = pieces[i]
        if piece.startswith("\\subsection"):
            title = re.match(r"\\subsection\{([^}]+)\}", piece)
            tit = title.group(1).strip() if title else ""
            out.append(f'<h4 class="title is-5 paper-subsection">{esc(tit)}</h4>')
            i += 1
            if i < len(pieces):
                out.append(method_chunk(pieces[i]))
            i += 1
        else:
            if piece.strip():
                out.append(method_chunk(piece))
            i += 1
    return "\n".join(out)


def method_chunk(text: str) -> str:
    text = re.sub(r"\\vspace\{[^}]+\}", "", text)
    # \[ \] display
    blocks = []
    pos = 0
    for m in re.finditer(r"\\\[(.*?)\\\]", text, re.DOTALL):
        if m.start() > pos:
            blocks.append(("t", text[pos : m.start()]))
        blocks.append(("d", m.group(1).strip()))
        pos = m.end()
    if pos < len(text):
        blocks.append(("t", text[pos:]))
    html = []
    for kind, content in blocks:
        if kind == "d":
            lab = re.sub(r"\\label\{[^}]+\}", "", content).strip()
            html.append(f'<div class="math-display">\\[{lab}\\]</div>')
        else:
            # equation env
            pos2 = 0
            c = content
            while "\\begin{equation}" in c[pos2:]:
                a = c.find("\\begin{equation}", pos2)
                if a > pos2:
                    html.append(text_to_paragraphs(c[pos2:a]))
                b = c.find("\\end{equation}", a)
                if b == -1:
                    break
                blk = c[a : b + len("\\end{equation}")]
                html.append(env_equation_to_html(blk))
                pos2 = b + len("\\end{equation}")
            html.append(text_to_paragraphs(c[pos2:]))
    return "\n".join(html)


def text_to_paragraphs(t: str) -> str:
    if not t.strip():
        return ""
    out = []
    pos = 0
    for m in BLOCK_HTML_PAT.finditer(t):
        if m.start() > pos:
            chunk = t[pos : m.start()].strip()
            if chunk:
                for p in split_paragraphs(chunk):
                    if p.strip():
                        out.append(f"<p>{process_paragraph(p)}</p>")
        out.append(m.group(0).strip())
        pos = m.end()
    if pos < len(t):
        chunk = t[pos:].strip()
        if chunk:
            for p in split_paragraphs(chunk):
                if p.strip():
                    out.append(f"<p>{process_paragraph(p)}</p>")
    return "\n".join(out)


def experiment():
    t = strip_tex_comments(read(f"{PAPER}/4_experiment.tex"))
    t = re.sub(r"\\section\{Experiment\}", "", t)
    tab1 = """<div class="table-container paper-table-wrap"><table class="table is-bordered is-striped is-narrow is-size-7">
<caption>Quantitative comparison of anomaly detection performance on the LIBERO-Anomaly-10 benchmark.</caption>
<thead><tr><th>Method</th><th colspan="2">Gripper Open</th><th colspan="2">Gripper Slippage</th><th colspan="2">Spatial Misalignment</th><th colspan="2">Average</th></tr>
<tr><th></th><th>AUC</th><th>AP</th><th>AUC</th><th>AP</th><th>AUC</th><th>AP</th><th>AUC</th><th>AP</th></tr></thead>
<tbody>
<tr><td>GPT-5</td><td>0.9137</td><td>0.9642</td><td>0.8941</td><td>0.8720</td><td>0.4904</td><td>0.4015</td><td>0.8500</td><td>0.8507</td></tr>
<tr><td>Gemini 2.5 Pro</td><td>0.8644</td><td>0.9333</td><td>0.8633</td><td>0.8505</td><td>0.5167</td><td>0.4271</td><td>0.8186</td><td>0.8313</td></tr>
<tr><td>Claude 4.5</td><td>0.8754</td><td>0.9401</td><td>0.8551</td><td>0.8285</td><td>0.5292</td><td>0.4290</td><td>0.8214</td><td>0.8249</td></tr>
<tr><td>FailDetect</td><td>0.7883</td><td>0.9032</td><td>0.6665</td><td>0.6932</td><td>0.6557</td><td>0.5820</td><td>0.7181</td><td>0.7700</td></tr>
<tr class="has-background-light"><td><strong>RC-NF (Ours)</strong></td><td><strong>0.9312</strong></td><td><strong>0.9781</strong></td><td><strong>0.9195</strong></td><td><strong>0.9180</strong></td><td><strong>0.9676</strong></td><td><strong>0.9585</strong></td><td><strong>0.9309</strong></td><td><strong>0.9494</strong></td></tr>
</tbody></table></div>"""
    tab2 = """<div class="table-container paper-table-wrap"><table class="table is-bordered is-striped is-narrow is-size-7">
<caption>Ablation study of the proposed Robot-Conditioned Point Query Network (RCPQNet). RC-NF (Ours) denotes the full model.</caption>
<thead><tr><th>Row</th><th>Method</th><th colspan="2">Gripper Open</th><th colspan="2">Gripper Slippage</th><th colspan="2">Spatial Misalignment</th><th colspan="2">Average</th></tr>
<tr><th></th><th></th><th>AUC</th><th>AP</th><th>AUC</th><th>AP</th><th>AUC</th><th>AP</th><th>AUC</th><th>AP</th></tr></thead>
<tbody>
<tr class="has-background-light"><td>1</td><td><strong>RC-NF (Ours)</strong></td><td><strong>0.9312</strong></td><td><strong>0.9781</strong></td><td><strong>0.9195</strong></td><td><strong>0.9180</strong></td><td><strong>0.9676</strong></td><td><strong>0.9585</strong></td><td><strong>0.9309</strong></td><td><strong>0.9494</strong></td></tr>
<tr><td>2</td><td>w/o Task Embedding</td><td>0.8769</td><td>0.9603</td><td>0.8668</td><td>0.8680</td><td>0.8139</td><td>0.8118</td><td>0.8643</td><td>0.9008</td></tr>
<tr><td>3</td><td>w/o Robot State</td><td>0.6327</td><td>0.8621</td><td>0.7443</td><td>0.8116</td><td>0.8929</td><td>0.8617</td><td>0.7152</td><td>0.8401</td></tr>
<tr><td>4</td><td>w/o Pos. Residual branch</td><td>0.9045</td><td>0.9712</td><td>0.8971</td><td>0.9085</td><td>0.8543</td><td>0.8072</td><td>0.8947</td><td>0.9225</td></tr>
<tr><td>5</td><td>w/o Dyn. Shape branch</td><td>0.7666</td><td>0.9234</td><td>0.7763</td><td>0.8108</td><td>0.1022</td><td>0.2755</td><td>0.6841</td><td>0.7899</td></tr>
</tbody></table></div>"""
    t = re.sub(r"\\begin\{table\*\}.*?\\end\{table\*\}", "___T1___", t, count=1, flags=re.DOTALL)
    t = re.sub(r"\\begin\{table\*\}.*?\\end\{table\*\}", "___T2___", t, count=1, flags=re.DOTALL)

    def fig_sub(m, path, w):
        raw = extract_tex_caption(m.group(0))
        c = raw.replace("\n", " ") if raw else ""
        c = ref_replace(c)
        c = tex_to_html_inline(c)
        return f'<figure class="paper-figure"><img src="{path}" alt="" style="max-width:{w}" loading="lazy"><figcaption class="is-size-7 has-text-grey">{c}</figcaption></figure>'

    t = re.sub(
        r"\\begin\{figure\}.*?\\end\{figure\}",
        lambda m: fig_sub(m, "static/images/exp_sim.png", "min(100%,720px)"),
        t,
        count=1,
        flags=re.DOTALL,
    )
    t = re.sub(
        r"\\begin\{figure\}.*?\\end\{figure\}",
        lambda m: fig_sub(m, "static/images/exp_real_0.png", "min(100%,720px)"),
        t,
        count=1,
        flags=re.DOTALL,
    )
    t = re.sub(
        r"\\begin\{figure\*\}.*?\\end\{figure\*\}",
        lambda m: fig_sub(m, "static/images/exp_real1.png", "100%"),
        t,
        count=1,
        flags=re.DOTALL,
    )
    t = re.sub(
        r"\\begin\{figure\}.*?\\end\{figure\}",
        lambda m: fig_sub(m, "static/images/exp_real2.png", "min(100%,720px)"),
        t,
        count=1,
        flags=re.DOTALL,
    )
    t = t.replace("___T1___", tab1)
    t = t.replace("___T2___", tab2)
    pieces = re.split(r"(\\subsection\{[^}]+\})", t)
    out = []
    i = 0
    while i < len(pieces):
        piece = pieces[i]
        if piece.startswith("\\subsection"):
            title = re.match(r"\\subsection\{([^}]+)\}", piece)
            tit = title.group(1).strip() if title else ""
            out.append(f'<h4 class="title is-5 paper-subsection">{esc(tit)}</h4>')
            i += 1
            if i < len(pieces):
                out.append(exp_chunk(pieces[i]))
            i += 1
        else:
            if piece.strip():
                out.append(exp_chunk(piece))
            i += 1
    return "\n".join(out)


def exp_chunk(text: str) -> str:
    text = re.sub(r"\\label\{[^}]+\}", "", text)
    pos = 0
    html = []
    while pos < len(text):
        m = re.search(r"\\begin\{equation\}", text[pos:])
        if not m:
            html.append(text_to_paragraphs(text[pos:]))
            break
        s = pos + m.start()
        if s > pos:
            html.append(text_to_paragraphs(text[pos:s]))
        e = text.find("\\end{equation}", s)
        if e == -1:
            html.append(text_to_paragraphs(text[s:]))
            break
        blk = text[s : e + len("\\end{equation}")]
        html.append(env_equation_to_html(blk))
        pos = e + len("\\end{equation}")
    return "\n".join(html)


def conclusion():
    t = strip_tex_comments(read(f"{PAPER}/5_conclusion.tex"))
    t = re.sub(r"\\section\{[^}]*\}", "", t)
    return text_to_paragraphs(t)


def ack():
    t = strip_tex_comments(read(f"{PAPER}/Acknowledgments.tex"))
    t = re.sub(r"\\section\*\{[^}]*\}", "", t)
    return text_to_paragraphs(t)


if __name__ == "__main__":
    blocks = {
        "intro": intro(),
        "related": related(),
        "method": method(),
        "experiment": experiment(),
        "conclusion": conclusion(),
        "ack": ack(),
    }
    out_path = r"E:\Desktop\test\RC-NF\static\paper-body-fragments.html"
    with open(out_path, "w", encoding="utf-8") as f:
        for k, v in blocks.items():
            f.write(f"<!-- BEGIN {k} -->\n{v}\n<!-- END {k} -->\n\n")
    print("Wrote", out_path)
