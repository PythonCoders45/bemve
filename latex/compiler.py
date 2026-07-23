import os
import hashlib
import subprocess
from pathlib import Path

CACHE_DIR = Path(".bemve_cache/latex")
CACHE_DIR.mkdir(parents=True, exist_ok=True)


class LaTeXCompiler:
    """Compiles LaTeX strings into vector SVGs with strict hash-caching."""

    @staticmethod
    def compile_to_svg(tex_string: str) -> Path:
        # Generate unique hash for cache check
        tex_hash = hashlib.sha256(tex_string.encode('utf-8')).hexdigest()[:16]
        svg_path = CACHE_DIR / f"tex_{tex_hash}.svg"

        if svg_path.exists():
            return svg_path  # Zero-delay cache hit!

        # Complete LaTeX Document
        doc = r"""
        \documentclass[preview]{standalone}
        \usepackage{amsmath}
        \usepackage{amssymb}
        \begin{document}
        """ + tex_string + r"""
        \end{document}
        """

        tex_file = CACHE_DIR / f"temp_{tex_hash}.tex"
        dvi_file = CACHE_DIR / f"temp_{tex_hash}.dvi"

        with open(tex_file, "w") as f:
            f.write(doc)

        try:
            # 1. Compile TeX to DVI
            subprocess.run(
                ["latex", "-interaction=batchmode", f"-output-directory={CACHE_DIR}", str(tex_file)],
                check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
            # 2. Convert DVI to SVG
            subprocess.run(
                ["dvisvgm", "--no-fonts", str(dvi_file), "-o", str(svg_path)],
                check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
        finally:
            # Clean temporary build artifacts
            for ext in [".tex", ".dvi", ".log", ".aux"]:
                f = CACHE_DIR / f"temp_{tex_hash}{ext}"
                if f.exists():
                    os.remove(f)

        return svg_path
