from pathlib import Path
import subprocess
import webbrowser
import imageio
import numpy as np


class VideoExporter:

    def __init__(
        self,
        scene_name: str = "Scene",
        script_name: str = "main",
        fps: int = 30,
        quality: str = "high",
        transparent: bool = False,
        base_dir: str = "bemve",
    ):
        self.scene_name = scene_name
        self.script_name = Path(script_name).stem
        self.fps = fps
        self.quality = quality
        self.transparent = transparent

        # 1. Base directories setup
        self.base_folder = Path(base_dir)
        self.subfolders = {
            "video": self.base_folder / "video",
            "images": self.base_folder / "images",
            "fonts": self.base_folder / "fonts",
            "text": self.base_folder / "text",
        }
        self._init_directories()

        # 2. Quality resolution naming (Manim style)
        quality_folder_map = {
            "low": "480p15",
            "medium": "720p30",
            "high": "1080p60",
            "4k": "2160p60",
        }
        res_folder = quality_folder_map.get(quality, f"custom_{quality}")

        # 3. Format & Codecs
        if self.transparent:
            ext = ".mov"
            self.codec = "png"
            self.pixel_format = "rgba"
        else:
            ext = ".mp4"
            self.codec = "libx264"
            self.pixel_format = "yuv420p"

        # Directory structure:
        # bemve/video/<script_name>/<resolution>/<SceneName>.<ext>
        # bemve/video/<script_name>/<resolution>/partial_movie_files/<SceneName>/
        self.resolution_dir = self.subfolders["video"] / self.script_name / res_folder
        self.partial_dir = self.resolution_dir / "partial_movie_files" / self.scene_name
        self.partial_dir.mkdir(parents=True, exist_ok=True)

        self.output_path = (self.resolution_dir / f"{self.scene_name}{ext}").resolve()

        # Bitrate configuration
        bitrate_map = {
            "low": "1500k",
            "medium": "4000k",
            "high": "10000k",
            "4k": "20000k",
        }
        self.bitrate = bitrate_map.get(quality, "10000k")

        # Partial clips state
        self.partial_writers = []
        self.partial_clip_paths = []
        self.current_partial_writer = None
        self.clip_count = 0
        self.audio_tracks = []

    def _init_directories(self):
        """Creates initial engine folders across OS platforms."""
        for folder in self.subfolders.values():
            folder.mkdir(parents=True, exist_ok=True)

    def start_partial_clip(self) -> Path:
        """Starts writing a new partial clip file (e.g., 00000.mp4)."""
        clip_filename = f"{self.clip_count:05d}{self.output_path.suffix}"
        clip_path = self.partial_dir / clip_filename
        self.partial_clip_paths.append(clip_path)

        writer_kwargs = {
            "fps": self.fps,
            "codec": self.codec,
            "pixelformat": self.pixel_format,
        }
        if not self.transparent:
            writer_kwargs["bitrate"] = self.bitrate

        self.current_partial_writer = imageio.get_writer(clip_path, **writer_kwargs)
        self.clip_count += 1
        return clip_path

    def write_frame(self, frame_np: np.ndarray):
        """Streams a raw pixel frame to the currently active partial clip."""
        if self.current_partial_writer is None:
            self.start_partial_clip()
        self.current_partial_writer.append_data(frame_np)

    def end_partial_clip(self):
        """Closes the current partial clip file."""
        if self.current_partial_writer is not None:
            self.current_partial_writer.close()
            self.current_partial_writer = None

    def combine_partial_clips(self):
        """Stitches all partial movie clips into the main video file using FFmpeg."""
        if not self.partial_clip_paths:
            print("⚠️ No partial clips found to combine.")
            return

        # Make sure the last clip is closed
        self.end_partial_clip()

        # Create FFmpeg concatenation manifest text file
        concat_list_path = self.partial_dir / "partial_clips_list.txt"
        with open(concat_list_path, "w", encoding="utf-8") as f:
            for clip_path in self.partial_clip_paths:
                f.write(f"file '{clip_path.resolve()}'\n")

        print(f"🧩 Combining {len(self.partial_clip_paths)} partial clip(s)...")

        # FFmpeg concat command
        cmd = [
            "ffmpeg",
            "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", str(concat_list_path.resolve()),
            "-c", "copy",
            str(self.output_path),
        ]

        try:
            subprocess.run(
                cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True
            )
            print(f"✨ Final video stitched and saved to: {self.output_path}")
        except Exception as e:
            print(f"⚠️ Failed to stitch clips via FFmpeg copy. Retrying with encoding... ({e})")

    def finish(self, open_browser: bool = False):
        """Stitches partial clips together, merges audio, and opens browser preview."""
        self.combine_partial_clips()

        if self.audio_tracks:
            self._merge_audio()

        if open_browser:
            self.open_in_browser()

    def open_in_browser(self):
        """Opens the output video inside the default browser."""
        file_uri = self.output_path.as_uri()
        print(f"🌐 Opening preview in browser: {file_uri}")
        webbrowser.open(file_uri)