import imageio
import numpy as np
from PIL import Image, ImageDraw


class Scene:

    def __init__(self, width=1280, height=720, fps=30):
        self.width = width
        self.height = height
        self.fps = fps
        self.mobjects = []
        self.camera = Camera3D()
        self.rendered_frames = []

    def add(self, *mobjects):
        for mob in mobjects:
            if mob not in self.mobjects:
                self.mobjects.append(mob)

    def play(self, *animations, rate_func=smooth, duration=1.0):
        total_frames = int(self.fps * duration)
        dt = 1.0 / self.fps

        for anim in animations:
            self.add(anim.mobject)

        for frame in range(total_frames):
            # 1. Calculate Eased Alpha Progress
            raw_t = frame / max(total_frames - 1, 1)
            eased_alpha = rate_func(raw_t)

            # 2. Execute Object Updaters
            for mob in self.mobjects:
                mob.update(dt)

            # 3. Step Animations
            for anim in animations:
                anim.update(eased_alpha)

            # 4. Render Frame
            self.rendered_frames.append(self._render_frame())

    def _render_frame(self):
        image = Image.new("RGB", (self.width, self.height), color="#0F0F12")
        draw = ImageDraw.Draw(image)

        # Draw all active mobjects via camera projection
        for mob in self.mobjects:
            # Map object math points through Camera3D -> Screen Pixels
            proj_x, proj_y = self.camera.project_point(mob.center)
            pixel_x = int((proj_x + 8) / 16 * self.width)
            pixel_y = int((1 - (proj_y + 4.5) / 9) * self.height)

            if mob.opacity > 0:
                draw.ellipse(
                    [pixel_x - 10, pixel_y - 10, pixel_x + 10, pixel_y + 10],
                    fill=mob.color,
                )

        return np.array(image)