from pathlib import Path

# --- 1. Version & Metadata ---
__version__ = "0.1.0"
__author__ = "Bemve Community"

# --- 2. Exporter Subsystem ---
from bemve.exporter import VideoExporter

# --- 3. Graphics & Rendering Subsystems ---
from bemve.cairo_renderer import CairoRenderer

from bemve.animation import Create, Transform

try:
    from bemve.opengl_renderer import ModernGLRenderer
except ImportError:
    # ModernGL is optional if running in pure 2D vector mode
    ModernGLRenderer = None

# --- 4. Math & Geometry Subsystems ---
try:
    from bemve.mobject import Mobject, Circle
except ImportError:
    pass

try:
    from bemve.geometry import Axes, FunctionGraph
except ImportError:
    pass

try:
    from bemve.rate_functions import linear, smooth, there_and_back, bounce
except ImportError:
    pass

# --- 5. Scene Engine ---
try:
    from bemve.scene import Scene
except ImportError:
    pass

# --- 6. Explicit Exports (__all__) ---
# Defines what gets imported when a user types `from bemve import *`
__all__ = [
    # Engine Meta
    "__version__",
    # Core Exporter
    "VideoExporter",
    # Renderers
    "CairoRenderer",
    "ModernGLRenderer",
    # Core Objects & Scenes
    "Mobject",
    "Circle",
    "Axes",
    "FunctionGraph",
    "Scene",
    # Easing Functions
    "linear",
    "smooth",
    "there_and_back",
    "bounce",
    "Create",
    "Transform"
]
