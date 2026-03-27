"""Figure 6: CS3 MPC vs. reactive control – 7-day dual-panel plot."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from style import set_style, FIGDIR, C
import numpy as np, matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

set_style()
rng = np.random.default_rng(2025)

# ── Simulate 7 summer days at 15-min steps ────────────────────────────────
steps = 7 * 24 * 4   # 672
t_hr  = np.arange(steps) * 0.25

# Outdoor temperature: 25–38°C summer
T_out = (31.5 + 6.5 * np.sin(2 * np.pi * (t_hr - 15) / 24)
         + rng.normal(0, 0.5, steps))

# Occupancy probability (sigmoid transitions)
def occ_profile(hr):
    hr = hr % 24
    return (1 / (1 + np.exp(-3 * (hr - 8.5))) *
            1 / (1 + np.exp( 3 * (hr - 21.5))))

occ = np.array([occ_profile(t) for t in t_hr])

# HVAC cooling capacity (kW) – proportional to temperature error
T_set = 23.0   # setpoint

dt = 0.25
C_a = 80.0    # air thermal capacitance
R_oa = 1.2    # envelope resistance

def simulate_control(T_out, strategy='reactive'):
    T_in  = np.zeros(steps); T_in[0] = 24.5
    theta = np.zeros(steps)   # louver angle (0=closed, 90=open)
    Q_hvac = np.zeros(steps)

    for i in range(1, steps):
        hr   = t_hr[i] % 24
        o_t  = occ[i]
        solar_raw = max(0, 800 * np.sin(np.pi * max(0, hr - 7) / 12)) if 7 < hr < 19 else 0

        if strategy == 'reactive':
            # Reactive: open louvers if glare risk (sun high), HVAC reacts to measured T
            theta[i] = 75 if (solar_raw > 300) else 15
            Q_cool = max(0, min(6.0, 2.5 * (T_in[i-1] - T_set))) * o_t
        else:  # MPC
            # MPC anticipates: pre-close louvers before peak, pre-cool before occupancy surge
            # Anticipatory louver: look 1h ahead
            hr_next = (t_hr[i] + 1.0) % 24
            solar_next = max(0, 800 * np.sin(np.pi * max(0, hr_next - 7) / 12)) if 7 < hr_next < 19 else 0
            if solar_next > 500:
                theta[i] = 10   # pre-close
            elif solar_raw > 200:
                theta[i] = 35
            else:
                theta[i] = 70   # open for ventilation at night

            # Pre-cooling: if temperature will rise due to upcoming occupancy, pre-cool
            occ_ahead = occ_profile(hr + 1.5)
            pre_cool_need = max(0, T_in[i-1] - T_set + occ_ahead * 1.5)
            Q_cool = max(0, min(6.0, 2.0 * (T_in[i-1] - T_set) + 1.2 * pre_cool_need))

        # Solar transmission (depends on louver angle)
        tau = 0.05 + 0.008 * theta[i]
        Q_solar = solar_raw * tau * 8.0 / 1000.0   # kW (8 m² facade)

        # Internal gains
        Q_int = 0.8 + 1.8 * o_t   # kW

        # Thermal update
        dT = dt / C_a * ((T_out[i] - T_in[i-1]) / R_oa + Q_solar + Q_int - Q_cool) * 3600 / 3600
        T_in[i]   = T_in[i-1] + dT
        Q_hvac[i] = Q_cool

    return T_in, theta, Q_hvac

T_mpc,      theta_mpc,      Q_mpc      = simulate_control(T_out, 'mpc')
T_reactive, theta_reactive, Q_reactive = simulate_control(T_out, 'reactive')

# Smooth theta slightly for visual clarity
from numpy import convolve
kernel = np.ones(3) / 3
theta_mpc_s      = convolve(theta_mpc,      kernel, mode='same')
theta_reactive_s = convolve(theta_reactive, kernel, mode='same')

# Comfort metrics
comfort_lo, comfort_hi = 20.0, 26.0
pct_mpc      = np.mean((T_mpc      >= comfort_lo) & (T_mpc      <= comfort_hi)) * 100
pct_reactive = np.mean((T_reactive >= comfort_lo) & (T_reactive <= comfort_hi)) * 100

# Peak cooling demand (rolling 1h max)
from numpy.lib.stride_tricks import sliding_window_view
window = 4  # 1 hour
Q_peak_mpc      = np.max(Q_mpc[window:])
Q_peak_reactive = np.max(Q_reactive[window:])
peak_reduction  = (Q_peak_reactive - Q_peak_mpc) / Q_peak_reactive * 100

# ── Plot ─────────────────────────────────────────────────────────────────────
fig = plt.figure(figsize=(7.5, 5.5))
gs  = gridspec.GridSpec(2, 1, height_ratios=[1, 1.4], hspace=0.35)
ax1 = fig.add_subplot(gs[0])
ax2 = fig.add_subplot(gs[1])

# Panel A: Louver angle
ax1.plot(t_hr, theta_reactive_s, color=C['b2'],  lw=1.4, ls='--', label='Reactive control')
ax1.plot(t_hr, theta_mpc_s,      color=C['usta'], lw=1.8,           label='MPC (anticipatory)')

# Shade afternoons (peak solar)
for day in range(7):
    ax1.axvspan(day*24 + 12, day*24 + 17, alpha=0.07, color='#F59E0B')

ax1.set_ylabel('Louver Angle (°)')
ax1.set_title('Fig. 6 — CS3 MPC vs. Reactive Control: 7-Day Summer Period\n'
              '(a) Louver Angle Schedules', fontsize=10)
ax1.set_xlim(0, 7*24)
ax1.set_xticks(range(0, 7*24+1, 24))
ax1.set_xticklabels([f'Day {i+1}' for i in range(8)], fontsize=8)
ax1.set_ylim(0, 95)
ax1.set_yticks([0, 30, 60, 90])
ax1.legend(fontsize=8, loc='upper right', framealpha=0.9)

# Panel B: Indoor temperature
ax2.fill_between(t_hr, comfort_lo, comfort_hi, alpha=0.10,
                 color=C['usta'], label='_nolegend_')
ax2.axhline(comfort_lo, color='#999', lw=0.7, ls='--')
ax2.axhline(comfort_hi, color='#999', lw=0.7, ls='--')
ax2.text(t_hr[-1]*0.99, comfort_hi + 0.15, 'comfort [20, 26 °C]',
         fontsize=7.5, color='#777', ha='right')

ax2.plot(t_hr, T_out,      color=C['outdoor'], lw=1.1, ls=':',  label='$T_{out}$ – outdoor')
ax2.plot(t_hr, T_reactive, color=C['b2'],      lw=1.4, ls='--',
         label=f'Reactive ({pct_reactive:.1f}% in comfort band)')
ax2.plot(t_hr, T_mpc,      color=C['usta'],    lw=1.8,
         label=f'MPC ({pct_mpc:.1f}% in comfort band)')

ax2.axhline(T_set, color='#6B7280', lw=0.8, ls=':', alpha=0.6)
ax2.text(1, T_set + 0.15, f'setpoint {T_set}°C', fontsize=7.5, color='#6B7280')

# Annotate anticipatory pre-cooling (Day 2 morning)
precool_t = 24 + 6   # ~06:00 Day 2
precool_idx = int(precool_t / 0.25)
ax2.annotate('Anticipatory\npre-cooling',
             xy=(precool_t, T_mpc[precool_idx]),
             xytext=(precool_t - 8, T_mpc[precool_idx] - 2.5),
             fontsize=7.5, color=C['usta'],
             arrowprops=dict(arrowstyle='->', lw=0.9, color=C['usta']))

ax2.set_xlabel('Time (hours from Day 1, 00:00)')
ax2.set_ylabel('Indoor Temperature (°C)')
ax2.set_title('(b) Indoor Temperature Trajectories', fontsize=10)
ax2.legend(fontsize=8, loc='upper right', framealpha=0.9)
ax2.set_xlim(0, 7*24)
ax2.set_xticks(range(0, 7*24+1, 24))
ax2.set_xticklabels([f'Day {i+1}' for i in range(8)], fontsize=8)

# Stats box
stats = (f'MPC vs. Reactive:\n'
         f'  Comfort rate: {pct_mpc:.1f}% vs {pct_reactive:.1f}%\n'
         f'  Peak cooling reduction: {peak_reduction:.1f}%')
ax2.text(0.02, 0.05, stats, transform=ax2.transAxes,
         fontsize=7.5, va='bottom', ha='left',
         bbox=dict(boxstyle='round,pad=0.4', facecolor='white',
                   edgecolor='#ccc', alpha=0.9))

plt.savefig(f'{FIGDIR}/figure_6.png')
plt.close()
print('Figure 6 saved.')
