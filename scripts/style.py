"""Shared academic plot style for all USTA paper figures."""
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

# ── palette ──────────────────────────────────────────────────────────────────
C = {
    'usta':     '#2166AC',   # deep blue   – USTA-Full
    'b1':       '#D73027',   # warm red    – Baseline 1
    'b2':       '#FC8D59',   # amber       – Baseline 2
    'b3':       '#4DAC26',   # green       – Baseline 3
    'b4':       '#762A83',   # purple      – Baseline 4
    'a1':       '#74ADD1',   # light blue  – Ablation 1
    'a2':       '#ABD9E9',   # pale blue   – Ablation 2
    'a3':       '#F46D43',   # orange-red  – Ablation 3
    'outdoor':  '#878787',   # grey        – outdoor / reference
    'comfort':  '#FDAE61',   # pale orange – comfort band fill
    'perez':    '#2166AC',
    'isotropic':'#D73027',
}
MARKER = {'usta': 'o', 'b1': 's', 'b2': '^', 'b4': 'D', 'a1': 'v'}


def set_style():
    mpl.rcParams.update({
        'font.family':      'serif',
        'font.serif':       ['Times New Roman', 'DejaVu Serif'],
        'font.size':        10,
        'axes.titlesize':   11,
        'axes.labelsize':   10,
        'xtick.labelsize':  9,
        'ytick.labelsize':  9,
        'legend.fontsize':  9,
        'lines.linewidth':  1.5,
        'axes.linewidth':   0.8,
        'axes.spines.top':  False,
        'axes.spines.right':False,
        'axes.grid':        True,
        'grid.color':       '#E0E0E0',
        'grid.linewidth':   0.5,
        'figure.dpi':       150,
        'savefig.dpi':      300,
        'savefig.bbox':     'tight',
        'savefig.pad_inches': 0.05,
    })


FIGDIR = '/Users/jcydwx/work/zqr/figures'
