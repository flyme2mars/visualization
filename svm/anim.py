import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D  # Import 3D toolkit

# Create a figure and 3D axis with a black background
fig = plt.figure(figsize=(10, 4))
fig.patch.set_facecolor("black")
ax = fig.add_subplot(111, projection="3d")
ax.set_facecolor("black")

# Generate data for the DNA double helix
x = np.linspace(0, 4 * np.pi, 100)
y1 = np.sin(x)
z1 = np.cos(x)
y2 = np.sin(x + np.pi)
z2 = np.cos(x + np.pi)

# Plot the initial lines for the double helix
(line1,) = ax.plot(x, y1, z1, color="red")
(line2,) = ax.plot(x, y2, z2, color="blue")

# Plot the inner lines across the strands
inner_lines = []
for i in range(len(x)):
    (line,) = ax.plot(
        [x[i], x[i]], [y1[i], y2[i]], [z1[i], z2[i]], color="white", alpha=0.5
    )
    inner_lines.append(line)

# Turn off the axis
ax.axis("off")


# Function to generate rainbow colors
def get_rainbow_color(frame, total_frames):
    colors = plt.cm.hsv(np.linspace(0, 1, total_frames))  # type: ignore
    return colors[int(frame) % total_frames]


# Update function for animation
def update(frame):
    speed = 0.1 + (frame / 2000.0)
    y1_data = np.sin(x + frame * speed)
    z1_data = np.cos(x + frame * speed)
    y2_data = np.sin(x + np.pi + frame * speed)
    z2_data = np.cos(x + np.pi + frame * speed)

    line1.set_data(x, y1_data)
    line1.set_3d_properties(z1_data)
    line1.set_color(get_rainbow_color(frame, 200))

    line2.set_data(x, y2_data)
    line2.set_3d_properties(z2_data)
    line2.set_color(get_rainbow_color(frame, 200))

    # Update the inner lines across the strands
    for i in range(len(x)):
        inner_lines[i].set_data([x[i], x[i]], [y1_data[i], y2_data[i]])
        inner_lines[i].set_3d_properties([z1_data[i], z2_data[i]])
        inner_lines[i].set_color(get_rainbow_color(frame + i, 200))  # Add color effect

    ax.set_title(f"Frame {frame}", color="white", fontsize=15)

    # Rotate the view for 3D effect
    ax.view_init(elev=30.0, azim=frame * 0.5)

    return (line1, line2) + tuple(inner_lines)


# Create and save the animation
ani = animation.FuncAnimation(fig, update, frames=np.arange(0, 200, 1), blit=True)
ani.save("dna_animation.mp4", writer="ffmpeg", fps=30)
