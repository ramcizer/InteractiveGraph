# import required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as st
import matplotlib.colors as mcol
import matplotlib.cm as cm


np.random.seed(12345)

df = pd.DataFrame([np.random.normal(32000, 200000, 3650),
                   np.random.normal(43000, 100000, 3650),
                   np.random.normal(43500, 140000, 3650),
                   np.random.normal(48000, 70000, 3650)],
                  index=[1992, 1993, 1994, 1995])

# calculate and set variables of important values
mean_values = df.mean(axis=1)
std_values = df.std(axis=1)
confidence = 0.95
n = len(df.columns)

# Calculate the full width (entire range) of the confidence interval
intervals = st.t.interval(confidence, n - 1, loc=mean_values, scale=std_values / np.sqrt(n))
full_widths = intervals[1] - intervals[0]

# Create a Normalize object to map mean_values to the range [0, 1]
normalize = mcol.Normalize(vmin=mean_values.min(), vmax=mean_values.max())

# Create a ScalarMappable object using the colormap and the Normalize object
scalarmappable = cm.ScalarMappable(norm=normalize, cmap='viridis')

fig, ax = plt.subplots()

# Plot the bar graph with error bars representing the confidence interval
for i, (mean_val, err_width) in enumerate(zip(mean_values, full_widths / 2)):
    # Get the color corresponding to the mean_value
    color = scalarmappable.to_rgba(mean_val)
    ax.bar(df.index[i], mean_val, yerr=err_width, capsize=10, alpha=0.6, color=color)

# Set the x-axis tick positions and labels
plt.xticks(df.index)
plt.xlabel("Years")

# Add a color bar to show the color scale
cbar = fig.colorbar(scalarmappable, ax=ax)
cbar.set_label('Mean Value')

clicked_positions = []  # Store clicked y-coordinates
lines = []  # Store references to the drawn lines
texts = []  # Store references to the displayed text labels

# Function for the click event to show y-axis value
def onclick(event):
    global clicked_positions, lines, texts

    if event.dblclick:
        # Double-click: Clear all previous drawn lines and their corresponding texts
        for line in lines:
            line.remove()
        lines = []
        for text in texts:
            text.remove()
        texts = []
        for i, (mean_val, err_width) in enumerate(zip(mean_values, full_widths / 2)):
            # Get the color corresponding to the mean_value
            color = scalarmappable.to_rgba(mean_val)
            ax.bar(df.index[i], mean_val, yerr=err_width, capsize=10, alpha=0.6, color=color)
                            

    else:
        if lines == []:
            # Single-click: Draw a line at the clicked y-coordinate and display the value
            clicked_positions.append(event.ydata)
            line = plt.axhline(y=event.ydata, color='black', alpha=0.3)
            text = plt.text(1992, event.ydata, f'Value: {event.ydata:.2f}', color='black', ha='left', va='center')
            lines.append(line)
            texts.append(text)

            # Update the alpha of bars based on the clicked y-coordinate
            for bar in ax.containers:
                for rect in bar:
                    if isinstance(rect, plt.Rectangle):  # Check if it's a rectangle
                        if rect.get_height() <= event.ydata:
                            rect.set_alpha(0.04)

    # Refresh the plot
    fig.canvas.draw()

cid = fig.canvas.mpl_connect('button_press_event', onclick)

plt.show()
cid



