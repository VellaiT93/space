import random

class StarField:
    def __init__(self, canvas, width, height, num_stars=200):
        self.canvas = canvas
        self.width = width
        self.height = height
        self.num_stars = num_stars
        self.stars = []

        # Create stars with random x, y, z positions and radius
        for _ in range(num_stars):
            x = random.uniform(-width//2, width//2)
            y = random.uniform(-height//2, height//2)
            z = random.uniform(50, 1000)   # depth
            r = random.uniform(0.5, 2.0)
            brightness = random.randint(150, 255)
            color = f'#{brightness:02x}{brightness:02x}{brightness:02x}'
            star_id = canvas.create_oval(0, 0, 0, 0, fill=color, outline="")
            self.stars.append({'id': star_id, 'x': x, 'y': y, 'z': z, 'r': r, 'color': color})

    def update(self, camera):
        """Project stars to screen using camera"""
        for star in self.stars:
            screen_x, screen_y, scale = camera.project(star['x'], star['y'], star['z'])
            r = max(0.2, star['r'] * scale)
            x0, y0 = screen_x - r, screen_y - r
            x1, y1 = screen_x + r, screen_y + r
            self.canvas.coords(star['id'], x0, y0, x1, y1)
