import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D  # Import 3D toolkit

fig = plt.figure(figsize=(11, 5))
fig.patch.set_facecolor("black")

axes = [fig.add_subplot(1, 4, i, projection="3d") for i in range(1, 5)]
for ax in axes:
    ax.set_facecolor("black")

x = np.linspace(0, 4 * np.pi, 100)
y1 = np.sin(x)
z1 = np.cos(x)
y2 = np.sin(x + np.pi)
z2 = np.cos(x + np.pi)

# Initialize velocities for bouncing effect
velocities = np.random.uniform(-0.05, 0.05, (4, 3))  # 4 axes, 3 dimensions (x, y, z)


def plot_helix(ax):
    (line1,) = ax.plot(x, y1, z1, color="red")
    (line2,) = ax.plot(x, y2, z2, color="blue")
    inner_lines = [
        ax.plot([x[i], x[i]], [y1[i], y2[i]], [z1[i], z2[i]], color="white", alpha=0.5)[
            0
        ]
        for i in range(len(x))
    ]
    ax.set_ylim(-1, 1)
    ax.set_zlim(-1, 1)
    ax.axis("off")
    return line1, line2, inner_lines


helix_data = [plot_helix(ax) for ax in axes]


def get_rainbow_color(frame, total_frames):
    return plt.cm.hsv(np.linspace(0, 1, total_frames))[int(frame) % total_frames]


def get_cool_color(frame, total_frames):
    return plt.cm.cool(np.linspace(0, 1, total_frames))[int(frame) % total_frames]


def update(frame):
    global velocities
    speed = 0.1 + (frame / 2000.0)
    y1_data = np.sin(x + frame * speed)
    z1_data = np.cos(x + frame * speed)
    y2_data = np.sin(x + np.pi + frame * speed)
    z2_data = np.cos(x + np.pi + frame * speed)

    for idx, (line1, line2, inner_lines) in enumerate(helix_data):
        # Update positions with velocities
        x_new = x + velocities[idx, 0]
        y1_data_new = y1_data + velocities[idx, 1]
        z1_data_new = z1_data + velocities[idx, 2]
        y2_data_new = y2_data + velocities[idx, 1]
        z2_data_new = z2_data + velocities[idx, 2]

        # Bounce off the edges
        if np.any(x_new < 0) or np.any(x_new > 4 * np.pi):
            velocities[idx, 0] *= -1
        if np.any(y1_data_new < -1) or np.any(y1_data_new > 1):
            velocities[idx, 1] *= -1
        if np.any(z1_data_new < -1) or np.any(z1_data_new > 1):
            velocities[idx, 2] *= -1

        line1.set_data(x_new, y1_data_new)
        line1.set_3d_properties(z1_data_new)
        line1.set_color(get_cool_color(frame, 200))

        line2.set_data(x_new, y2_data_new)
        line2.set_3d_properties(z2_data_new)
        line2.set_color(get_cool_color(frame, 200))

        for i in range(len(x)):
            inner_lines[i].set_data(
                [x_new[i], x_new[i]], [y1_data_new[i], y2_data_new[i]]
            )
            inner_lines[i].set_3d_properties([z1_data_new[i], z2_data_new[i]])
            inner_lines[i].set_color(get_cool_color(frame + i, 200))

    for ax in axes:
        ax.view_init(elev=30.0, azim=frame * 0.5)

    return sum(
        [
            (line1, line2) + tuple(inner_lines)
            for line1, line2, inner_lines in helix_data
        ],
        (),
    )


ani = animation.FuncAnimation(fig, update, frames=np.arange(0, 200, 1), blit=True)
ani.save("dna_animation.mp4", writer="ffmpeg", fps=30)
