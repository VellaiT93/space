import tkinter as tk
import random
import math
import time

# --- Camera and objects ---
class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 100  # distance for scaling

class Star:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Planet:
    def __init__(self, x, y, radius=20):
        self.x = x
        self.y = y
        self.radius = radius
        self.angle = random.uniform(0, 2*math.pi)
        self.orbit_speed = random.uniform(0.01, 0.03)

    def update(self):
        self.angle += self.orbit_speed
        self.x += math.cos(self.angle) * 0.5
        self.y += math.sin(self.angle) * 0.5

# --- Main Space Game ---
class SpaceGame:
    def __init__(self, root):
        self.root = root
        self.root.title("2D Space Explorer")
        self.root.state("zoomed")  # maximized window with X button

        self.last_time = time.time()
        self.fps = 0

        # Dynamic canvas size
        self.width = self.root.winfo_screenwidth()
        self.height = self.root.winfo_screenheight()
        self.canvas = tk.Canvas(root, width=self.width, height=self.height, bg="black")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Camera
        self.camera = Camera()

        # Axes
        self.show_axes = True

        # Sun in the center
        self.sun_radius = 150

        # Stars (large map)
        self.num_stars = 1000
        self.stars = [Star(random.randint(-5000, 5000), random.randint(-5000, 5000)) for _ in range(self.num_stars)]
        self.star_ids = []

        # Draw stars once and keep IDs
        for star in self.stars:
            sx, sy, scale = self.project(star.x, star.y)
            size = max(1, int(2*scale))
            star_id = self.canvas.create_oval(sx-size, sy-size, sx+size, sy+size, fill="white", outline="")
            self.star_ids.append(star_id)

        # Planets
        self.planets = [Planet(random.randint(-2000, 2000), random.randint(-2000, 2000),
                               radius=random.randint(10, 40)) for _ in range(50)]

        # Bind keys for movement
        self.root.bind("<w>", lambda e: setattr(self.camera, 'y', self.camera.y - 50))
        self.root.bind("<s>", lambda e: setattr(self.camera, 'y', self.camera.y + 50))
        self.root.bind("<a>", lambda e: setattr(self.camera, 'x', self.camera.x - 50))
        self.root.bind("<d>", lambda e: setattr(self.camera, 'x', self.camera.x + 50))
        self.root.bind("<q>", lambda e: setattr(self.camera, 'z', max(10, self.camera.z - 10)))
        self.root.bind("<e>", lambda e: setattr(self.camera, 'z', self.camera.z + 10))
        self.root.bind("<x>", lambda e: self.toggle_axes())
        self.root.bind("<Escape>", lambda e: self.root.destroy())

        # Track last Z to update star size
        self.last_z = self.camera.z

        # Start loop
        self.loop()

    def toggle_axes(self):
        self.show_axes = not self.show_axes

    def project(self, x, y):
        """Project world coordinates to screen coordinates with simple scaling by camera.z"""
        scale = 200 / self.camera.z
        sx = (x - self.camera.x) * scale + self.width / 2
        sy = (y - self.camera.y) * scale + self.height / 2
        return sx, sy, scale

    def loop(self):
        # --- Calculate FPS ---
        current_time = time.time()
        dt = current_time - self.last_time
        if dt > 0:
            self.fps = 1 / dt
        self.last_time = current_time

        # --- Update canvas size ---
        self.width = self.root.winfo_width()
        self.height = self.root.winfo_height()

        # --- Update star positions and size ---
        for i, star in enumerate(self.stars):
            sx, sy, scale = self.project(star.x, star.y)
            size = max(1, int(2*200/self.camera.z))
            self.canvas.coords(self.star_ids[i], sx-size, sy-size, sx+size, sy+size)

        # --- Clear dynamic objects ---
        self.canvas.delete("dynamic")

        # --- Draw sun ---
        sx, sy, scale = self.project(0, 0)
        sun_size = int(self.sun_radius * 200 / self.camera.z)
        self.canvas.create_oval(sx-sun_size, sy-sun_size, sx+sun_size, sy+sun_size,
                                fill="orange", outline="", tags="dynamic")

        # --- Draw planets ---
        for planet in self.planets:
            planet.update()
            sx, sy, scale = self.project(planet.x, planet.y)
            size = max(2, int(planet.radius * 200 / self.camera.z))
            self.canvas.create_oval(sx-size, sy-size, sx+size, sy+size, fill="blue", outline="", tags="dynamic")

        # --- Draw axes ---
        if self.show_axes:
            cx, cy, _ = self.project(0, 0)
            self.canvas.create_line(0, cy, self.width, cy, fill="red", width=2, tags="dynamic")    # X-axis
            self.canvas.create_line(cx, 0, cx, self.height, fill="green", width=2, tags="dynamic")  # Y-axis
            self.canvas.create_line(cx, cy, cx + 100, cy + 100, fill="blue", width=2, tags="dynamic")  # Z-line

        # --- Draw coordinates + FPS ---
        self.canvas.create_text(
            10, 10, anchor="nw", fill="white",
            text=f"X: {int(self.camera.x)}  Y: {int(self.camera.y)}  Z: {int(self.camera.z)}  FPS: {int(self.fps)}",
            font=("Arial", 14), tags="dynamic"
        )

        # --- Schedule next frame ---
        self.root.after(16, self.loop)

if __name__ == "__main__":
    root = tk.Tk()
    game = SpaceGame(root)
    root.mainloop()
