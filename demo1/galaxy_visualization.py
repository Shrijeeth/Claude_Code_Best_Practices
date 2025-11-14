#!/usr/bin/env python3
"""
Cool Spiral Galaxy Visualization
A mesmerizing animated visualization of a spiral galaxy with colorful particles
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.colors import LinearSegmentedColormap

# Set up the figure with dark background
plt.style.use('dark_background')
fig, ax = plt.subplots(figsize=(12, 12))
fig.patch.set_facecolor('#000814')
ax.set_facecolor('#000814')

# Generate spiral galaxy data
n_particles = 2000
n_arms = 5

# Initial angle for each particle
theta = np.random.uniform(0, 4 * np.pi, n_particles)
# Assign each particle to a spiral arm
arm_assignment = np.random.randint(0, n_arms, n_particles)

# Distance from center (varies to create depth)
r = np.random.gamma(2, 2, n_particles)

# Add arm offset based on which spiral arm
arm_offset = (2 * np.pi / n_arms) * arm_assignment

# Calculate positions with spiral pattern
def spiral_position(t, theta, r, arm_offset):
    """Calculate spiral galaxy particle positions"""
    spiral_tightness = 0.3
    angle = theta + arm_offset + spiral_tightness * r + t
    x = r * np.cos(angle)
    y = r * np.sin(angle)
    return x, y

# Create custom colormap (blue to purple to pink)
colors = ['#0077b6', '#7209b7', '#f72585', '#ffd60a']
n_bins = 100
cmap = LinearSegmentedColormap.from_list('galaxy', colors, N=n_bins)

# Particle properties
sizes = 50 * (1 / (r + 1)) * np.random.uniform(0.5, 2, n_particles)
particle_colors = cmap(np.random.uniform(0, 1, n_particles))
alpha_values = np.random.uniform(0.3, 1, n_particles)

# Initialize scatter plot
x, y = spiral_position(0, theta, r, arm_offset)
scatter = ax.scatter(x, y, s=sizes, c=particle_colors, alpha=alpha_values, edgecolors='none')

# Add a bright center
center = ax.scatter([0], [0], s=500, c='white', alpha=1, edgecolors='#ffd60a', linewidths=2)

# Configure plot
ax.set_xlim(-15, 15)
ax.set_ylim(-15, 15)
ax.set_aspect('equal')
ax.axis('off')
ax.set_title('Spiral Galaxy Visualization', color='#ffd60a', fontsize=20, pad=20, fontweight='bold')

# Animation function
def animate(frame):
    """Update particle positions for animation"""
    t = frame * 0.02
    x, y = spiral_position(t, theta, r, arm_offset)

    # Update positions
    data = np.c_[x, y]
    scatter.set_offsets(data)

    # Add slight pulsing effect to brightness
    pulse = 0.5 + 0.5 * np.sin(frame * 0.1)
    alpha_variation = alpha_values * (0.7 + 0.3 * pulse)
    scatter.set_alpha(alpha_variation)

    return scatter, center

# Create animation
anim = FuncAnimation(fig, animate, frames=200, interval=50, blit=True, repeat=True)

# Add text
fig.text(0.5, 0.08, 'Press Ctrl+C in terminal to stop',
         ha='center', color='#adb5bd', fontsize=10)

print("🌌 Generating spiral galaxy visualization...")
print("✨ Close the window or press Ctrl+C to exit")

plt.tight_layout()
plt.show()
