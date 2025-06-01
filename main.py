import pygame
import sys
import random
from settings import *
from board import PlinkoBoard
from ball import Ball

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Plinko")
font = pygame.font.SysFont("Arial", 24)
FPS = pygame.time.Clock()

board = PlinkoBoard()
balls = []
score = 0

running = True
while running:
    FPS.tick(60)
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            x = WIDTH // 2 + random.uniform(-3, 3)
            balls.append(Ball(x, 100))

    board.draw_pins(screen)
    board.draw_slots(screen, font)
    boardPins = board.get_pins_cordinates()

    for ball in balls[:]:
        ball.draw(screen)
        ball.move(boardPins)

        if ball.is_done():
            index = ball.x // (WIDTH // NUMBER_OF_SLOTS)
            score += SLOT_VALUES[int(index)]
            balls.remove(ball)

    score_text = font.render(f"Bodovi: {score}", True, BLUE)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()


pygame.quit()
sys.exit()
