# 🌞 USTA: Unified Solar-Thermal-Adaptive Framework

<div align="center">

[![Paper](https://img.shields.io/badge/Paper-PDF-red.svg)](./main_twocolumn.pdf)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.9+-green.svg)](https://www.python.org/)

**From Static Shading to Time-Domain Control: A Unified Framework for Climate-Adaptive Passive Building Design**

*Qingru Zhang | Beijing Normal University*

[📄 Paper](./main_twocolumn.pdf) • [📊 Figures](./figures/) • [🔧 Scripts](./scripts/) • [🌐 Website](./docs/index.html)

</div>

---

## 🎯 What is USTA?

**USTA** is a physics-informed computational framework that revolutionizes passive solar building design by treating it as a **unified time-domain optimization problem**.

```
   Static Rules ──────────────► USTA ──────────────► Time-Domain Control
   
   "Noon geometry"                  "Every hour matters"
   Single objective                 5 objectives (Pareto)
   Design-only                      Design + Operation
   Steady-state                     Transient dynamics
```

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        USTA Framework                               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────────────┐  │
│  │   Layer 1    │───►│   Layer 2    │───►│      Layer 3         │  │
│  │              │    │              │    │                      │  │
│  │ Perez Sky    │    │ 3R2C Thermal│    │  NSGA-II + MPC       │  │
│  │ Model        │    │ Network     │    │  (Offline + Online)  │  │
│  │              │    │              │    │                      │  │
│  │ Anisotropic  │    │ Transient   │    │  Bi-level Opt.       │  │
│  │ Radiation    │    │ Dynamics    │    │                      │  │
│  └──────────────┘    └──────────────┘    └──────────────────────┘  │
│                                                                      │
│   Weather ─────────► Irradiance ─────────► Temperature ─────► Cost │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

## 🚀 Key Results

| Scenario | Metric | USTA | Baseline | Improvement |
|----------|--------|------|----------|-------------|
| Warm Climate | Cooling Load Proxy | ↓ 44.8% | - | ✅ Glare constraints met |
| Cold Climate | Heating Demand | ↓ 35.7% | - | ✅ 3× survivability |
| Dynamic Occupancy | Comfort Hours | 94.1% | 78.3% | +15.8 pp |
| Grid Outage | Hours ≥15°C | 45% | 18% | +27 pp |

## 🔬 Ablation Study

Each component matters:

```
┌─────────────────┬───────────────────┬─────────────────────┐
│ Remove Module   │ Impact            │ Magnitude           │
├─────────────────┼───────────────────┼─────────────────────┤
│ Perez Model     │ Cooling ↓         │ 4.7 pp decrease     │
│ 3R2C Dynamics   │ Comfort Violations│ 3.25× increase      │
│ MPC Control     │ Comfort Violations│ 5.6× increase       │
│ Pareto Search   │ Glare Violations  │ Systematic breach   │
└─────────────────┴───────────────────┴─────────────────────┘
```

## 📁 Project Structure

```
latex_paper/
├── main_twocolumn.tex    # Main paper (Elsevier format)
├── main_twocolumn.pdf    # Compiled PDF
├── references.bib        # Bibliography
├── figures/              # Paper figures (PNG)
├── scripts/              # Python scripts for all figures
│   ├── fig1_framework.py
│   ├── fig2_pareto_front.py
│   ├── fig3_solar_irradiance.py
│   ├── fig4_winter_temperature.py
│   ├── fig5_outage_survivability.py
│   ├── fig6_mpc_control.py
│   ├── fig7_latitude_generalization.py
│   ├── fig8_morris_sensitivity.py
│   └── style.py          # Plotting style
├── latex/                # Alternative LaTeX directory
└── docs/                 # GitHub Pages website
```

## 🛠️ Quick Start

### Regenerate Figures

```bash
cd scripts
pip install matplotlib numpy
python fig1_framework.py
python fig2_pareto_front.py
# ... etc
```

### Compile Paper

```bash
# Using tectonic
tectonic main_twocolumn.tex

# Or using pdflatex
pdflatex main_twocolumn.tex
bibtex main_twocolumn
pdflatex main_twocolumn.tex
pdflatex main_twocolumn.tex
```

## 📖 Citation

```bibtex
@article{zhang2024usta,
  title={From Static Shading to Time-Domain Control: A Unified Solar-Thermal-Adaptive Framework for Climate-Adaptive Passive Building Design},
  author={Zhang, Qingru},
  journal={Energy and Buildings},
  year={2024},
  institution={Beijing Normal University}
}
```

## 👤 Author

**Qingru Zhang (张清茹)**
- 🎓 School of Artificial Intelligence, Beijing Normal University
- 📧 Email: trueshz@qq.com

**Advisor:** Prof. Guo Jianwei (郭建伟)

## 📜 License

MIT License - feel free to use and build upon!

---

<div align="center">

**⭐ Star this repo if you find it useful! ⭐**

Made with ❤️ and ☀️

[🌐 View Website](./docs/index.html)

</div>
