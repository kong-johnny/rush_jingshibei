"""Figure 1: USTA Framework Architecture Diagram."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import set_style, FIGDIR
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import matplotlib.patheffects as pe

set_style()

fig, ax = plt.subplots(figsize=(7.5, 4.5))
ax.set_xlim(0, 10); ax.set_ylim(0, 6); ax.axis('off')
ax.set_facecolor('#FAFAFA'); fig.patch.set_facecolor('#FAFAFA')

# ── Color definitions ────────────────────────────────────────────────────────
COL = {
    'input':   '#D1E5F0',
    'layer1':  '#92C5DE',
    'layer2':  '#4393C3',
    'layer3':  '#2166AC',
    'offline': '#F4A582',
    'online':  '#D6604D',
    'output':  '#B2DF8A',
    'header':  '#1A237E',
}
BORDER = '#374151'

def box(ax, x, y, w, h, label, sublabel='', color='#D1E5F0', fs=9, sfs=7.5):
    rect = FancyBboxPatch((x - w/2, y - h/2), w, h,
                          boxstyle='round,pad=0.06', linewidth=0.9,
                          edgecolor=BORDER, facecolor=color, zorder=3)
    ax.add_patch(rect)
    dy = 0.12 if sublabel else 0
    ax.text(x, y + dy, label, ha='center', va='center', fontsize=fs,
            fontweight='bold', zorder=4, wrap=True)
    if sublabel:
        ax.text(x, y - 0.22, sublabel, ha='center', va='center',
                fontsize=sfs, fontstyle='italic', color='#374151', zorder=4)

def arrow(ax, x1, y1, x2, y2, color='#374151'):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=color, lw=1.3),
                zorder=5)

# ── Input row ────────────────────────────────────────────────────────────────
ax.text(5, 5.65, 'USTA Framework — Computational Pipeline',
        ha='center', va='center', fontsize=11, fontweight='bold', color=COL['header'])

box(ax, 2.0, 4.8, 2.4, 0.75, 'Weather Inputs', 'TMY: DNI, DHI, GHI, T_out', COL['input'])
box(ax, 5.0, 4.8, 2.4, 0.75, 'Building Config.', 'geometry g, materials m', COL['input'])
box(ax, 8.0, 4.8, 2.4, 0.75, 'Occupancy Forecast', r'$\hat{o}_{t:t+H-1}$', COL['input'])

arrow(ax, 2.0, 4.42, 2.0, 3.88)
arrow(ax, 5.0, 4.42, 5.0, 3.88)
arrow(ax, 8.0, 4.42, 7.0, 3.88)

# ── Layer 1 ──────────────────────────────────────────────────────────────────
box(ax, 4.5, 3.5, 5.5, 0.75, 'Layer 1: Perez Anisotropic Sky Transposition',
    r'$E^{POA}_{f,t}$ = Eq.(6)–(9)', COL['layer1'], fs=9)

arrow(ax, 4.5, 3.12, 4.5, 2.58)

# ── Layer 2 ──────────────────────────────────────────────────────────────────
box(ax, 4.5, 2.22, 5.5, 0.72, 'Layer 2: Solar Admission Model',
    r'$\tau_{f,t}(z,u_t)$ = Eq.(10); $Q^{sol}_t$ = Eq.(11)', COL['layer2'], fs=9)
arrow(ax, 4.5, 1.86, 4.5, 1.32)

# ── Layer 3 ──────────────────────────────────────────────────────────────────
box(ax, 4.5, 0.97, 5.5, 0.72, 'Layer 3: 3R2C Thermal State Update',
    r'$x_{t+1} = f_d(x_t, u_t, d_t; z)$ = Eq.(14)', COL['layer3'], fs=9)

# ── Branch to offline / online ───────────────────────────────────────────────
arrow(ax, 2.2, 0.97, 1.5, 0.97)   # left to offline
arrow(ax, 6.8, 0.97, 7.5, 0.97)   # right to online

# Offline
rect_off = FancyBboxPatch((0.1, 0.35), 2.7, 1.25,
    boxstyle='round,pad=0.07', lw=1.0, edgecolor='#B45309',
    facecolor=COL['offline'], zorder=2)
ax.add_patch(rect_off)
ax.text(1.45, 1.27, 'OFFLINE', ha='center', fontsize=8.5, fontweight='bold', color='#7C2D12')
ax.text(1.45, 0.97, 'NSGA-II', ha='center', fontsize=9, fontweight='bold')
ax.text(1.45, 0.67, 'Multi-Objective Design\n→ Pareto Front P*', ha='center', fontsize=7.5,
        fontstyle='italic', color='#374151')
ax.text(1.45, 0.35, 'z* via knee-point', ha='center', fontsize=7.5, color='#374151')

# Online
rect_on = FancyBboxPatch((7.2, 0.35), 2.7, 1.25,
    boxstyle='round,pad=0.07', lw=1.0, edgecolor='#991B1B',
    facecolor=COL['online'], zorder=2)
ax.add_patch(rect_on)
ax.text(8.55, 1.27, 'ONLINE', ha='center', fontsize=8.5, fontweight='bold', color='#450A0A')
ax.text(8.55, 0.97, 'MPC (QP)', ha='center', fontsize=9, fontweight='bold')
ax.text(8.55, 0.67, 'Receding Horizon\nH = 16 steps (4 h)', ha='center', fontsize=7.5,
        fontstyle='italic', color='#FFFFFF')
ax.text(8.55, 0.35, 'warm-start from P*', ha='center', fontsize=7.5, color='#FECACA')

# Warm-start arrow offline → online
ax.annotate('', xy=(7.2, 0.97), xytext=(2.8, 0.97),
            arrowprops=dict(arrowstyle='->', color='#374151', lw=1.0,
                            linestyle='dashed', connectionstyle='arc3,rad=-0.3'), zorder=5)
ax.text(5.0, 0.55, 'warm-start priors', ha='center', fontsize=7.5, color='#374151',
        fontstyle='italic')

# Feedback arrow (Online → Layer 3)
ax.annotate('', xy=(9.5, 0.97), xytext=(9.5, 2.0),
            arrowprops=dict(arrowstyle='<-', color='#374151', lw=1.0), zorder=5)
ax.text(9.75, 1.5, r'$u_t$', ha='left', fontsize=9, color='#374151')

plt.tight_layout(pad=0.3)
plt.savefig(f'{FIGDIR}/figure_1.png')
plt.close()
print('Figure 1 saved.')
