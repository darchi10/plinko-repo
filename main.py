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
balance = 100
insufficient_balance = False

running = True
while running:
    FPS.tick(60)
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN or (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
            if balance - INPUT_AMOUNT < 0:
                insufficient_balance = True
            else:
                x = WIDTH // 2 + random.uniform(-3, 3)
                balls.append(Ball(x, 100))
                balance -= INPUT_AMOUNT

    board.draw_pins(screen)
    board.draw_slots(screen, font)
    boardPins = board.get_pins_cordinates()

    for ball in balls[:]:
        ball.draw(screen)
        ball.move(boardPins)

        if ball.is_done():
            index = ball.x // (WIDTH // NUMBER_OF_SLOTS)
            balance += SLOT_VALUES[int(index)]
            balls.remove(ball)

    balance_text = font.render(f"Balance: {balance}€", True, BLUE)
    screen.blit(balance_text, (10, 10))

    if insufficient_balance and balance < INPUT_AMOUNT:
        screen.blit(font.render("Insufficient balance!", True, RED), (10, 40))

    pygame.display.flip()


pygame.quit()
sys.exit()
