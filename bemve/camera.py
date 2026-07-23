import numpy as np
import cairo

class Camera3D:

    def __init__(self, focal_length=5.0):
        self.focal_length = focal_length
        self.phi = 0.0  # Latitude angle
        self.theta = 0.0  # Longitude angle

    def set_rotation(self, phi: float, theta: float):
        self.phi = phi
        self.theta = theta

    def project_point(self, point_3d: np.ndarray) -> tuple[float, float]:
        """Applies 3D pitch/yaw rotation matrices and perspective projection."""
        x, y, z = point_3d

        # 1. Rotation Matrix (Yaw - Theta)
        cos_t, sin_t = np.cos(self.theta), np.sin(self.theta)
        x1 = cos_t * x - sin_t * y
        y1 = sin_t * x + cos_t * y

        # 2. Rotation Matrix (Pitch - Phi)
        cos_p, sin_p = np.cos(self.phi), np.sin(self.phi)
        y2 = cos_p * y1 - sin_p * z
        z2 = sin_p * y1 + cos_p * z

        # 3. Perspective Projection
        distance = self.focal_length + z2
        scale = self.focal_length / max(distance, 0.1)

        return (x1 * scale, y2 * scale)

class Camera:
    """Manages the viewport offset and zoom level."""

    def __init__(self, width: int = 1920, height: int = 1080):
        self.width = width
        self.height = height
        self.center = np.array([0.0, 0.0])  # Look-at point (X, Y)
        self.zoom = 1.0                     # 1.0 = Default, 2.0 = 2x Zoomed in

    def look_at(self, x: float, y: float):
        """Sets the camera focus point."""
        self.center = np.array([x, y], dtype=float)

    def set_zoom(self, zoom_factor: float):
        """Sets the zoom magnification level."""
        self.zoom = max(0.01, float(zoom_factor))

    def apply_transform(self, ctx: cairo.Context):
        """Applies the camera zoom and pan transform to the Cairo context."""
        ctx.save()
        # Move origin to screen center
        ctx.translate(self.width / 2.0, self.height / 2.0)
        
        # Apply zoom scaling
        ctx.scale(self.zoom, self.zoom)

        # Pan to camera center point
        ctx.translate(-self.center[0], -self.center[1])
