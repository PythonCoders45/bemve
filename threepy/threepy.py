from typing import Tuple, Optional
import moderngl
import numpy as np
from PIL import Image

import pygfx as gfx
from wgpu.gui.auto import WgpuCanvas, run


# ============================================================================
# 1. MODERNGL LOW-LEVEL GPU RENDERER
# ============================================================================

class ModernGLCoreRenderer:
    """
    Direct OpenGL GPU shader context using ModernGL.
    Useful for off-screen frame capture directly to image buffers or video frames.
    """

    def __init__(self, width: int = 1920, height: int = 1080):
        self.width = width
        self.height = height
        
        # Create a headless OpenGL context
        self.ctx = moderngl.create_standalone_context()
        self.fbo = self.ctx.framebuffer(
            color_attachments=[self.ctx.texture((width, height), 4)]
        )
        self.fbo.use()

        # Basic GLSL Shader Program mimicking THREE.MeshBasicMaterial
        self.program = self.ctx.program(
            vertex_shader="""
                #version 330
                in vec3 in_position;
                uniform mat4 u_modelViewProjection;
                void main() {
                    gl_Position = u_modelViewProjection * vec4(in_position, 1.0);
                }
            """,
            fragment_shader="""
                #version 330
                uniform vec4 u_color;
                out vec4 fragColor;
                void main() {
                    fragColor = u_color;
                }
            """
        )

    def render_mesh(self, vertices: np.ndarray, indices: np.ndarray, mvp_matrix: np.ndarray, color: Tuple[float, float, float, float]):
        """Renders raw geometry buffers to the ModernGL framebuffer."""
        self.ctx.clear(0.05, 0.05, 0.08, 1.0)
        
        vbo = self.ctx.buffer(vertices.astype('f4').tobytes())
        ibo = self.ctx.buffer(indices.astype('i4').tobytes())
        
        vao = self.ctx.vertex_array(
            self.program,
            [(vbo, '3f', 'in_position')],
            index_buffer=ibo
        )
        
        self.program['u_modelViewProjection'].write(mvp_matrix.astype('f4').tobytes())
        self.program['u_color'].value = color
        vao.render()

    def get_frame_bytes(self) -> bytes:
        """Returns raw RGBA frame buffer bytes for video compilation."""
        return self.fbo.read(components=4)


# ============================================================================
# 2. PYGFX / WGPU THREE.JS-STYLE SCENE ENGINE
# ============================================================================

class ThreePyGFXScene:
    """
    High-level 3D engine mirroring Three.js scene architecture powered by PyGFX and WGPU.
    """

    def __init__(self, width: int = 1280, height: int = 720, offscreen: bool = False):
        self.width = width
        self.height = height
        self.offscreen = offscreen

        # 1. Three.js Scene Setup
        self.scene = gfx.Scene()
        self.camera = gfx.PerspectiveCamera(70, width / height)
        self.camera.position.z = 3.0

        if not offscreen:
            # Interactive window setup using WgpuCanvas
            self.canvas = WgpuCanvas(size=(width, height), title="bemve - ThreePyGFX Engine")
            self.renderer = gfx.renderers.WgpuRenderer(self.canvas)
        else:
            # Headless off-screen renderer for video generation
            self.renderer = gfx.renderers.WgpuRenderer(None, pixel_ratio=1.0)

    def add_box(self, size: Tuple[float, float, float] = (1.0, 1.0, 1.0), color: str = "cyan") -> gfx.Mesh:
        """Creates a THREE.BoxGeometry + THREE.MeshPhongMaterial equivalent."""
        geometry = gfx.box_geometry(*size)
        material = gfx.MeshPhongMaterial(color=color)
        mesh = gfx.Mesh(geometry, material)
        
        # Add lighting if not present
        if not any(isinstance(child, gfx.Light) for child in self.scene.children):
            self.scene.add(gfx.AmbientLight("#ffffff", 0.4))
            dir_light = gfx.DirectionalLight("#ffffff", 0.8)
            dir_light.position.set(5, 5, 5)
            self.scene.add(dir_light)

        self.scene.add(mesh)
        return mesh

    def render_frame(self):
        """Draws a single 3D frame."""
        self.renderer.render(self.scene, self.camera)

    def start_window_loop(self, animate_fn):
        """Starts continuous window rendering with wgpu.gui.auto."""
        if not self.offscreen:
            def draw():
                animate_fn()
                self.renderer.render(self.scene, self.camera)
            
            self.canvas.request_draw(draw)
            run()
