import sys
import subprocess
from pathlib import Path

os = sys.platform
folder_name = "bemve"
folder_path = Path(folder_name)
parent_folder = Path("bemve")

sub_video = parent_folder / "video"
sub_fonts = parent_folder / "fonts"
sub_images = parent_folder / "images"
sub_text = parent_folder / "text"

if os = 'linux' or 'darwin':
    if not folder_path.is_dir():
        result = folder_path.mkdir(parents=True, exist_ok=True)
        sub_video.mkdir(parents=True, exist_ok=True)
        sub_images.mkdir(parents=True, exist_ok=True)
        sub_fonts.mkdir(parents=True, exist_ok=True)
        sub_text.mkdir(parents=True, exist_ok=True)
        print(result.stdout)
elif os = 'win32' :
    if not folder_path.is_dir():
        result = folder_path.mkdir(parents=True, exist_ok=True)
        sub_video.mkdir(parents=True, exist_ok=True)
        sub_images.mkdir(parents=True, exist_ok=True)
        sub_fonts.mkdir(parents=True, exist_ok=True)
        sub_text.mkdir(parents=True, exist_ok=True)
        print(result.stdout)