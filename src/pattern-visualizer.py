# Helper script to visualize various scan patterns for the LFI right
# This script will make it easier to plan the scan before actually trying it out on a chip


import matplotlib.pyplot as plt

def zigzag_pattern(x_min, x_max, y_min, y_max, hop):
    direction = 1
    for y in range(y_min, y_max + 1, hop):
        if direction == 1:
            for x in range(x_min, x_max + 1, hop):
                yield (x, y)
        else:
            for x in range(x_max, x_min - 1, -hop):
                yield (x, y)
        direction *= -1

def line_sweep(x_min, x_max, y_min, y_max,  hop):
    # Sweep from left to right
    for x in range(x_min, x_max + 1, hop):
        yield (x, y_min)
    # Sweep from right to left
    for x in range(x_max, x_min - 1, -hop):
        yield (x, y_min)


def spiral_pattern(x_min, x_max, y_min, y_max, step):
    # Calculate center and starting conditions
    x_center, y_center = (x_max + x_min) // 2, (y_max + y_min) // 2
    x, y = x_center, y_center
    dx, dy = 0, -step
    segment_length = step
    segment_passed = 0
    
    # Adjustments to ensure the spiral expands
    while x_min <= x <= x_max and y_min <= y <= y_max:
        yield (x, y)
        # Check if we need to turn
        if segment_passed == segment_length:
            # Turn counter-clockwise
            dx, dy = -dy, dx
            segment_passed = 0
            # Every time we complete two turns, increase the segment length
            if dx == 0:
                segment_length += step
        
        # Move to the next point
        x += dx
        y += dy
        segment_passed += step


def diagonal_zigzag(x_min, x_max, y_min, y_max, hop):
    direction = 1
    for diag in range(0, (x_max - x_min) + (y_max - y_min) + 1, hop):
        x_start = max(x_min, x_max - diag)
        y_start = max(y_min, y_min + diag - (x_max - x_min))
        while x_start <= x_max and y_start <= y_max:
            yield (x_start, y_start)
            x_start += hop
            y_start += hop
        direction *= -1

def plot_pattern(generator, x_min, x_max, y_min, y_max, title, hop):
    x_vals, y_vals = zip(*list(generator(x_min, x_max, y_min, y_max, hop)))
    plt.figure()
    plt.plot(x_vals, y_vals, marker='o')
    plt.title(title)
    plt.xlim([x_min - 1, x_max + 1])
    plt.ylim([y_min - 1, y_max + 1])
    plt.grid(True)

# Define boundaries
x_min, x_max, y_min, y_max, hop = 0, 100, 0, 100, 10


def plot_patterns_together(x_min, x_max, y_min, y_max, step):
    # Create a figure and set of subplots
    fig, axs = plt.subplots(2, 2, figsize=(10, 10))  # Adjust the figure size as needed for clarity

    # Assign patterns to subplots
    patterns = [
        (zigzag_pattern, "Zigzag Pattern", axs[0, 0]),
        (line_sweep, "Line Sweep Pattern", axs[0, 1]),
        (spiral_pattern, "Spiral Pattern", axs[1, 0]),
        (diagonal_zigzag, "Diagonal Zigzag Pattern", axs[1, 1])
    ]

    for generator, title, ax in patterns:
        if title == "Line Sweep Pattern":
            y = (y_min + y_max) // 2  # fixed y-value for line sweep
            x_vals, y_vals = zip(*list(generator(x_min, x_max, y, 0, step)))
        else:
            x_vals, y_vals = zip(*list(generator(x_min, x_max, y_min, y_max, step)))
        
        ax.plot(x_vals, y_vals, marker='o', color='red', markersize=3)
        ax.set_title(title)
        ax.set_xlim([x_min - 1, x_max + 1])
        ax.set_ylim([y_min - 1, y_max + 1])
        ax.grid(False)  # Turn off the grid
        ax.set_xticks([])  # Remove x-axis ticks
        ax.set_yticks([])  # Remove y-axis ticks

    plt.tight_layout(pad=3.0)
    plt.suptitle('Laser Beam Movement Patterns', fontsize=16, color='black', y=1.02) 
    plt.show()

# Define boundaries
x_min, x_max, y_min, y_max, step = 0, 20, 0, 20, 1

# Call the plotting function
plot_patterns_together(x_min, x_max, y_min, y_max, step)
