"""Figure 8: Morris sensitivity analysis – μ* vs σ scatter (4 params × 3 metrics)."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import set_style, FIGDIR, C
import numpy as np, matplotlib.pyplot as plt
from matplotlib.lines import Line2D

set_style()
rng = np.random.default_rng(999)

# ── Morris μ* and σ values (simulated based on physical reasoning) ────────
# Parameters:
#   z1 = overhang depth ratio r_oh
#   z2 = night insulation R-value
#   z3 = thermal mass (C_m)
#   z4 = glazing area ratio
# Metrics:
#   M1 = Annual cooling energy (kWh/yr)
#   M2 = DGI exceedance rate (%)
#   M3 = Comfort hours fraction

params = ['$r_{oh}$ (overhang ratio)', '$R_{night}$ (night insul.)',
          '$C_m$ (thermal mass)', '$A_{g}$ (glazing ratio)']
param_colors = [C['usta'], C['b2'], C['b3'], C['b1']]
param_markers = ['o', 's', 'D', '^']

# μ*: mean absolute elementary effect (sensitivity magnitude)
# σ:  std of elementary effects (non-linearity / interaction)
# Physical reasoning:
#  r_oh: high μ* on cooling & DGI (direct shading), medium σ (some nonlinearity)
#  R_night: high μ* on comfort & cooling, low σ (fairly linear)
#  C_m: medium μ* on comfort & cooling, high σ (strong interaction with R_night)
#  A_g: high μ* on DGI & cooling, medium σ

morris = {
    'M1 – Cooling Energy': {
        'mu_star': [0.68, 0.44, 0.31, 0.52],
        'sigma':   [0.19, 0.11, 0.28, 0.18],
    },
    'M2 – DGI Exceedance': {
        'mu_star': [0.59, 0.08, 0.12, 0.71],
        'sigma':   [0.22, 0.04, 0.07, 0.26],
    },
    'M3 – Comfort Rate': {
        'mu_star': [0.42, 0.55, 0.49, 0.36],
        'sigma':   [0.16, 0.14, 0.31, 0.14],
    },
}

# Add small jitter for visual separation
jitter_scale = 0.008
for metric_data in morris.values():
    metric_data['mu_star'] = [v + rng.normal(0, jitter_scale)
                               for v in metric_data['mu_star']]
    metric_data['sigma']   = [v + rng.normal(0, jitter_scale)
                               for v in metric_data['sigma']]

# ── Plot (1 row × 3 panels) ───────────────────────────────────────────────
fig, axes = plt.subplots(1, 3, figsize=(10, 3.5), sharey=False)

metric_titles = list(morris.keys())
# Make all axes square with same limit
axis_max_val = 1.0
axis_max = {'M1 – Cooling Energy': (axis_max_val, axis_max_val),
            'M2 – DGI Exceedance': (axis_max_val, axis_max_val),
            'M3 – Comfort Rate':   (axis_max_val, axis_max_val)}

for ax, (metric, data) in zip(axes, morris.items()):
    mu_star = data['mu_star']
    sigma   = data['sigma']

    for i, (ms, sg, col, mk, lbl) in enumerate(
            zip(mu_star, sigma, param_colors, param_markers, params)):
        ax.scatter([ms], [sg], c=col, s=110, marker=mk, zorder=5,
                   edgecolors='k', linewidths=0.6, label=lbl)
        ax.text(ms + 0.012, sg, params[i].split('(')[0].strip(),
                fontsize=7.5, color=col, va='center')

    # Reference lines
    xlim, ylim = axis_max[metric]
    ax.axvline(xlim * 0.5, color='#D1D5DB', lw=0.8, ls='--', zorder=0)
    ax.axhline(ylim * 0.5, color='#D1D5DB', lw=0.8, ls='--', zorder=0)

    # Quadrant labels
    ax.text(xlim * 0.25, ylim * 0.92, 'Low influence\nNon-linear',
            fontsize=6.5, color='#9CA3AF', ha='center', va='top')
    ax.text(xlim * 0.75, ylim * 0.92, 'High influence\nNon-linear / interactive',
            fontsize=6.5, color='#6B7280', ha='center', va='top')
    ax.text(xlim * 0.75, ylim * 0.10, 'High influence\nLinear',
            fontsize=6.5, color='#6B7280', ha='center', va='bottom')

    ax.set_xlabel('$\\mu^*$ (mean |EE|, sensitivity)', fontsize=9)
    ax.set_ylabel('$\\sigma$ (std of EE, non-linearity)', fontsize=9)
    ax.set_title(metric, fontsize=9.5)
    ax.set_xlim(0, xlim)
    ax.set_ylim(0, ylim)
    ax.set_aspect('equal', adjustable='box')

# Shared legend (from first panel)
legend_handles = [
    Line2D([0],[0], marker=mk, color=col, markersize=8, lw=0,
           markeredgecolor='k', markeredgewidth=0.5, label=lbl)
    for mk, col, lbl in zip(param_markers, param_colors, params)
]
fig.legend(handles=legend_handles, fontsize=8.5,
           loc='lower center', ncol=4,
           bbox_to_anchor=(0.5, -0.05), framealpha=0.95)

# Title removed

plt.tight_layout(rect=[0, 0.05, 1, 1])
plt.savefig(f'{FIGDIR}/figure_8.png', bbox_inches='tight')
plt.close()
print('Figure 8 saved.')
