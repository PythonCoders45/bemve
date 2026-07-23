from pathlib import Path
import cairo
import imageio
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


class AnimatedBarChart:
    """Renders a Seaborn/Matplotlib bar chart with growing bars over time."""

    def __init__(
        self,
        categories: list,
        values: list,
        title: str = "Data Chart",
        palette: str = "viridis",
    ):
        self.categories = categories
        self.values = values
        self.title = title
        self.palette = palette

    def render_frame_to_surface(self, progress: float) -> cairo.ImageSurface:
        """Generates a chart frame where bar heights grow according to progress."""
        # Set dark theme for video matching
        plt.style.use("dark_background")
        fig, ax = plt.subplots(figsize=(6, 4), dpi=150)

        # Scale values according to animation progress
        current_values = [v * progress for v in self.values]

        # Draw Seaborn barplot
        sns.barplot(
            x=self.categories,
            y=current_values,
            palette=self.palette,
            ax=ax,
        )
        ax.set_title(self.title, fontsize=14, color="white")
        ax.set_ylim(0, max(self.values) * 1.15)

        # Save temporary buffer to Cairo surface
        fig.canvas.draw()
        rgba_buffer = fig.canvas.buffer_rgba()
        h, w, _ = rgba_buffer.shape

        surface = cairo.ImageSurface.create_for_data(
            np.asarray(rgba_buffer), cairo.FORMAT_ARGB32, w, h
        )
        plt.close(fig)
        return surface


class Plot3D:
    """Renders animated 3D surface functions (e.g. z = sin(x) * cos(y))."""

    def __init__(self, func, x_range=(-3, 3), y_range=(-3, 3), title: str = "3D Surface"):
        self.func = func
        self.x_range = x_range
        self.y_range = y_range
        self.title = title

    def render_surface_frame(self, rotation_angle: float) -> cairo.ImageSurface:
        """Generates a rotating 3D surface plot."""
        plt.style.use("dark_background")
        fig = plt.figure(figsize=(6, 4), dpi=150)
        ax = fig.add_subplot(111, projection="3d")

        X = np.linspace(self.x_range[0], self.x_range[1], 30)
        Y = np.linspace(self.y_range[0], self.y_range[1], 30)
        X, Y = np.meshgrid(X, Y)
        Z = self.func(X, Y)

        # Plot 3D surface
        ax.plot_surface(X, Y, Z, cmap="magma", edgecolor="none", alpha=0.8)
        ax.view_init(elev=30, azim=rotation_angle)
        ax.set_title(self.title, fontsize=12)

        # Buffer to Cairo Surface
        fig.canvas.draw()
        rgba_buffer = fig.canvas.buffer_rgba()
        h, w, _ = rgba_buffer.shape

        surface = cairo.ImageSurface.create_for_data(
            np.asarray(rgba_buffer), cairo.FORMAT_ARGB32, w, h
        )
        plt.close(fig)
        return surface
