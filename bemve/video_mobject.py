from pathlib import Path
import cairo
import imageio
import numpy as np


class VideoMobject:
    """Streams video file frames (MP4, MOV) inside the 2D vector scene."""

    def __init__(
        self,
        video_name: str,
        scale: float = 2.0,
        position: tuple[float, float] = (0.0, 0.0),
    ):
        self.video_path = Path("bemve/video") / video_name
        self.scale = scale
        self.position = np.array(position, dtype=float)
        self.reader = None

        if self.video_path.exists():
            # Open video reader
            self.reader = imageio.get_reader(str(self.video_path.resolve()))
        else:
            print(f"⚠️ Video file not found: {self.video_path}")

    def draw_frame(self, ctx: cairo.Context, frame_index: int, alpha: float = 1.0):
        """Extracts a frame by index and paints it to Cairo context."""
        if self.reader is None:
            return

        try:
            # Read RGB frame from video stream
            rgb_frame = self.reader.get_data(frame_index)
            h, w, _ = rgb_frame.shape

            # Convert RGB array to Cairo ARGB32 surface
            bgra = np.zeros((h, w, 4), dtype=np.uint8)
            bgra[:, :, 0] = rgb_frame[:, :, 2]  # B
            bgra[:, :, 1] = rgb_frame[:, :, 1]  # G
            bgra[:, :, 2] = rgb_frame[:, :, 0]  # R
            bgra[:, :, 3] = 255                 # A

            surface = cairo.ImageSurface.create_for_data(
                bgra, cairo.FORMAT_ARGB32, w, h
            )

            ctx.save()
            x, y = self.position
            ctx.translate(x, y)

            # Scale to fit canvas coordinates
            ctx.scale(self.scale / w, -(self.scale / h))
            ctx.set_source_surface(surface, -w / 2, -h / 2)
            ctx.paint_with_alpha(alpha)
            ctx.restore()

        except Exception as e:
            print(f"⚠️ Failed to render video frame {frame_index}: {e}")

    def close(self):
        if self.reader is not None:
            self.reader.close()
