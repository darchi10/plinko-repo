import pygame
from settings import *

class PlinkoBoard:
    def __init__(self):
        self.cordinates = []

    def draw_pins(self, screen):
        CELL_WIDTH = (WIDTH // COLS)
        if not self.cordinates:
            for row in range(1, ROWS):
                num_pins = row + 1 
                start_x = WIDTH // 2 - (num_pins - 1) * CELL_WIDTH // 2

                for col in range(num_pins):
                    x = start_x + col * CELL_WIDTH
                    y = row * CELL_HEIGHT + 100
                    self.cordinates.append((x, y))
        
        for (x, y) in self.cordinates:
            pygame.draw.circle(screen, BLACK, (x, y), 7)


    def get_pins_cordinates(self):
        return self.cordinates

    def draw_slots(self, screen, font):
        for i in range(NUMBER_OF_SLOTS):
            x = i * SLOT_WIDTH

            pygame.draw.rect(screen, GREY, (x, HEIGHT - 80, SLOT_WIDTH, 80), 2)
            
            value_text = font.render(str(SLOT_VALUES[i]), True, BLACK)
            text_rect = value_text.get_rect(center=(x + SLOT_WIDTH // 2, HEIGHT - 40))
            screen.blit(value_text, text_rect)

        pygame.draw.line(screen, BLACK, (0, HEIGHT - 80), (WIDTH, HEIGHT - 80), 2)

