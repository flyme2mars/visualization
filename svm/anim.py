import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

fig, ax = plt.subplots(
    figsize=(10, 4)
)  # Change the figure size to have more width and less height
fig.patch.set_facecolor("black")  # Set figure background to black
ax.set_facecolor("black")  # Set axes background to black
x = np.linspace(0, 2 * np.pi, 100)
(line,) = ax.plot(x, np.sin(x), color="white")  # Set line color to white

ax.axis("off")  # Turn off the axis, its numbers, and ticks


def update(frame):
    line.set_ydata(np.sin(x + frame / 7.0))  # Increase speed by changing the divisor
    return (line,)


ani = animation.FuncAnimation(
    fig, update, frames=np.arange(0, 200, 0.5), blit=True
)  # Increase smoothness by using smaller step size
ani.save(
    "sine_wave_animation.mp4", writer="ffmpeg", fps=60
)  # Save as video with higher fps for smoothness
