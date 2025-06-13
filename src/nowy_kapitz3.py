import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider, Button
import matplotlib.image as mpimg


# 1. Parametry fizyczne
g     = 9.81
l     = 0.045
A     = 0.016
omega_init = 2 * np.pi * 10.5

# 2. Parametry symulacji i animacji
t_sim    = 5.0
play_dur = 30.0
fps      = 45
N        = int(fps * play_dur)
interval = 1000.0 / fps
t_eval   = np.linspace(0, t_sim, N)

# 3. Równanie ruchu wahadła Kapicy
def kapitsa(t, y, omega):
    phi, phidot = y
    phidd = - (g + A * omega**2 * np.cos(omega * t)) / l * np.sin(phi)
    return [phidot, phidd]

# 4. Warunki początkowe i obliczenie trajektorii
phi0, phidot0 = np.deg2rad(178.0), 0.0
y0 = [phi0, phidot0]

def compute_solution(omega):
    sol = solve_ivp(kapitsa, (0, t_sim), y0, args=(omega,),
                    t_eval=t_eval, method='RK45', rtol=1e-8)
    return sol.t, sol.y[0]

t_vals, phi_t = compute_solution(omega_init)

# Precompute pozycje boba
y_pivot_vals = A * np.cos(omega_init * t_vals)
x_bob_vals   = l * np.sin(phi_t)
y_bob_vals   = y_pivot_vals - l * np.cos(phi_t)

# 5. Przygotowanie figury
fig, ax = plt.subplots(figsize=(6,6))
plt.subplots_adjust(bottom=0.25)

# Ustawienie tła jako zdjęcie
img = mpimg.imread('../media/menu.jpg')
fig.figimage(img, xo=0, yo=0, alpha=0.5, zorder=-1, resize=True)

ax.set_aspect('equal')
ax.set_xlim(-0.10, 0.10)
ax.set_ylim(-0.13, 0.13)
ax.set_title("Wahadło Kapicy BW NG")
ax.set_xlabel("x [m]")
ax.set_ylabel("y [m]")
ax.set_facecolor('#838a85')

trace_line, = ax.plot([], [], color='#c6ceb6', lw=1)
pivot,      = ax.plot([], [], 'ko', ms=8)
rod_line,   = ax.plot([], [], 'k-', lw=2)
bob_dot,    = ax.plot([], [], color='#ffec00', marker='o', ms=12)
time_text   = ax.text(0.02, 0.95, '', transform=ax.transAxes)

# 6. Slider do zmiany omega
ax_omega = plt.axes([0.15, 0.10, 0.6, 0.03])
slider_omega = Slider(ax_omega, 'omega\n[rad/s]', 0.0, 100.0, valinit=omega_init, valstep=0.1)

# 7. Funkcje animacji
def init():
    trace_line.set_data([], [])
    pivot.set_data([], [])
    rod_line.set_data([], [])
    bob_dot.set_data([], [])
    time_text.set_text('')
    return trace_line, pivot, rod_line, bob_dot, time_text

def update(frame):
    # czas fizyczny do obliczeń
    t_phys = t_vals[frame]
    # pozycje
    x_pivot = 0.0
    y_pivot = A * np.cos(slider_omega.val * t_phys)
    x_bob   = x_bob_vals[frame]
    y_bob   = y_bob_vals[frame]
    # ślad
    trace_line.set_data(x_bob_vals[:frame+1], y_bob_vals[:frame+1])
    # wahadło
    pivot.set_data([x_pivot], [y_pivot])
    rod_line.set_data([x_pivot, x_bob], [y_pivot, y_bob])
    bob_dot.set_data([x_bob], [y_bob])
    # równomierny czas animacji
    t_display = frame / fps
    f_display = slider_omega.val / (2 * np.pi)
    time_text.set_text(f"t = {t_display:.2f} s   f = {f_display:.1f} Hz")
    return trace_line, pivot, rod_line, bob_dot, time_text

anim = FuncAnimation(fig, update, frames=N,
                     init_func=init, blit=True,
                     interval=interval)

# 8. Callback suwaka
def on_omega_change(val):
    global omega, t_vals, phi_t, x_bob_vals, y_bob_vals, y_pivot_vals
    omega = slider_omega.val
    t_vals, phi_t = compute_solution(omega)
    y_pivot_vals = A * np.cos(omega * t_vals)
    x_bob_vals   = l * np.sin(phi_t)
    y_bob_vals   = y_pivot_vals - l * np.cos(phi_t)
    # Reset śladu
    trace_line.set_data([], [])
    update(0)

slider_omega.on_changed(on_omega_change)

# 9. Przyciski Pause/Run i Toggle Trace
ax_btn_pause = plt.axes([0.85, 0.1, 0.1, 0.04])
btn_pause    = Button(ax_btn_pause, 'Pause')
paused = False

def on_pause(event):
    global paused
    if paused:
        anim.event_source.start()
        btn_pause.label.set_text('Pause')
    else:
        anim.event_source.stop()
        btn_pause.label.set_text('Run')
    paused = not paused

btn_pause.on_clicked(on_pause)

ax_btn_trace = plt.axes([0.85, 0.15, 0.1, 0.04])
btn_toggle_trace = Button(ax_btn_trace, 'Hide')
show_trace = True

def on_toggle_trace(event):
    global show_trace
    show_trace = not show_trace
    trace_line.set_visible(show_trace)
    btn_toggle_trace.label.set_text('Show' if not show_trace else 'Hide')
    plt.draw()

btn_toggle_trace.on_clicked(on_toggle_trace)

plt.show()