+------------------+      +-------------------+      +-------------------+
|   Python Scene   | ---> | Pycairo Renderer  | ---> |   Partial Clip    |
|  (User Scripts)  |      | / ModernGL Engine |      |    (.mp4 files)   |
+------------------+      +-------------------+      +-------------------+
|
v
+------------------+      +-------------------+      +-------------------+
|  Browser Preview | <--- |   Final Render    | <--- |  FFmpeg Stitcher  |
|  (Local Server)  |      |  (output.mp4)     |      |   & Audio Sync    |
+------------------+      +-------------------+      +-------------------+


---

## Core Concepts

### 1. `Scene`
The container for your animations. You inherit from `Scene` and override the `construct()` method to define the animation timeline.

### 2. `Mobject` / `VMobject`
Mathematical Objects. `VMobject` represents vector objects constructed using Cubic Bézier curves, allowing smooth shape morphing and path tracing.

### 3. `Animation` & `Transition`
Functions or classes that manipulate object attributes frame-by-frame over a specified duration using interpolation (alpha values from `0.0` to `1.0`).

---

## Modules Reference

### Scene & Rendering
* **`bemve.scene.Scene`**: Handles frame updates, object lists, updaters, caching checks, and rendering pipeline execution.
* **`bemve.cairo_renderer.CairoRenderer`**: Manages the Pycairo drawing context and pixel buffer generation.
* **`bemve.exporter.VideoExporter`**: Handles directory creation, FFmpeg stitching, partial clip tracking, and browser preview.

### Vector Objects (`VMobject`)
* **`bemve.vmobject.VMobject`**: Base class for Bézier vector shapes. Supports linear point interpolation.
* **`bemve.vmobject.VSquare`**: Square constructed with Bézier edge segments.
* **`bemve.vmobject.VCircle`**: Circle built with 4 cubic Bézier splines ($k = 0.55228$).

### Animations & Transitions
* **`bemve.animation.Create`**: Animates path stroke tracing progressively over time.
* **`bemve.animation.Transform`**: Morphs one `VMobject` into another by interpolating control points.
* **`bemve.transition.FadeIn` / `FadeOut`**: Controls opacity fading.
* **`bemve.transition.SlideIn`**: Slides objects onto screen from an offset vector.
* **`bemve.transition.GrowFromCenter`**: Scales an object up from $0\\%$ to $100\\%$.

### Typography & LaTeX
* **`bemve.latex.Tex` / `MathTex`**: Converts math expressions into vector paths for rendering.
* **`bemve.text.Text`**: Text rendering with full `.ttf` / `.otf` font file support.

### Data Charts & 3D Plotting
* **`bemve.charts.AnimatedBarChart`**: Creates growing Seaborn/Matplotlib bar charts.
* **`bemve.charts.Plot3D`**: Renders rotating 3D surface functions ($z = f(x, y)$).

### Camera & Viewport Controls
* **`bemve.camera.Camera`**: Manages viewport transformations, enabling smooth zooming and panning to coordinate points.

### Media Support
* **`bemve.image_mobject.ImageMobject`**: Renders `.png` and `.jpg` raster images with alpha blending.
* **`bemve.video_mobject.VideoMobject`**: Streams video files frame-by-frame into the animation context.

### Caching System
* **`bemve.caching.CacheManager`**: Hashes animation block data (MD5) to skip re-rendering unchanged partial clips.
"""

readme_content = """# Bemve 🎬✨

**Bemve** is a lightweight, modular Python animation engine for creating mathematical, data-driven, and technical videos. Inspired by **Manim** and **Canva**, Bemve gives developers fine-grained vector control, dynamic charts, smooth camera transitions, and instant media rendering.

---

## ✨ Key Features

- 📐 **Vector Bézier Engine (`VMobject`)**: Smooth path tracing (`Create`) and shape morphing (`Transform`).
- 🧮 **LaTeX & Math Expressions (`MathTex`)**: Render mathematical equations cleanly.
- 🔤 **Custom Typography (`Text`)**: Load `.ttf` / `.otf` font files directly.
- 📊 **Animated Data & 3D Graphs (`AnimatedBarChart`, `Plot3D`)**: Seaborn and Matplotlib integration with animated growing bars and rotating 3D surfaces.
- 🎥 **Media Streaming (`ImageMobject`, `VideoMobject`)**: Embed raster images and video clips into vector scenes.
- 🎨 **Canva-Style Transitions (`FadeIn`, `SlideIn`, `GrowFromCenter`)**: Entrances and exits made simple.
- 🎥 **Camera Viewport Control (`Camera`)**: Pan and zoom smooth focus onto coordinate points.
- ⚡ **Smart Hash Caching**: MD5 hashing to reuse rendered partial clips and accelerate build times.
- 🌐 **Instant Browser Preview**: Automatically launches exported MP4 videos in your browser.

---

## 🚀 Quick Start

### 1. Installation

Ensure you have Python 3.9+, **FFmpeg**, and Pycairo installed on your system.

```bash
pip install numpy pycairo imageio matplotlib seaborn
2. Creating Your First Scene
Save the following as example.py:

Python
from bemve import Scene, VSquare, VCircle, MathTex, Text, Create, Transform
from bemve.transition import SlideIn

class QuickDemo(Scene):
    def construct(self):
        # 1. Animated Title
        title = Text("Welcome to Bemve", font_size=0.6, color=(1.0, 0.8, 0.0, 1.0))
        self.play(SlideIn(title, direction=(0.0, -2.0)), duration=1.0)

        # 2. Vector Objects
        square = VSquare(side_length=2.5, stroke_color=(0.0, 0.9, 1.0, 1.0))
        circle = VCircle(radius=1.5, stroke_color=(1.0, 0.2, 0.5, 1.0))

        # 3. Create & Transform
        self.play(Create(square), duration=1.5)
        self.play(Transform(square, circle), duration=1.5)

        # 4. Math Equation
        formula = MathTex(r"e^{i\pi} + 1 = 0", font_size=0.5)
        self.play(Create(formula), duration=1.5)

if __name__ == "__main__":
    scene = QuickDemo(name="QuickDemo")
    scene.render(preview=True)
3. Run the Render
Bash
python example.py
Bemve will render partial clips, stitch them via FFmpeg, and automatically open your video in your web browser!

📁 Directory Structure
.
├── bemve/
│   ├── __init__.py           # Package exports
│   ├── scene.py              # Main Scene engine
│   ├── vmobject.py           # Vector Bézier objects (VCircle, VSquare)
│   ├── animation.py          # Vector animations (Create, Transform)
│   ├── transition.py         # Transitions (FadeIn, SlideIn, GrowFromCenter)
│   ├── camera.py             # Viewport pan & zoom control
│   ├── latex.py              # LaTeX / Math rendering
│   ├── text.py               # Custom TTF font handling
│   ├── charts.py             # Seaborn charts & 3D graphs
│   ├── image_mobject.py      # Image surface support
│   ├── video_mobject.py      # MP4 Video streaming
│   ├── value_tracker.py      # Frame updaters & trackers
│   ├── caching.py            # MD5 hash caching
│   ├── cairo_renderer.py     # Pycairo rendering context
│   └── exporter.py           # FFmpeg clip stitching & browser launch
├── docs/
│   └── DOCUMENTATION.md      # Full architecture & API guide
└── README.md
📜 License
This project is open-source and released under the MIT License. Feel free to modify, expand, and use it for commercial or educational video production!
"""

Write files
with open("README.md", "w", encoding="utf-8") as f:
f.write(readme_content)

os.makedirs("docs", exist_ok=True)
with open("docs/DOCUMENTATION.md", "w", encoding="utf-8") as f:
f.write(docs_content)

print("Files generated successfully!")

Your **`README.md`** and **`docs/DOCUMENTATION.md`** files are ready!

[file-tag: code-generated-file-0-1784833634381108200]
[file-tag: code-generated-file-1-1784833634381126537]

---

### What's Included:

1. **`README.md`**:
   - Project overview, feature breakdown, and installation prerequisites.
   - Quick Start guide with a complete working scene example.
   - Project tree directory structure.
   - MIT License details.

2. **`docs/DOCUMENTATION.md`**:
   - Full architecture diagram showing how scenes flow into Pycairo, FFmpeg partial clip stitching, and browser preview.
   - Comprehensive module reference covering `VMobject`, `Scene`, `Camera`, `AnimatedBarChart`, `Plot3D`, `MathTex`, `Text`, and `Transition`.
