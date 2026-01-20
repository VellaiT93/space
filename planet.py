import math

class Planet:
    def __init__(self, canvas, center_x, center_y, gravity=0.2, rotation_speed=2, z=0):
        self.canvas = canvas
        self.CENTER_X = center_x
        self.CENTER_Y = center_y
        self.GRAVITY = gravity
        self.ROTATION_SPEED = rotation_speed

        # Position in space
        self.x = self.CENTER_X + 200
        self.y = self.CENTER_Y
        self.z = z

        # Velocity (optional, for thrust)
        self.vx = 0
        self.vy = -2
        self.vz = 0

        # Orbit / rotation
        self.radius = 25
        self.orbit_angle = 0
        self.rotation_angle = 0

        # Orbit parameters
        self.orbit_radius = 200
        self.angular_speed = 0.02
        self.vertical_amplitude = 50
        self.vertical_speed = 0.5
        self.max_z = 200

        # Canvas objects
        self.body = canvas.create_oval(0, 0, 0, 0, fill="#4da6ff", outline="")
        self.line = canvas.create_line(0, 0, 0, 0, fill="white")

    def update_canvas(self):
        """Update canvas drawing based on x, y, z using camera"""
        if hasattr(self, 'camera') and self.camera is not None:
            screen_x, screen_y, scale = self.camera.project(self.x, self.y, self.z)
        else:
            # fallback: no camera, use original CENTER_X/Y
            screen_x, screen_y, scale = self.x, self.y, 1

        r = self.radius * scale

        # Planet circle
        self.canvas.coords(
            self.body,
            screen_x - r, screen_y - r,
            screen_x + r, screen_y + r
        )

        # Rotation line
        rad = math.radians(self.rotation_angle)
        lx = screen_x + math.cos(rad) * r
        ly = screen_y + math.sin(rad) * r
        self.canvas.coords(self.line, screen_x, screen_y, lx, ly)

    def update(self):
        """Update orbit and rotation"""
        # Orbit around center
        self.orbit_angle += self.angular_speed
        self.x = self.CENTER_X + math.cos(self.orbit_angle) * self.orbit_radius
        self.z = math.sin(self.orbit_angle) * self.orbit_radius
        self.y = self.CENTER_Y + math.sin(self.orbit_angle * self.vertical_speed) * self.vertical_amplitude

        # Planet rotation
        self.rotation_angle += self.ROTATION_SPEED

        # Update canvas
        self.update_canvas()

    def thrust(self, dx, dy, dz=0):
        self.vx += dx
        self.vy += dy
        self.vz += dz
