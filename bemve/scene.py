import cairo
from pathlib import Path
from bemve.cairo_renderer import CairoRenderer
from bemve.exporter import VideoExporter
from bemve.caching import CacheManager


class Scene:

    def __init__(
        self,
        name: str = "Scene",
        fps: int = 60,
        quality: str = "high",
        use_cache: bool = True,
    ):
        self.name = name
        self.fps = fps
        self.quality = quality
        self.use_cache = use_cache

        self.width = 1920 if quality == "high" else 1280
        self.height = 1080 if quality == "high" else 720

        self.renderer = CairoRenderer(width=self.width, height=self.height)
        self.exporter = VideoExporter(
            scene_name=self.name,
            script_name=__file__,
            fps=self.fps,
            quality=self.quality,
        )
        self.mobjects = []
        self.updaters = []  # List of functions: func(dt)

    def add(self, *mobjects):
        for mob in mobjects:
            if mob not in self.mobjects:
                self.mobjects.append(mob)

    def add_updater(self, updater_func):
        """Adds a continuous frame updater function."""
        if updater_func not in self.updaters:
            self.updaters.append(updater_func)

    def remove_updater(self, updater_func):
        if updater_func in self.updaters:
            self.updaters.remove(updater_func)

    def play(self, *animations, duration: float = 1.0):
        """Renders an animation block or reuses cached partial clip if available."""
        dt = 1.0 / self.fps
        total_frames = int(self.fps * duration)

        # 1. Generate hash for this play call
        anim_repr = "".join([str(a.__class__.__name__) for a in animations])
        cache_hash = CacheManager.compute_hash(anim_repr, str(total_frames), self.name)
        
        # Determine partial clip destination
        clip_filename = f"clip_{cache_hash}{self.exporter.output_path.suffix}"
        clip_path = self.exporter.partial_dir / clip_filename

        # 2. Check if cached version exists
        if self.use_cache and CacheManager.is_cached(clip_path):
            print(f"⚡ Using cached clip: {clip_filename}")
            self.exporter.partial_clip_paths.append(clip_path)
            # Advance tracker animation state to target
            for anim in animations:
                anim.update(1.0)
            return

        # 3. Render fresh frames if not cached
        print(f"🎬 Rendering new clip: {clip_filename}")
        self.exporter.start_partial_clip_path(clip_path)

        for frame_idx in range(total_frames):
            alpha = frame_idx / max(total_frames - 1, 1)

            # Execute scene updaters
            for updater in self.updaters:
                updater(dt)

            # Clear context
            self.renderer.clear()

            # Update and draw animations
            for anim in animations:
                anim.update(self.renderer.ctx, alpha)

            # Stream frame buffer
            rgb_frame = self.renderer.get_frame_np()
            self.exporter.write_frame(rgb_frame)

        self.exporter.end_partial_clip()

    def construct(self):
        pass

    def render(self, preview: bool = False):
        self.construct()
        self.exporter.finish(open_browser=preview)
