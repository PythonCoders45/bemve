import cairo
import numpy as np


class CairoRenderer:

    def __init__(self, width=1280, height=720):
        self.width = width
        self.height = height

        # Create an image surface in memory (ARGB32)
        self.surface = cairo.ImageSurface(
            cairo.FORMAT_ARGB32, self.width, self.height
        )
        self.ctx = cairo.Context(self.surface)

        # Setup math coordinates: Origin (0,0) at center, scale to fit [-8, 8] x [-4.5, 4.5]
        self.ctx.translate(self.width / 2.0, self.height / 2.0)
        self.scale_factor = self.width / 16.0  # 16 math units wide
        self.ctx.scale(self.scale_factor, -self.scale_factor)  # Flip Y axis

    def clear(self):
        """Clears the background with a dark color."""
        self.ctx.save()
        self.ctx.set_source_rgb(0.06, 0.06, 0.07)  # #0F0F12
        self.ctx.paint()
        self.ctx.restore()

    def draw_circle(
        self, x: float, y: float, radius: float, color=(0.0, 0.9, 1.0, 1.0)
    ):
        """Draws a vector circle with anti-aliasing."""
        self.ctx.save()
        self.ctx.arc(x, y, radius, 0, 2 * np.pi)

        # Stroke border
        r, g, b, a = color
        self.ctx.set_source_rgba(r, g, b, a)
        self.ctx.set_line_width(0.08)  # Vector width in math units
        self.ctx.stroke()
        self.ctx.restore()

    def get_frame_np(self) -> np.ndarray:
        """Converts Cairo surface buffer directly into a NumPy array for video export."""
        buffer = self.surface.get_data()
        frame = np.ndarray(
            shape=(self.height, self.width, 4), dtype=np.uint8, buffer=buffer
        )
        # Cairo stores as BGRA; convert to RGB for video writers
        return frame[:, :, [2, 1, 0]]