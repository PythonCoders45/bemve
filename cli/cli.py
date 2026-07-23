import argparse
import sys
from pathlib import Path


def main():

    parser = argparse.ArgumentParser(
        prog="bemve",
        description="Bemve Math Animation Engine",
        add_help=False,  
    )

    parser.add_argument(
        "file", type=str, help="Path to the Python file containing the scene"
    )
    parser.add_argument(
        "scene", type=str, help="Name of the Scene class to render"
    )

    parser.add_argument(
        "--help", action="help", help="Show this help message and exit"
    )

    parser.add_argument(
        "-l",
        "--low",
        action="store_true",
        help="Low Quality (480p, 15 FPS) - Fast preview",
    )
    parser.add_argument(
        "-m",
        "--medium",
        action="store_true",
        help="Medium Quality (720p, 30 FPS)",
    )
    parser.add_argument(
        "-h",
        "--high",
        action="store_true",
        help="High Quality (1080p, 60 FPS)",
    )

    parser.add_argument(
        "-p",
        "--preview",
        action="store_true",
        help="Automatically preview output video",
    )

    args = parser.parse_args()

    quality_config = {
        "width": 1920,
        "height": 1080,
        "fps": 60,
    }  

    if args.low:
        quality_config = {"width": 854, "height": 480, "fps": 15}
    elif args.medium:
        quality_config = {"width": 1280, "height": 720, "fps": 30}
    elif args.high:
        quality_config = {"width": 1920, "height": 1080, "fps": 60}

if __name__ == "__main__":
    main()