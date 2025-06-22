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

balls = []
balance = 100
insufficient_balance = False

reset_button_rect = pygame.Rect(WIDTH - 150, 20, 120, 40)
exit_button_rect = pygame.Rect(WIDTH - 150, 70, 120, 40)

board = PlinkoBoard(reset_button_rect, exit_button_rect)

SLIDER_TRACK_Y = 50
SLIDER_TRACK_X = 80
SLIDER_TRACK_WIDTH = 150
SLIDER_TRACK_HEIGHT = 10
SLIDER_HANDLE_WIDTH = 8
SLIDER_HANDLE_HEIGHT = 20
DISABLED_COLOR = (180, 180, 180)

slider_track_rect = pygame.Rect(SLIDER_TRACK_X, SLIDER_TRACK_Y, SLIDER_TRACK_WIDTH, SLIDER_TRACK_HEIGHT)
slider_handle_rect = pygame.Rect(0, SLIDER_TRACK_Y - (SLIDER_HANDLE_HEIGHT - SLIDER_TRACK_HEIGHT) // 2, SLIDER_HANDLE_WIDTH, SLIDER_HANDLE_HEIGHT)

dragging_slider = False

initial_stake_from_settings = INPUT_AMOUNT
original_slot_values = list(SLOT_VALUES)

current_stake = initial_stake_from_settings
current_slot_values = list(original_slot_values)

def update_handle_position_from_stake():
    if MAX_STAKE == MIN_STAKE:
        percentage = 0
    else:
        percentage = (current_stake - MIN_STAKE) / (MAX_STAKE - MIN_STAKE)
    handle_x = slider_track_rect.left + percentage * slider_track_rect.width
    slider_handle_rect.centerx = handle_x

def update_stake_from_handle_position():
    global current_stake
    if slider_track_rect.width == 0:
        stake = MIN_STAKE
    else:
        percentage = (slider_handle_rect.centerx - slider_track_rect.left) / slider_track_rect.width
        stake = MIN_STAKE + percentage * (MAX_STAKE - MIN_STAKE)
    current_stake = max(MIN_STAKE, min(MAX_STAKE, round(stake)))
    update_handle_position_from_stake()

def update_slot_values():
    global current_slot_values
    ratio = current_stake / initial_stake_from_settings
    current_slot_values = [int(value * ratio) for value in original_slot_values]

update_handle_position_from_stake()
update_slot_values()

running = True
while running:
    FPS.tick(60)
    screen.fill(BLACK)

    slider_disabled = len(balls) > 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if not slider_disabled and slider_handle_rect.collidepoint(mouse_pos):
                dragging_slider = True
            elif reset_button_rect.collidepoint(mouse_pos):
                balance = 100
                balls.clear()
            elif exit_button_rect.collidepoint(mouse_pos):
                running = False
            elif balance - current_stake < 0:
                insufficient_balance = True
            else:
                x = WIDTH // 2 + random.uniform(-3, 3)
                balls.append(Ball(x, 100))
                balance -= current_stake
                insufficient_balance = False

        elif event.type == pygame.MOUSEBUTTONUP:
            if dragging_slider:
                dragging_slider = False

        elif event.type == pygame.MOUSEMOTION:
            if dragging_slider and not slider_disabled:
                mouse_x = event.pos[0]
                slider_handle_rect.centerx = max(slider_track_rect.left, min(mouse_x, slider_track_rect.right))
                update_stake_from_handle_position()
                update_slot_values()

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if balance - current_stake < 0: 
                insufficient_balance = True
            else:
                x = WIDTH // 2 + random.uniform(-3, 3)
                balls.append(Ball(x, 100))
                balance -= current_stake
                insufficient_balance = False


    board.draw_pins(screen)
    board.draw_slots(screen, font, current_slot_values) 
    boardPins = board.get_pins_cordinates()

    for ball in balls[:]:
        ball.draw(screen)
        ball.move(boardPins)

        if ball.is_done():
            slot_index_float = ball.x / (WIDTH // NUMBER_OF_SLOTS)
            slot_index = max(0, min(NUMBER_OF_SLOTS - 1, int(slot_index_float)))
            balance += current_slot_values[slot_index]
            balls.remove(ball)

    balance_text = font.render(f"Balance: {balance}€", True, BLUE)
    screen.blit(balance_text, (10, 10))

    stake_label_text = font.render("Stake:", True, WHITE)
    screen.blit(stake_label_text, (10, SLIDER_TRACK_Y + SLIDER_TRACK_HEIGHT // 2 - stake_label_text.get_height() // 2))

    track_color = DISABLED_COLOR if slider_disabled else GREY
    handle_color = DISABLED_COLOR if slider_disabled else BLUE

    pygame.draw.rect(screen, track_color, slider_track_rect)
    pygame.draw.rect(screen, handle_color, slider_handle_rect)

    stake_value_text = font.render(f"{current_stake}", True, WHITE)
    screen.blit(stake_value_text, (slider_track_rect.right + 10, SLIDER_TRACK_Y + SLIDER_TRACK_HEIGHT // 2 - stake_value_text.get_height() // 2))

    board.draw_reset_button(screen, font)
    board.draw_exit_button(screen, font)

    if insufficient_balance and balance < current_stake:
        insufficient_text_y = SLIDER_TRACK_Y + SLIDER_HANDLE_HEIGHT + 15
        screen.blit(font.render("Insufficient balance!", True, RED), (10, insufficient_text_y))

    pygame.display.flip()


pygame.quit()
sys.exit()
