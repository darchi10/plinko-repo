import pygame
import random
import math
from settings import *

class Ball:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.radius = BALL_RADIUS
        self.vx = random.uniform(-0.5, 0.5)
        self.vy = 0
        self.gravity = 0.2
        self.color = RED

    def move(self, boardPins):
        self.vy += self.gravity
        self.y += self.vy
        self.x += self.vx

        for pin_x, pin_y in boardPins:
            dx = self.x - pin_x
            dy = self.y - pin_y
            distance_squared = dx**2 + dy**2
            combined_radii = PIN_RADIUS + self.radius
            combined_radii_squared = combined_radii**2
    
            if distance_squared < combined_radii_squared and distance_squared > 0:
                distance = math.sqrt(distance_squared)
                
                nx = dx / distance
                ny = dy / distance

                overlap = combined_radii - distance
                self.x += overlap * nx
                self.y += overlap * ny
                
                dx_resolved = self.x - pin_x
                dy_resolved = self.y - pin_y
                dist_resolved = math.sqrt(dx_resolved**2 + dy_resolved**2)
                if dist_resolved == 0: continue

                nx_resolved = dx_resolved / dist_resolved
                ny_resolved = dy_resolved / dist_resolved

                dot_product = self.vx * nx_resolved + self.vy * ny_resolved

                v_normal_x = dot_product * nx_resolved
                v_normal_y = dot_product * ny_resolved
                
                v_tangential_x = self.vx - v_normal_x
                v_tangential_y = self.vy - v_normal_y
                
                v_normal_x *= -BOUNCINESS_PIN
                v_normal_y *= -BOUNCINESS_PIN
                
                self.vx = v_normal_x + v_tangential_x
                self.vy = v_normal_y + v_tangential_y

                self.vx += random.uniform(-0.05, 0.05)

        if self.x - self.radius < 0:
            self.x = self.radius
            self.vx *= -BOUNCINESS_WALL
        elif self.x + self.radius > WIDTH:
            self.x = WIDTH - self.radius
            self.vx *= -BOUNCINESS_WALL

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

    def is_done(self):
        return self.y + self.radius >= HEIGHT - 20

