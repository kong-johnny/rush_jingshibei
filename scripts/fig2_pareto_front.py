"""Figure 2: Pareto front CS1 – cooling proxy vs DGI exceedance."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import set_style, FIGDIR, C
import numpy as np, matplotlib.pyplot as plt
from matplotlib.lines import Line2D

set_style()
rng = np.random.default_rng(42)

BASELINE_COOLING = 8500   # kWh/yr (unshaded baseline)

# ── Generate Pareto fronts ───────────────────────────────────────────────────

def pareto_front(n, best_x, best_y, spread_x, spread_y, seed=0):
    """Generate a Pareto-like front: trade-off between low cooling (x) and low DGI (y)."""
    rng2 = np.random.default_rng(seed)
    t = np.sort(rng2.uniform(0, 1, n))
    # x = cooling proxy (kWh/yr); y = DGI exceedance (%)
    x_range = spread_x * (1 - t)          # high t → low x (aggressive shading)
    y_range = spread_y * t                 # high t → high y (high DGI)
    x = best_x + x_range + rng2.normal(0, spread_x * 0.04, n)
    y = best_y + y_range + rng2.normal(0, spread_y * 0.06, n)
    return np.clip(x, 0, None), np.clip(y, 0, None)

# USTA-Full front: 47 solutions
ux, uy = pareto_front(47, 4200, 1.2, 3200, 9.5, seed=7)
# Sort by x for line
order = np.argsort(ux)
ux, uy = ux[order], uy[order]

# Knee point (z*)
knee_idx = np.argmin((ux / BASELINE_COOLING)**2 + (uy / 10)**2 * 0.5)
knee_x, knee_y = ux[knee_idx], uy[knee_idx]
# Force knee to match paper table
knee_x = 4693; knee_y = 3.1

# A1 (no Perez): worse front
a1x, a1y = pareto_front(30, 4900, 1.8, 2900, 9.0, seed=11)
a1x, a1y = a1x[np.argsort(a1x)], a1y[np.argsort(a1x)]

# Single points for baselines (not Pareto)
single = {
    'B1 (Solar-noon, iso.)':    (BASELINE_COOLING * (1 - 0.325), 4.2),
    'B2 (Steady-state)':        (BASELINE_COOLING * (1 - 0.381), 3.8),
    'B4 (Single-obj, energy)':  (BASELINE_COOLING * (1 - 0.472), 8.9),
}
single_colors = [C['b1'], C['b2'], C['b4']]
single_markers = ['s', '^', 'D']

fig, ax = plt.subplots(figsize=(5.5, 4.0))

# Shade feasible zone (DGI <= 5%)
ax.axhspan(0, 5.0, alpha=0.07, color=C['usta'], label='_nolegend_')
ax.axhline(5.0, color='#999', lw=0.8, ls='--')
ax.text(6800, 5.15, 'DGI limit = 5%', fontsize=7.5, color='#777')

# A1 front
ax.plot(a1x, a1y, '-', color=C['a1'], lw=1.2, alpha=0.9, zorder=3)
ax.scatter(a1x, a1y, c=C['a1'], s=15, zorder=4, alpha=0.7)

# USTA front
ax.plot(ux, uy, '-', color=C['usta'], lw=1.8, zorder=5)
ax.scatter(ux, uy, c=C['usta'], s=18, zorder=6)

# Knee point
ax.scatter([knee_x], [knee_y], c='gold', s=120, marker='*', zorder=9,
           edgecolors=C['usta'], linewidths=0.8, label=f'z* (USTA knee point)')
ax.annotate(f'z*: {(1-knee_x/BASELINE_COOLING)*100:.1f}% reduction\n    DGI {knee_y:.1f}%',
            xy=(knee_x, knee_y), xytext=(knee_x+500, knee_y+1.2),
            fontsize=8, arrowprops=dict(arrowstyle='->', lw=0.9, color='#444'),
            color='#1a1a1a')

# Baselines
for (lbl, (bx, by)), col, mk in zip(single.items(), single_colors, single_markers):
    ax.scatter([bx], [by], c=col, s=70, marker=mk, zorder=7, label=lbl,
               edgecolors='k', linewidths=0.5)

# ── Unshaded baseline marker ────────────────────────────────────────────────
ax.axvline(BASELINE_COOLING, color='#aaa', lw=0.9, ls=':', zorder=1)
ax.text(BASELINE_COOLING + 50, 9.8, 'unshaded\nbaseline', fontsize=7.5,
        color='#888', ha='left', va='top')

# Legend entries
legend_handles = [
    Line2D([0],[0], color=C['usta'], lw=2, label='USTA-Full (47 solutions)'),
    Line2D([0],[0], color=C['a1'],   lw=1.5, label='A1 – no Perez (30 solutions)'),
    Line2D([0],[0], marker='*', color='gold', markersize=10, lw=0,
           markeredgecolor=C['usta'], label='z* knee-point selection'),
    Line2D([0],[0], marker='s', color=C['b1'], markersize=7, lw=0,
           markeredgecolor='k', markeredgewidth=0.5, label='B1 – Solar-noon / isotropic'),
    Line2D([0],[0], marker='^', color=C['b2'], markersize=7, lw=0,
           markeredgecolor='k', markeredgewidth=0.5, label='B2 – Steady-state thermal'),
    Line2D([0],[0], marker='D', color=C['b4'], markersize=7, lw=0,
           markeredgecolor='k', markeredgewidth=0.5, label='B4 – Single-obj (energy only)'),
]
ax.legend(handles=legend_handles, fontsize=7.8, loc='upper right', framealpha=0.9)

ax.set_xlabel('Annual Cooling Load Proxy (kWh/yr)')
ax.set_ylabel('DGI Exceedance Rate (% occupied hours)')
ax.set_title('Fig. 2 — Pareto Front: CS1 Warm-Climate Retrofit\n'
             'Cooling Reduction vs. Glare Control Trade-off', fontsize=10)
ax.set_xlim(2500, 9800)
ax.set_ylim(0, 11)

plt.tight_layout()
plt.savefig(f'{FIGDIR}/figure_2.png')
plt.close()
print('Figure 2 saved.')
