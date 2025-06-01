# ball.py
import pygame
import random
import math
from settings import *

class Ball:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.radius = BALL_RADIUS
        self.vx = random.uniform(-0.1, 0.1)
        self.vy = 0
        self.gravity = 0.2

    def move(self, boardPins):
        self.vy += self.gravity
        self.y += self.vy
        self.x += self.vx

        for pin_x, pin_y in boardPins:
            dx = self.x - pin_x
            dy = self.y - pin_y
            distance = (dx ** 2 + dy ** 2) ** 0.5

            if distance < PIN_RADIUS + self.radius:
                # jednostavno odbijanje: preusmjeri brzine
                angle = math.atan2(dy, dx)
                speed = (self.vx ** 2 + self.vy ** 2) ** 0.5
                self.vx = speed * math.cos(angle)
                self.vy = speed * math.sin(angle)
                break  # izbjegni višestruke sudare
            
            if self.x >= (WIDTH - 20) or self.x <= 20: self.vx *= -1


    def draw(self, screen):
        pygame.draw.circle(screen, RED, (self.x, self.y), BALL_RADIUS)

    def is_done(self):
        return self.y >= HEIGHT - 40

