# RC-NF: Robot-Conditioned Normalizing Flow for Real-Time Anomaly Detection in Robotic Manipulation

**Accepted to CVPR 2026.**

This repository hosts the **project page** for our paper on real-time anomaly monitoring for robotic manipulation. RC-NF is a robot-conditioned normalizing flow that runs as a plug-and-play monitor for vision-language-action (VLA) policies, producing anomaly scores in **under 100 ms** on real hardware.

**Project page:** [https://heikaishuizz.github.io/RC-NF/](https://heikaishuizz.github.io/RC-NF/)  
**Paper (arXiv):** [2603.11106](https://arxiv.org/abs/2603.11106)

## Authors

Shijie Zhou<sup>1,2</sup>, [Bin Zhu](https://binzhubz.github.io/)<sup>3</sup>, [Jiarui Yang](https://flyfaerss.github.io/)<sup>1,2</sup>, [Xiangyu Zhao](https://xyzhao.top/)<sup>1,2</sup>, [Jingjing Chen](https://jingjing1.github.io/#teach)<sup>1,2,*</sup>, [Yu-Gang Jiang](https://scholar.google.com/citations?user=f3_FP8AAAAAJ)<sup>1,2</sup>

<sup>1</sup> Institute of Trustworthy Embodied AI, Fudan University  
<sup>2</sup> Shanghai Key Laboratory of Multimodal Embodied AI  
<sup>3</sup> Singapore Management University  

## Abstract (short)

VLA models trained by imitation learning often fail under out-of-distribution (OOD) conditions. RC-NF monitors whether the joint distribution of **robot states** and **task-relevant object trajectories** matches normal execution using a **conditional normalizing flow** trained only on successful demonstrations. A key component is **RCPQNet** (Robot-Conditioned Point Query Network), an affine coupling layer that conditions on task embeddings and robot state while processing **SAM2**-based point sets. We also introduce **LIBERO-Anomaly-10**, a benchmark with gripper open, slippage, and spatial misalignment anomalies. RC-NF achieves strong AUC/AP on the benchmark and supports **task-level replanning** and **state-level rollback** in real-world demos with a VLA (e.g., π₀).

## Acknowledgments

- Page structure derives from the [Academic Project Page Template](https://github.com/eliahuhorwitz/Academic-project-page-template) and the [Nerfies](https://nerfies.github.io/) project page (see footer on the website).

## License

Website content is licensed under [CC BY-SA 4.0](http://creativecommons.org/licenses/by-sa/4.0/).
