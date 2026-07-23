from pathlib import Path
import cairo
import numpy as np


class ImageMobject:
    """Displays raster images (PNG, JPG) inside the 2D vector scene."""

    def __init__(
        self,
        image_name: str,
        scale: float = 1.0,
        position: tuple[float, float] = (0.0, 0.0),
    ):
        self.image_path = Path("bemve/images") / image_name
        self.scale = scale
        self.position = np.array(position, dtype=float)
        self.surface = None

        if self.image_path.exists():
            # Load PNG image into Cairo surface
            self.surface = cairo.ImageSurface.create_from_png(
                str(self.image_path.resolve())
            )
        else:
            print(f"⚠️ Image file not found: {self.image_path}")

    def draw(self, ctx: cairo.Context, alpha: float = 1.0):
        """Draws and scales the image surface onto Cairo context."""
        if self.surface is None:
            return

        ctx.save()

        # Translate to position
        x, y = self.position
        ctx.translate(x, y)

        # Scale image relative to vector grid
        img_w = self.surface.get_width()
        img_h = self.surface.get_height()

        ctx.scale(
            (self.scale / img_w),
            -(self.scale / img_h),  # Flip Y to match coordinate system
        )

        # Set image surface as source pattern
        ctx.set_source_surface(self.surface, -img_w / 2, -img_h / 2)

        # Paint with alpha transparency support
        ctx.paint_with_alpha(alpha)
        ctx.restore()
