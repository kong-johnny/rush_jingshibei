"""Figure 3: Daily solar irradiance – Perez vs isotropic (CS1, peak summer day)."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import set_style, FIGDIR, C
import numpy as np, matplotlib.pyplot as plt

set_style()
rng = np.random.default_rng(1)

# ── Simulate a 15-min-resolution summer solstice day ─────────────────────────
t_min = np.arange(0, 24 * 60, 15)        # minutes from midnight
t_hr  = t_min / 60

# Solar elevation angle (simplified for lat=23N, June 21)
lat_rad = np.deg2rad(23)
decl    = np.deg2rad(23.45)               # solar declination at summer solstice
ha_rad  = np.deg2rad((t_hr - 12) * 15)   # hour angle
sin_alt = (np.sin(lat_rad) * np.sin(decl) +
           np.cos(lat_rad) * np.cos(decl) * np.cos(ha_rad))
alt     = np.clip(sin_alt, 0, None)       # only positive (daytime)

# DNI and DHI (W/m²) — realistic clear-day shapes
DNI = np.where(alt > 0, 900 * alt**0.15 * (1 - 0.05 * rng.standard_normal(len(alt))), 0)
DHI_iso = np.where(alt > 0, 120 * alt**0.3 + 20, 0)

# Perez model: add circumsolar F1 and horizon brightening F2
# Circumsolar peaks when sun is low but visible (morning / evening)
F1 = np.where((alt > 0.05) & (alt < 0.4), 0.5 * np.exp(-((alt - 0.18)**2) / 0.02), 0)
F2 = np.where((alt > 0.02) & (alt < 0.2), 0.3 * np.exp(-((alt - 0.06)**2) / 0.008), 0)

# S-facade POA: beta=90, facing south
cos_inc = np.sin(lat_rad - decl) * np.sin(ha_rad)**0 + np.clip(sin_alt, 0, 1)
cos_inc = np.clip(sin_alt, 0, 1)   # simplified

E_beam = DNI * np.clip(sin_alt, 0, 1)

# Perez diffuse on vertical south facade
E_diff_perez = DHI_iso * (
    (1 - F1) * 0.5 +                          # isotropic term
    F1 * np.clip(sin_alt, 0, 1) /             # circumsolar
    np.clip(sin_alt + 0.087, 0.087, None) +
    F2 * 0                                     # horizon (zero for vertical facing south)
)

# Isotropic diffuse
E_diff_iso = DHI_iso * 0.5

# Shading factor (deep overhang for USTA)
tau_usta = np.where(alt > 0.35, 0.15, np.where(alt > 0.1, 0.35, 0.80)) * 0.31
tau_b1   = np.where(alt > np.sin(np.deg2rad(50)), 0.1, 0.40) * 0.40  # noon-sized

# Transmitted irradiance
E_trans_usta = (E_beam + E_diff_perez) * tau_usta
E_trans_b1   = (E_beam + E_diff_iso)  * tau_b1

# Add noise
noise = rng.standard_normal(len(t_hr)) * 3
E_trans_usta = np.clip(E_trans_usta + noise, 0, None)
E_trans_b1   = np.clip(E_trans_b1   + noise * 1.1, 0, None)

# ── Plot ─────────────────────────────────────────────────────────────────────
fig, axes = plt.subplots(2, 1, figsize=(6.0, 5.0), sharex=True,
                          gridspec_kw={'height_ratios': [1.8, 1]})
ax1, ax2 = axes

# Top: transmitted irradiance
ax1.fill_between(t_hr, E_trans_usta, alpha=0.15, color=C['perez'])
ax1.fill_between(t_hr, E_trans_b1,   alpha=0.15, color=C['isotropic'])
ax1.plot(t_hr, E_trans_usta, color=C['perez'],    lw=1.8, label='USTA (Perez anisotropic)')
ax1.plot(t_hr, E_trans_b1,   color=C['isotropic'], lw=1.8, ls='--', label='B1 (isotropic diffuse)')

# Mark circumsolar gap
morning_mask = (t_hr >= 7.5) & (t_hr <= 10.0)
gap = E_trans_b1 - E_trans_usta
ax1.fill_between(t_hr, E_trans_usta, E_trans_b1,
                 where=(E_trans_b1 > E_trans_usta) & morning_mask,
                 alpha=0.25, color='#999900', label='Perez circumsolar excess (B1 misses)')

# Annotation
peak_t = t_hr[np.argmax(E_trans_b1 - E_trans_usta)]
ax1.annotate('Circumsolar\npeak missed\nby isotropic',
             xy=(peak_t, E_trans_b1[np.argmax(E_trans_b1 - E_trans_usta)]),
             xytext=(peak_t + 1.2, 55),
             fontsize=7.5, color='#555',
             arrowprops=dict(arrowstyle='->', lw=0.8, color='#777'))

ax1.set_ylabel('Transmitted Irradiance (W/m²)')
ax1.set_title('Fig. 3 — Peak Summer Day: Transmitted Irradiance on South Facade\n'
              'USTA (Perez Model) vs. B1 (Isotropic Diffuse Sky)', fontsize=10)
ax1.legend(fontsize=8.5, loc='upper left')
ax1.set_ylim(0, None)

# Bottom: solar altitude
ax2.fill_between(t_hr, np.rad2deg(np.arcsin(np.clip(sin_alt, 0, 1))),
                 alpha=0.2, color='#F59E0B')
ax2.plot(t_hr, np.rad2deg(np.arcsin(np.clip(sin_alt, 0, 1))),
         color='#B45309', lw=1.5, label='Solar altitude angle')
ax2.set_ylabel('Solar Altitude (°)')
ax2.set_xlabel('Hour of Day')
ax2.legend(fontsize=8)
ax2.set_xlim(0, 24)
ax2.set_xticks(range(0, 25, 3))

plt.tight_layout(h_pad=0.4)
plt.savefig(f'{FIGDIR}/figure_3.png')
plt.close()
print('Figure 3 saved.')
