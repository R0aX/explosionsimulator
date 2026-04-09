import pygame
import random
import math

# --- Configuration ---
WIDTH, HEIGHT = 800, 600
FPS = 60

# Colors
BLACK = (10, 10, 10)
WHITE = (255, 255, 255)
ORANGE = (255, 100, 0)
YELLOW = (255, 255, 0)
RED = (200, 0, 0)

class Particle:
    def __init__(self, x, y, scale):
        self.x = x
        self.y = y
        # Scale affects how far and fast particles fly
        angle = random.uniform(0, math.pi * 2)
        speed = random.uniform(2, 10) * scale
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        
        self.radius = random.uniform(2, 6) * scale
        self.life = 1.0  # 1.0 is full life, 0 is dead
        self.decay = random.uniform(0.01, 0.03)
        self.color = random.choice([ORANGE, YELLOW, RED, WHITE])

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vx *= 0.95  # Friction/Air resistance
        self.vy *= 0.95
        self.life -= self.decay
        if self.radius > 0.1:
            self.radius -= 0.05

    def draw(self, surface):
        if self.life > 0:
            # Shift color toward grey/black as it dies
            r = int(self.color[0] * self.life)
            g = int(self.color[1] * self.life)
            b = int(self.color[2] * self.life)
            pygame.draw.circle(surface, (r, g, b), (int(self.x), int(self.y)), int(self.radius))

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pookie's Python Explosion Sim")
    clock = pygame.time.Clock()
    
    particles = []
    current_scale = 5.0
    
    running = True
    while running:
        screen.fill(BLACK)
        
        # Display Instructions
        font = pygame.font.SysFont("Arial", 18)
        img = font.render(f"Press SPACE to Detonate | Scale: {current_scale:.1f} (Up/Down Arrows)", True, WHITE)
        screen.blit(img, (20, 20))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Create a new explosion
                    for _ in range(int(20 * current_scale)):
                        particles.append(Particle(WIDTH//2, HEIGHT//2, current_scale))
                
                # Scale Controls
                if event.key == pygame.K_UP:
                    current_scale = min(current_scale + 0.5, 20.0)
                if event.key == pygame.K_DOWN:
                    current_scale = max(current_scale - 0.5, 1.0)

        # Update and Draw Particles
        for p in particles[:]:
            p.update()
            p.draw(screen)
            if p.life <= 0:
                particles.remove(p)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()