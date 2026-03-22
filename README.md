# RC-NF: Robot-Conditioned Normalizing Flow for Real-Time Anomaly Detection in Robotic Manipulation

**Accepted to CVPR 2026.**

This repository hosts the **project page** for our paper on real-time anomaly monitoring for robotic manipulation. RC-NF is a robot-conditioned normalizing flow that runs as a plug-and-play monitor for vision-language-action (VLA) policies, producing anomaly scores in **under 100 ms** on real hardware.

**Project page:** [https://heikaishuizz.github.io/RC-NF/](https://heikaishuizz.github.io/RC-NF/)  
**Paper (arXiv):** [2603.11106](https://arxiv.org/abs/2603.11106)

## Authors

Shijie Zhou<sup>1,2</sup>, Bin Zhu<sup>3</sup>, Jiarui Yang<sup>1,2</sup>, Xiangyu Zhao<sup>1,2</sup>, Jingjing Chen<sup>1,2,*</sup>, Yu-Gang Jiang<sup>1,2</sup>

<sup>1</sup> Institute of Trustworthy Embodied AI, Fudan University  
<sup>2</sup> Shanghai Key Laboratory of Multimodal Embodied AI  
<sup>3</sup> Singapore Management University  

## Abstract (short)

VLA models trained by imitation learning often fail under out-of-distribution (OOD) conditions. RC-NF monitors whether the joint distribution of **robot states** and **task-relevant object trajectories** matches normal execution using a **conditional normalizing flow** trained only on successful demonstrations. A key component is **RCPQNet** (Robot-Conditioned Point Query Network), an affine coupling layer that conditions on task embeddings and robot state while processing **SAM2**-based point sets. We also introduce **LIBERO-Anomaly-10**, a benchmark with gripper open, slippage, and spatial misalignment anomalies. RC-NF achieves strong AUC/AP on the benchmark and supports **task-level replanning** and **state-level rollback** in real-world demos with a VLA (e.g., π₀).

## Repository layout

| Path | Description |
|------|-------------|
| `index.html` | Main project page (hero, videos, paper sections, BibTeX) |
| `static/css/`, `static/js/` | Styles and scripts |
| `static/images/` | Figures, teaser, favicon |
| `static/videos/` | Real-world and simulation demo videos |
| `static/paper-body-fragments.html` | Generated HTML for collapsible paper sections |
| `scripts/build_paper_body.py` | Converts `paper/sec/*.tex` → HTML fragments |
| `scripts/inject_paper_html.py` | Injects fragments into `index.html` |
| `scripts/cite_map.py` | BibTeX key → numeric citation mapping for the page |

To regenerate the long-form paper text on the site (when LaTeX sources under your `paper/sec` tree change):

```bash
cd scripts
python build_paper_body.py
python inject_paper_html.py
```

## Local preview

Open `index.html` in a browser, or use any static server from the repo root, for example:

```bash
python -m http.server 8000
```

Then visit `http://localhost:8000`.

## Acknowledgments

- Page structure derives from the [Academic Project Page Template](https://github.com/eliahuhorwitz/Academic-project-page-template) and the [Nerfies](https://nerfies.github.io/) project page (see footer on the website).

## License

Website content is licensed under [CC BY-SA 4.0](http://creativecommons.org/licenses/by-sa/4.0/).
