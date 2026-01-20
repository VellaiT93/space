WIDTH, HEIGHT = 1000, 800
CENTER_X, CENTER_Y = WIDTH // 2, HEIGHT // 2

class Camera:
    def __init__(self, x=0, y=0, z=-500, focal_length=500):
        self.x = x
        self.y = y
        self.z = z
        self.focal_length = focal_length

    def project(self, obj_x, obj_y, obj_z):
        dz = obj_z - self.z
        scale = self.focal_length / (self.focal_length + dz) if (self.focal_length + dz) != 0 else 1
        screen_x = (obj_x - self.x) * scale + CENTER_X
        screen_y = (obj_y - self.y) * scale + CENTER_Y
        return screen_x, screen_y, scale