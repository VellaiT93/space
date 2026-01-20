import tkinter as tk
from camera import Camera
from planet import Planet
from starfield import StarField

WIDTH, HEIGHT = 1000, 800
CENTER_X, CENTER_Y = WIDTH // 2, HEIGHT // 2

GRAVITY = 0.2
ROTATION_SPEED = 2

class SpaceGame:
    def __init__(self, root):
        self.root = root
        self.root.title("2.5D Gravity Simulator")

        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black")
        self.canvas.pack()

        # Create camera
        self.camera = Camera()

        # --- Sun in the center (STATIC, screen coordinates) ---
        self.sun_id = self.canvas.create_oval(
            CENTER_X - 30,
            CENTER_Y - 30,
            CENTER_X + 30,
            CENTER_Y + 30,
            fill="orange",
            outline=""
        )

        # --- Add stars in the background ---
        self.stars = StarField(self.canvas, WIDTH, HEIGHT, num_stars=300)

        # --- Draw visible axes ---
        self.axis_x = self.canvas.create_line(
            0, CENTER_Y, WIDTH, CENTER_Y, fill="red", width=2
        )
        self.axis_y = self.canvas.create_line(
            CENTER_X, 0, CENTER_X, HEIGHT, fill="green", width=2
        )
        self.axis_z = self.canvas.create_line(
            CENTER_X, CENTER_Y,
            CENTER_X + 100, CENTER_Y + 100,
            fill="blue", width=2
        )

        # Planet with camera
        self.planet = Planet(
            self.canvas,
            center_x=CENTER_X,
            center_y=CENTER_Y,
            gravity=GRAVITY,
            rotation_speed=ROTATION_SPEED,
            z=0
        )

        self.planet.camera = self.camera  # pass camera to planet

        # --- Camera movement (fixed lambda) ---
        self.root.bind("<w>", lambda e: setattr(self.camera, 'y', self.camera.y - 10))
        self.root.bind("<s>", lambda e: setattr(self.camera, 'y', self.camera.y + 10))
        self.root.bind("<a>", lambda e: setattr(self.camera, 'x', self.camera.x - 10))
        self.root.bind("<d>", lambda e: setattr(self.camera, 'x', self.camera.x + 10))
        self.root.bind("<q>", lambda e: setattr(self.camera, 'z', self.camera.z - 20))
        self.root.bind("<e>", lambda e: setattr(self.camera, 'z', self.camera.z + 20))

        self.loop()

    def loop(self):
        self.planet.update()
        self.stars.update(self.camera)
        self.root.after(16, self.loop)  # ~60 FPS

if __name__ == "__main__":
    root = tk.Tk()
    SpaceGame(root)
    root.mainloop()
