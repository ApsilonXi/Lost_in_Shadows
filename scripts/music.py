import pygame

def play_hero_hit_enemy_sound():
    hit_sound = pygame.mixer.Sound('sounds/hero_hit_enemy.mp3')  # Загрузка звука удара
    hit_sound.set_volume(0.5)  # Установка громкости звука удара
    hit_sound.play()
    
def play_enemy_hit_hero_sound():
    hit_sound = pygame.mixer.Sound('sounds/hit_hero_by_enemy.mp3')  # Загрузка звука удара
    hit_sound.set_volume(0.5)  # Установка громкости звука удара
    hit_sound.play()

def play_enemy_hit_hero_in_shield_sound():
    hit_sound = pygame.mixer.Sound('sounds/enemy_hit_hero_in_shield.mp3')  # Загрузка звука удара
    hit_sound.set_volume(0.5)  # Установка громкости звука удара
    hit_sound.play()

def play_rest_sound():
    hit_sound = pygame.mixer.Sound('sounds/rest_sound.mp3')  # Загрузка звука удара
    hit_sound.set_volume(0.5)  # Установка громкости звука удара
    hit_sound.play()

def play_hero_death_sound():
    hit_sound = pygame.mixer.Sound('music/hero_death.mp3')  # Загрузка звука удара
    hit_sound.set_volume(0.5)  # Установка громкости звука удара
    hit_sound.play()

def play_background_music():
    pygame.mixer.music.load('music/prolog_music.mp3')  # Загрузка файла с музыкой
    pygame.mixer.music.set_volume(0.5)  # Установка громкости
    pygame.mixer.music.play(loops=-1)  # Бесконечное повторение

def play_menu_music():
    pygame.mixer.music.load('music/main_menu.mp3')  # Загрузка файла с музыкой
    pygame.mixer.music.set_volume(0.5)  # Установка громкости
    pygame.mixer.music.play(loops=-1)  # Бесконечное повторение

def play_classical_music():
    pygame.mixer.music.load('music/high_hp_music.mp3')  # Загрузка файла с музыкой
    pygame.mixer.music.set_volume(0.5)  # Установка громкости
    pygame.mixer.music.play(loops=-1)  # Бесконечное повторение

def stop_music():
    pygame.mixer.music.stop()

def set_volume(volume):
    pygame.mixer.music.set_volume(volume)

def play_game_over_music():
    pygame.mixer.music.load('music/game_over_music.mp3')  # Загружаем музыку для Game Over
    pygame.mixer.music.set_volume(0.5)  # Устанавливаем громкость (по желанию)
    pygame.mixer.music.play(loops=-1)  # Зацикливаем музыку
