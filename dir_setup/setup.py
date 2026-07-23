from pathlib import Path
base_folder = Path("bemve")
subfolders = [
    base_folder / "video",
    base_folder / "fonts",
    base_folder / "images",
    base_folder / "text",
]
for folder in subfolders:
    folder.mkdir(parents=True, exist_ok=True)