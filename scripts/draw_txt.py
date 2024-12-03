from configs import *

def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    SCREEN.blit(text_surface, (x, y))