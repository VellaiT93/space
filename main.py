import pygame
import random
import math
import sys

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

# --- Space Game in pygame ---
class SpaceGame:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.fps = 0

        # Fullscreen
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.width, self.height = self.screen.get_size()

        # Camera
        self.camera = Camera()

        # Axes
        self.show_axes = True

        # Sun
        self.sun_radius = 50

        # Stars
        self.num_stars = 1000
        self.stars = [Star(random.randint(-5000, 5000), random.randint(-5000, 5000)) for _ in range(self.num_stars)]

        # Planets
        self.planets = [Planet(random.randint(-2000, 2000), random.randint(-2000, 2000),
                               radius=random.randint(10, 40)) for _ in range(50)]

        # Fonts
        self.font = pygame.font.SysFont("Arial", 24)

        self.run_game()

    def project(self, x, y):
        """Project world coordinates to screen coordinates with simple scaling by camera.z"""
        scale = 200 / self.camera.z
        sx = int((x - self.camera.x) * scale + self.width / 2)
        sy = int((y - self.camera.y) * scale + self.height / 2)
        return sx, sy, scale

    def run_game(self):
        running = True
        while running:
            dt = self.clock.tick(60) / 1000.0
            self.fps = self.clock.get_fps()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if event.key == pygame.K_x:
                        self.show_axes = not self.show_axes

            # --- Handle key states for smooth movement ---
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                self.camera.y -= 500 * dt
            if keys[pygame.K_s]:
                self.camera.y += 500 * dt
            if keys[pygame.K_a]:
                self.camera.x -= 500 * dt
            if keys[pygame.K_d]:
                self.camera.x += 500 * dt
            if keys[pygame.K_q]:
                self.camera.z = max(10, self.camera.z - 200 * dt)
            if keys[pygame.K_e]:
                self.camera.z += 200 * dt

            # --- Draw background ---
            self.screen.fill((0, 0, 0))

            # --- Draw stars ---
            for star in self.stars:
                sx, sy, scale = self.project(star.x, star.y)
                size = max(1, int(2 * 200 / self.camera.z))
                if 0 <= sx < self.width and 0 <= sy < self.height:
                    pygame.draw.circle(self.screen, (255, 255, 255), (sx, sy), size)

            # --- Draw sun ---
            sx, sy, scale = self.project(0, 0)
            sun_size = int(self.sun_radius * 200 / self.camera.z)
            pygame.draw.circle(self.screen, (255, 165, 0), (sx, sy), sun_size)

            # --- Draw planets ---
            for planet in self.planets:
                planet.update()
                sx, sy, scale = self.project(planet.x, planet.y)
                size = max(2, int(planet.radius * 200 / self.camera.z))
                pygame.draw.circle(self.screen, (0, 0, 255), (sx, sy), size)

            # --- Draw axes ---
            if self.show_axes:
                cx, cy, _ = self.project(0, 0)
                pygame.draw.line(self.screen, (255, 0, 0), (0, cy), (self.width, cy), 2)  # X-axis
                pygame.draw.line(self.screen, (0, 255, 0), (cx, 0), (cx, self.height), 2)  # Y-axis
                pygame.draw.line(self.screen, (0, 0, 255), (cx, cy), (cx + 100, cy + 100), 2)  # Z-line

            # --- Draw coordinates + FPS ---
            text = self.font.render(f"X: {int(self.camera.x)} Y: {int(self.camera.y)} Z: {int(self.camera.z)} FPS: {int(self.fps)}", True, (255, 255, 255))
            self.screen.blit(text, (10, 10))

            pygame.display.flip()

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    SpaceGame()
