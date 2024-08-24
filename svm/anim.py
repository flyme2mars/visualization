import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

fig, ax = plt.subplots(
    figsize=(10, 4)
)  # Change the figure size to have more width and less height
fig.patch.set_facecolor("black")  # Set figure background to black
ax.set_facecolor("black")  # Set axes background to black
x = np.linspace(0, 2 * np.pi, 100)
(line,) = ax.plot(x, np.sin(x))  # Remove initial line color

# Create a fill between the sine wave and the x-axis
fill = ax.fill_between(x, np.sin(x), color="blue", alpha=0.3)

ax.axis("off")  # Turn off the axis, its numbers, and ticks


# Define a function to generate rainbow colors
def get_rainbow_color(frame, total_frames):
    colors = plt.cm.hsv(np.linspace(0, 1, total_frames))  # type: ignore
    return colors[int(frame) % total_frames]  # Ensure frame is an integer


def update(frame):
    speed = 0.1 + (frame / 2000.0)  # Start slow and increase speed gradually
    y_data = np.sin(x + np.sin(frame * speed))  # Make the wave oscillate
    line.set_ydata(y_data)  # Update line data
    line.set_color(get_rainbow_color(frame, 200))  # Set line color to rainbow
    global fill  # Declare fill as global to modify it
    fill.remove()  # Remove the old fill
    fill_color = get_rainbow_color(frame, 200)  # Get a rainbow color for the fill
    fill = ax.fill_between(
        x, y_data, color=fill_color, alpha=0.3
    )  # Update the fill with animated color

    # Add a dynamic title that changes with the frame number
    ax.set_title(f"Frame {frame}", color="white", fontsize=15)

    return (line, fill)


ani = animation.FuncAnimation(
    fig, update, frames=np.arange(0, 200, 0.5), blit=True
)  # Increase smoothness by using smaller step size
ani.save(
    "sine_wave_animation.mp4", writer="ffmpeg", fps=60
)  # Save as video with higher fps for smoothness
