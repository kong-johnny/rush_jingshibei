"""Figure 5: CS2 72-hour power outage – passive survivability."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import set_style, FIGDIR, C
import numpy as np, matplotlib.pyplot as plt

set_style()
rng = np.random.default_rng(77)

steps = 72 * 4  # 72 hours at 15-min steps
t_hr  = np.arange(steps) * 0.25

# Outdoor temperature: severe cold snap, mid-winter
T_out = (-20 + 6 * np.sin(2 * np.pi * (t_hr - 14) / 24)
         + rng.normal(0, 0.4, steps))

T_safe = 15.0   # survivability threshold

def simulate_outage(T_out, C_a, C_m, R_oa, R_am, night_insul=1.0,
                    T0_in=21.0, T0_m=20.0):
    T_in   = np.zeros(steps); T_in[0]   = T0_in
    T_mass = np.zeros(steps); T_mass[0] = T0_m
    dt = 0.25
    for i in range(1, steps):
        hr = t_hr[i] % 24
        solar = max(0, 20 * np.sin(np.pi * max(0, hr - 9) / 9)) if 9 < hr < 18 else 0
        R_oa_eff = R_oa * night_insul if (hr > 19 or hr < 7) else R_oa
        dTin  = dt / C_a * ((T_out[i] - T_in[i-1]) / R_oa_eff +
                             (T_mass[i-1] - T_in[i-1]) / R_am + 0.45 * solar)
        dTm   = dt / C_m * ((T_in[i-1] - T_mass[i-1]) / R_am + 0.55 * solar)
        T_in[i]   = T_in[i-1]   + dTin
        T_mass[i] = T_mass[i-1] + dTm
    return T_in

T_unretro = simulate_outage(T_out, 120, 600,  0.8, 0.18, night_insul=1.0)
T_b2      = simulate_outage(T_out, 120, 600,  1.8, 0.18, night_insul=1.0)  # better R, no mass surge
T_usta    = simulate_outage(T_out, 120, 2000, 1.8, 0.10, night_insul=3.0)

# Compute survivability hours
survive_unretro = np.sum(T_unretro >= T_safe) / 4  # hours above threshold
survive_b2      = np.sum(T_b2      >= T_safe) / 4
survive_usta    = np.sum(T_usta    >= T_safe) / 4
pct_unretro = survive_unretro / 72 * 100
pct_b2      = survive_b2      / 72 * 100
pct_usta    = survive_usta    / 72 * 100

# ── Plot ─────────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(6.5, 4.0))

# Fill below T_safe
ax.fill_between(t_hr, T_out, T_safe, where=(T_out < T_safe), alpha=0.06, color='#ef4444')
ax.axhline(T_safe, color='#ef4444', lw=1.2, ls='--')
ax.text(1, T_safe + 0.3, f'$T_{{safe}}$ = {T_safe} °C', fontsize=8, color='#ef4444')

ax.fill_between(t_hr, 0, 1, alpha=0.10, color='#BFDBFE', transform=ax.get_xaxis_transform())
ax.text(0.5, 0.02, 'HVAC OFF (outage)', transform=ax.transAxes,
        fontsize=7.5, color='#1E40AF', ha='center')

ax.plot(t_hr, T_out,     color=C['outdoor'], lw=1.2, ls=':',  label='$T_{out}$ – outdoor (-20 to -14 °C)')
ax.plot(t_hr, T_unretro, color=C['b1'],      lw=1.5, ls='-.', label=f'Unretrofitted ({pct_unretro:.0f}% hours above T_safe)')
ax.plot(t_hr, T_b2,      color=C['b2'],      lw=1.5, ls='--', label=f'B2 – Steady-state ({pct_b2:.0f}% hours above T_safe)')
ax.plot(t_hr, T_usta,    color=C['usta'],    lw=2.0,           label=f'USTA-Full ({pct_usta:.0f}% hours above T_safe)')

# Mark when each drops below T_safe
for T_arr, col, lbl in [(T_usta, C['usta'], None),
                         (T_b2,   C['b2'], None),
                         (T_unretro, C['b1'], None)]:
    cross = np.where(np.diff(np.sign(T_arr - T_safe)) < 0)[0]
    if len(cross):
        t_c = t_hr[cross[0]]
        ax.axvline(t_c, color=col, lw=0.8, ls=':', alpha=0.7)
        ax.text(t_c + 0.3, T_safe - 1.5, f'{t_c:.0f} h', fontsize=7, color=col)

ax.set_xlabel('Time after Power Outage (hours)')
ax.set_ylabel('Indoor Temperature (°C)')
ax.set_title('Fig. 5 — CS2 Passive Survivability: 72-Hour Winter Power Outage\n'
             'Indoor Temperature Trajectories and Survivability Fractions', fontsize=10)
ax.legend(fontsize=8, loc='lower left', framealpha=0.9)
ax.set_xlim(0, 72)

# Stats box
stats_text = (f'Survivability (T_in ≥ {T_safe}°C):\n'
              f'  USTA-Full:     {pct_usta:.0f}%\n'
              f'  B2 (SS):       {pct_b2:.0f}%\n'
              f'  Unretrofitted: {pct_unretro:.0f}%')
ax.text(0.98, 0.97, stats_text, transform=ax.transAxes,
        fontsize=8, va='top', ha='right',
        bbox=dict(boxstyle='round,pad=0.4', facecolor='white',
                  edgecolor='#ccc', alpha=0.9))

plt.tight_layout()
plt.savefig(f'{FIGDIR}/figure_5.png')
plt.close()
print('Figure 5 saved.')
