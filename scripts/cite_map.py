# -*- coding: utf-8 -*-
"""BibTeX key → reference number [1–52], same order as RC-NF/reference.md / CVPR ref list."""

CITE_KEY_TO_NUM = {
    "agia2024unpacking": 1,
    "alinezhad2023understanding": 2,
    "altan2023clue": 3,
    "anthropic2025claude45": 4,
    "black2024pi0": 5,
    "black2025pi05": 6,
    "cheng2024yolo": 7,
    "comanici2025gemini": 8,
    "cui2025openhelix": 9,
    "delic2025sequential": 10,
    "fu2025llmdet": 11,
    "han2024dual": 12,
    "hirschorn2023normalizing": 13,
    "huang2024copa": 14,
    "huang2024rekep": 15,
    "ji2025robobrain": 16,
    "jiang2025galaxea": 17,
    "karaev2024cotracker": 18,
    "kim2024openvla": 19,
    "kim2025fine": 20,
    "kingma2018glow": 21,
    "kirillov2023segment": 22,
    "li2023vision": 23,
    "li2025hamster": 24,
    "liu2023libero": 25,
    "liu2024model": 26,
    "luo2025visual": 27,
    "nvidia2025gr00t": 28,
    "openai2025gpt5": 29,
    "pan2025omnimanip": 30,
    "perez2018film": 31,
    "ravi2024sam": 32,
    "ren2024dino": 33,
    "romer2025failure": 34,
    "ross2011reduction": 35,
    "seo2025unisafe": 36,
    "shafer2008tutorial": 37,
    "sliwowski2024conditionnet": 38,
    "song2025rationalvla": 39,
    "wang2023tracking": 40,
    "wen2023any": 41,
    "willibald2025hierarchical": 42,
    "willibald2025multimodal": 43,
    "wu2025flow": 44,
    "wu2025foresight": 45,
    "xi2025ow": 46,
    "xu2025can": 47,
    "yang2025actor": 48,
    "yang2024consistency": 49,
    "yang2024follow": 50,
    "zhang2024hirt": 51,
    "zitkovich2023rt": 52,
}


def format_cite_html(inner: str) -> str:
    """Turn \\cite{a,b,c} content into [1, 2, 3] using CITE_KEY_TO_NUM."""
    keys = [k.strip() for k in inner.split(",") if k.strip()]
    nums = []
    missing = []
    for k in keys:
        n = CITE_KEY_TO_NUM.get(k)
        if n is None:
            missing.append(k)
        else:
            nums.append(n)
    nums = sorted(set(nums))
    parts = [str(n) for n in nums]
    if missing:
        parts.extend(missing)
    body = ", ".join(parts)
    return f'<span class="cite-keys">[{body}]</span>'
