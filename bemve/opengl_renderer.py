import moderngl
import numpy as np


class ModernGLRenderer:

    def __init__(self, width=1280, height=720):
        self.width = width
        self.height = height

        # Initialize headless OpenGL context via GPU
        self.ctx = moderngl.create_standalone_context()

        # Vertex shader: Standard 3D transformation matrix pipeline
        self.prog = self.ctx.program(
            vertex_shader="""
                #version 330
                in vec3 in_position;
                in vec3 in_color;
                out vec3 v_color;
                uniform mat4 mvp;

                void main() {
                    gl_Position = mvp * vec4(in_position, 1.0);
                    v_color = in_color;
                }
            """,
            fragment_shader="""
                #version 330
                in vec3 v_color;
                out vec4 f_color;

                void main() {
                    f_color = vec4(v_color, 1.0);
                }
            """,
        )

        # Offscreen frame buffer object (FBO) for rendering frames
        self.fbo = self.ctx.framebuffer(
            color_attachments=[
                self.ctx.texture((self.width, self.height), 4)
            ]
        )

    def render_mesh(self, vertices: np.ndarray, mvp_matrix: np.ndarray):
        """Renders 3D geometry vertices using GPU acceleration."""
        self.fbo.use()
        self.ctx.clear(0.06, 0.06, 0.07, 1.0)

        # Pass Model-View-Projection matrix to GPU
        self.prog["mvp"].write(mvp_matrix.astype("f4").tobytes())

        vbo = self.ctx.buffer(vertices.astype("f4").tobytes())
        vao = self.ctx.simple_vertex_array(
            self.prog, vbo, "in_position", "in_color"
        )

        vao.render(moderngl.TRIANGLES)

    def get_frame_np() -> np.ndarray:
        """Reads back raw pixels from GPU memory."""
        raw_bytes = self.fbo.color_attachments[0].read()
        frame = np.frombuffer(raw_bytes, dtype=np.uint8).reshape(
            (self.height, self.width, 4)
        )
        return frame[:, :, :3]  # Return RGB