import pygame
import random
from draw_txt import *
import music as music


class StatusEffect:
    def __init__(self, name, duration, effect_function):
        self.name = name  # Имя состояния
        self.duration = duration  # Длительность состояния
        self.effect_function = effect_function  # Функция, которая применяет эффект
        self.start_time = pygame.time.get_ticks()  # Время начала эффекта

    def apply(self, hero):
        if pygame.time.get_ticks() - self.start_time < self.duration:
            self.effect_function(hero)
        else:
            return False  # Возвращаем False, если состояние истекло
        return True  # Возвращаем True, если состояние еще активно

def burn_effect(hero):
    hero.health -= 1  # Уменьшаем здоровье героя каждую секунду
    draw_text("Горение", pygame.font.Font("fonts/hohenzollernlamont.ttf", 36) , RED, 20, HEIGHT - 100)

def bleed_effect(hero):
    hero.health -= 2  # Накладываем урон кровотечением
    draw_text("Кровотечение", pygame.font.Font("fonts/hohenzollernlamont.ttf", 36) , RED, 20, HEIGHT - 150)

class FlyingDemon:
    def __init__(self, font):
        self.health = 22
        self.speed = 5
        self.image_width, self.image_height = 300, 300
        self.hitbox_width, self.hitbox_height = 300, 300
        self.offset_x, self.offset_y = 0, 50  # Смещение по оси X и Y
        self.rect = pygame.Rect(
            WIDTH//2 + 300,  # X координата
            400,  # Y координата
            self.hitbox_width, self.hitbox_height
        )

        self.is_attacking = False  # Флаг для отслеживания атакии

        # Шрифты для отображения урона
        self.font = font

        # Анимация покоя
        self.idle_frames = [
            pygame.transform.scale(pygame.image.load(f"sprites/enemys/demon/idle/idle{i}.png").convert_alpha(), (300, 300))
            for i in range(1, 5)
        ]
        self.idle_frame_index = 0
        self.idle_animation_speed = 0.1
        self.idle_time_accumulator = 0

        # Анимация атаки
        self.attack_frames = [
            pygame.transform.scale(pygame.image.load(f"sprites/enemys/demon/attack/attack{i}.png").convert_alpha(), (300, 300))
            for i in range(1, 9)
        ]
        self.attack_frame_index = 0
        self.attack_animation_speed = 0.1
        self.attack_time_accumulator = 0

        # Начальная текстура - первый кадр анимации покоя
        self.texture = self.idle_frames[0]

    def draw(self, dt):
        """Отображение врага на экране с обновлением анимации"""
        if self.is_attacking:
            # Анимация атаки
            self.attack_time_accumulator += dt
            if self.attack_time_accumulator >= self.attack_animation_speed:
                self.attack_time_accumulator = 0
                self.attack_frame_index = (self.attack_frame_index + 1) % len(self.attack_frames)
            self.texture = self.attack_frames[self.attack_frame_index]
        else:
            # Анимация покоя
            self.idle_time_accumulator += dt
            if self.idle_time_accumulator >= self.idle_animation_speed:
                self.idle_time_accumulator = 0
                self.idle_frame_index = (self.idle_frame_index + 1) % len(self.idle_frames)
            self.texture = self.idle_frames[self.idle_frame_index]

        # Отрисовка демона
        SCREEN.blit(self.texture, self.rect)

    def attack(self, hero):
        damage = random.randint(4, 15)  # Наносимый урон
        hero.health -= damage  # Уменьшаем здоровье героя
        hero.status_effects.append(StatusEffect("Burn", 5000, burn_effect))
        return damage  # Возвращаем величину урона
    
    def start_attack_animation(self):
        """Начало анимации атаки"""
        self.is_attacking = True
        self.attack_frame_index = 0
        music.play_enemy_hit_hero_sound() # Воспроизведение звука удара при начале анимации
        
    def stop_attack_animation(self):
        """Окончание анимации атаки, возвращение к покою"""
        self.is_attacking = False

class Goblin:
    def __init__(self, font):
        self.health = 29
        self.speed = 5
        self.image_width, self.image_height = 300, 300
        self.hitbox_width, self.hitbox_height = 300, 300
        self.offset_x, self.offset_y = 0, 50  # Смещение по оси X и Y
        self.rect = pygame.Rect(
            WIDTH//2 + 300,  # X координата
            HEIGHT//2,  # Y координата
            self.hitbox_width, self.hitbox_height
        )

        self.is_attacking = False  # Флаг для отслеживания атакии

        # Шрифты для отображения урона
        self.font = font

        # Анимация покоя
        self.idle_frames = [
            pygame.transform.scale(pygame.image.load(f"sprites/enemys/goblin/idle/idle{i}.png").convert_alpha(), (450, 450))
            for i in range(1, 5)
        ]
        self.idle_frame_index = 0
        self.idle_animation_speed = 0.1
        self.idle_time_accumulator = 0

        # Анимация атаки
        self.attack_frames = [
            pygame.transform.scale(pygame.image.load(f"sprites/enemys/goblin/attack/attack{i}.png").convert_alpha(), (450, 450))
            for i in range(1, 9)
        ]
        self.attack_frame_index = 0
        self.attack_animation_speed = 0.1
        self.attack_time_accumulator = 0

        # Начальная текстура - первый кадр анимации покоя
        self.texture = self.idle_frames[0]

    def draw(self, dt):
        """Отображение врага на экране с обновлением анимации"""
        if self.is_attacking:
            # Анимация атаки
            self.attack_time_accumulator += dt
            if self.attack_time_accumulator >= self.attack_animation_speed:
                self.attack_time_accumulator = 0
                self.attack_frame_index = (self.attack_frame_index + 1) % len(self.attack_frames)
            self.texture = self.attack_frames[self.attack_frame_index]
        else:
            # Анимация покоя
            self.idle_time_accumulator += dt
            if self.idle_time_accumulator >= self.idle_animation_speed:
                self.idle_time_accumulator = 0
                self.idle_frame_index = (self.idle_frame_index + 1) % len(self.idle_frames)
            self.texture = self.idle_frames[self.idle_frame_index]

        # Отрисовка демона
        SCREEN.blit(self.texture, self.rect)

    def attack(self, hero):
        """Метод атаки"""
        damage = random.randint(8, 18)  # Наносимый урон
        hero.health -= damage  # Уменьшаем здоровье героя
        hero.status_effects.append(StatusEffect("Bleed", 3000, bleed_effect))
        return damage  # Возвращаем величину урона
        
    def start_attack_animation(self):
        """Начало анимации атаки"""
        self.is_attacking = True
        self.attack_frame_index = 0
        music.play_enemy_hit_hero_sound() # Воспроизведение звука удара при начале анимации
        
    def stop_attack_animation(self):
        """Окончание анимации атаки, возвращение к покою"""
        self.is_attacking = False

class Skeleton:
    def __init__(self, font):
        self.health = 34
        self.speed = 5
        self.image_width, self.image_height = 300, 300
        self.hitbox_width, self.hitbox_height = 300, 300
        self.offset_x, self.offset_y = 0, 50  # Смещение по оси X и Y
        self.rect = pygame.Rect(
            WIDTH//2 + 300,  # X координата
            HEIGHT//2 - 300,  # Y координата
            self.hitbox_width, self.hitbox_height
        )

        self.is_attacking = False  # Флаг для отслеживания атакии

        # Шрифты для отображения урона
        self.font = font

        # Анимация покоя
        self.idle_frames = [
            pygame.transform.scale(pygame.image.load(f"sprites/enemys/skeleton/idle/idle{i}.png").convert_alpha(), (400, 750))
            for i in range(1, 5)
        ]
        self.idle_frame_index = 0
        self.idle_animation_speed = 0.1
        self.idle_time_accumulator = 0

        # Анимация атаки
        self.attack_frames = [
            pygame.transform.scale(pygame.image.load(f"sprites/enemys/skeleton/attack/attack{i}.png").convert_alpha(), (400, 750))
            for i in range(1, 9)
        ]
        self.attack_frame_index = 0
        self.attack_animation_speed = 0.1
        self.attack_time_accumulator = 0

        # Начальная текстура - первый кадр анимации покоя
        self.texture = self.idle_frames[0]

    def draw(self, dt):
        """Отображение врага на экране с обновлением анимации"""
        if self.is_attacking:
            # Анимация атаки
            self.attack_time_accumulator += dt
            if self.attack_time_accumulator >= self.attack_animation_speed:
                self.attack_time_accumulator = 0
                self.attack_frame_index = (self.attack_frame_index + 1) % len(self.attack_frames)
            self.texture = self.attack_frames[self.attack_frame_index]
        else:
            # Анимация покоя
            self.idle_time_accumulator += dt
            if self.idle_time_accumulator >= self.idle_animation_speed:
                self.idle_time_accumulator = 0
                self.idle_frame_index = (self.idle_frame_index + 1) % len(self.idle_frames)
            self.texture = self.idle_frames[self.idle_frame_index]

        # Отрисовка демона
        SCREEN.blit(self.texture, self.rect)

    def attack(self, hero):
        """Метод атаки"""
        damage = random.randint(11, 23)  # Наносимый урон
        hero.health -= damage  # Уменьшаем здоровье героя
        return damage  # Возвращаем величину урона
        
    def start_attack_animation(self):
        """Начало анимации атаки"""
        self.is_attacking = True
        self.attack_frame_index = 0
        music.play_enemy_hit_hero_sound() # Воспроизведение звука удара при начале анимации
        
    def stop_attack_animation(self):
        """Окончание анимации атаки, возвращение к покою"""
        self.is_attacking = False

class Mushroom:
    def __init__(self, font):
        self.health = 67
        self.speed = 5
        self.image_width, self.image_height = 300, 300
        self.hitbox_width, self.hitbox_height = 300, 300
        self.offset_x, self.offset_y = 0, 50  # Смещение по оси X и Y
        self.rect = pygame.Rect(
            WIDTH//2 + 300,  # X координата
            HEIGHT//2 - 380,  # Y координата
            self.hitbox_width, self.hitbox_height
        )

        self.is_attacking = False  # Флаг для отслеживания атакии

        # Шрифты для отображения урона
        self.font = font

        # Анимация покоя
        self.idle_frames = [
            pygame.transform.scale(pygame.image.load(f"sprites/enemys/mushroom/idle/idle{i}.png").convert_alpha(), (500, 850))
            for i in range(1, 5)
        ]
        self.idle_frame_index = 0
        self.idle_animation_speed = 0.1
        self.idle_time_accumulator = 0

        # Анимация атаки
        self.attack_frames = [
            pygame.transform.scale(pygame.image.load(f"sprites/enemys/mushroom/attack/attack{i}.png").convert_alpha(), (500, 850))
            for i in range(1, 9)
        ]
        self.attack_frame_index = 0
        self.attack_animation_speed = 0.1
        self.attack_time_accumulator = 0

        # Начальная текстура - первый кадр анимации покоя
        self.texture = self.idle_frames[0]

    def draw(self, dt):
        """Отображение врага на экране с обновлением анимации"""
        if self.is_attacking:
            # Анимация атаки
            self.attack_time_accumulator += dt
            if self.attack_time_accumulator >= self.attack_animation_speed:
                self.attack_time_accumulator = 0
                self.attack_frame_index = (self.attack_frame_index + 1) % len(self.attack_frames)
            self.texture = self.attack_frames[self.attack_frame_index]
        else:
            # Анимация покоя
            self.idle_time_accumulator += dt
            if self.idle_time_accumulator >= self.idle_animation_speed:
                self.idle_time_accumulator = 0
                self.idle_frame_index = (self.idle_frame_index + 1) % len(self.idle_frames)
            self.texture = self.idle_frames[self.idle_frame_index]

        # Отрисовка демона
        SCREEN.blit(self.texture, self.rect)

    def attack(self, hero):
        """Метод атаки"""
        damage = random.randint(12, 23)  # Наносимый урон
        hero.health -= damage  # Уменьшаем здоровье героя
        return damage  # Возвращаем величину урона
        
    def start_attack_animation(self):
        """Начало анимации атаки"""
        self.is_attacking = True
        self.attack_frame_index = 0
        music.play_enemy_hit_hero_sound() # Воспроизведение звука удара при начале анимации
        
    def stop_attack_animation(self):
        """Окончание анимации атаки, возвращение к покою"""
        self.is_attacking = False
