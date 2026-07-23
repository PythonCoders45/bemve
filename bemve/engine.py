from pathlib import Path
import imageio
import numpy as np
from PIL import Image, ImageDraw


class Vector2D:

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y


class Canvas:
    """Handles translating math coordinates into screen pixel coordinates."""

    def __init__(self, width=1920, height=1080, x_range=(-8, 8), y_range=(-4.5, 4.5)):
        self.width = width
        self.height = height
        self.x_min, self.x_max = x_range
        self.y_min, self.y_max = y_range

    def math_to_pixel(self, point: tuple[float, float]) -> tuple[int, int]:
        """Converts mathematical coordinates (x, y) to image pixel coordinates (px_x, px_y)."""
        x, y = point

        # Normalize x and y to range [0, 1]
        norm_x = (x - self.x_min) / (self.x_max - self.x_min)
        norm_y = (y - self.y_min) / (self.y_max - self.y_min)

        # Convert to screen space (Y-axis is flipped in screen space)
        pixel_x = int(norm_x * self.width)
        pixel_y = int((1 - norm_y) * self.height)

        return pixel_x, pixel_y


class Renderer:

    def __init__(self, width=1280, height=720, fps=30):
        self.width = width
        self.height = height
        self.fps = fps
        self.canvas = Canvas(width=width, height=height)

    def draw_circle(
        self,
        draw: ImageDraw.ImageDraw,
        center: tuple[float, float],
        radius: float,
        color="cyan",
        fill=None,
    ):
        """Draws a circle using math coordinates."""
        cx, cy = center
        # Calculate bounding box in math space
        p1 = self.canvas.math_to_pixel((cx - radius, cy - radius))
        p2 = self.canvas.math_to_pixel((cx + radius, cy + radius))

        draw.ellipse([p1, p2], outline=color, fill=fill, width=4)

    def draw_line(
        self,
        draw: ImageDraw.ImageDraw,
        start: tuple[float, float],
        end: tuple[float, float],
        color="white",
        width=3,
    ):
        """Draws a vector line using math coordinates."""
        p1 = self.canvas.math_to_pixel(start)
        p2 = self.canvas.math_to_pixel(end)
        draw.line([p1, p2], fill=color, width=width)


class Scene:

    def __init__(self, width=1280, height=720, fps=30):
        self.renderer = Renderer(width, height, fps)
        self.duration = 3.0  # Default 3 seconds
        self.frames = []

    def construct(self):
        """Override this method in your own scene scripts!"""
        pass

    def render(self, output_filename="output.mp4"):
        total_frames = int(self.renderer.fps * self.duration)
        print(
            f"🎬 Rendering {total_frames} frames ({self.renderer.fps} FPS)..."
        )

        writer = imageio.get_writer(
            output_filename, fps=self.renderer.fps, codec="libx264"
        )

        for frame_idx in range(total_frames):
            # Alpha parameter ranging from 0.0 to 1.0 representing timeline progress
            alpha = frame_idx / max(total_frames - 1, 1)

            # Create a dark background image
            image = Image.new(
                "RGB",
                (self.renderer.width, self.renderer.height),
                color="#0f0f12",
            )
            draw = ImageDraw.Draw(image)

            # Draw the current frame state
            self.draw_frame(draw, alpha)

            # Convert PIL Image to Numpy array for imageio
            frame_data = np.array(image)
            writer.append_data(frame_data)

        writer.close()
        print(f"✨ Video saved as '{output_filename}'!")

    def draw_frame(self, draw: ImageDraw.ImageDraw, alpha: float):
        """Override or animate items here using the timeline alpha (0.0 -> 1.0)."""
        pass