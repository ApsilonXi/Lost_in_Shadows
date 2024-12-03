import pygame
from text_manager import load_strings

def draw_text_menu(screen, text, font, color, x, y):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def main_menu_loop(screen, black, font, gold, width, height, red, white, clock, background_texture):
    running = True
    current_language = "en"
    strings = load_strings(f"lang/{current_language}.txt")
    
    while running:
        screen.fill(black)
        screen.blit(background_texture, (0, 0))
        draw_text_menu(screen, "Lost In Shadows", font, gold, (width // 2 - 100), (height // 4 + 60))

        mouse = pygame.mouse.get_pos()

        quit_text_pos = (width // 2 - 40, height // 2 + 20)
        lang_button_pos = (width // 2 - 100, height // 2 + 150)

        if width // 2 - 150 < mouse[0] < width // 2 + 150 and height // 2 - 40 < mouse[1] < height // 2 + 30:
            draw_text_menu(screen, strings[0], font, red, width // 2 - 40, height // 2 - 30)
        else:
            draw_text_menu(screen, strings[0], font, white, width // 2 - 40, height // 2 - 30)

        if width // 2 - 150 < mouse[0] < width // 2 + 150 and height // 2 + 30 < mouse[1] < height // 2 + 60:
            draw_text_menu(screen, strings[1], font, red, *quit_text_pos)
        else:
            draw_text_menu(screen, strings[1], font, white, *quit_text_pos)

        if width // 2 - 150 < mouse[0] < width // 2 + 150 and height // 2 + 150 < mouse[1] < height // 2 + 190:
            draw_text_menu(screen, strings[2], font, red, *lang_button_pos)
        else:
            draw_text_menu(screen, strings[2], font, white, *lang_button_pos)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:  
                if width // 2 - 150 < mouse[0] < width // 2 + 150 and height // 2 - 40 < mouse[1] < height // 2 + 30:
                    running = False  
                if width // 2 - 150 < mouse[0] < width // 2 + 150 and height // 2 + 30 < mouse[1] < height // 2 + 60:
                    pygame.quit()  
                    quit()
                if width // 2 - 150 < mouse[0] < width // 2 + 150 and height // 2 + 150 < mouse[1] < height // 2 + 190:
                    current_language = "ru" if current_language == "en" else "en"
                    strings = load_strings(f"lang/{current_language}.txt")

        pygame.display.update()
        clock.tick(30)