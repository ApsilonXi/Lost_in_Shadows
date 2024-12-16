#------------------------------------------------
# Developers:
#   Emilia Volkova
#   Basenko Bella
#   Vyacheslav Oleshchuk
#   Bogdanov Ivan
#   Grand Babayan
#   Evsyukova Sofya
#------------------------------------------------

import pygame
import random
import time
from configs import *
from draw_txt import *
import music as music  
import main_menu as main_menu
from enemys_classes import *

# Инициализация Pygame
pygame.init()

# Запуск фоновой музыки
music.play_background_music()

pygame.display.set_caption("Lost In Shadows")

# Игровые переменные
hero_health = 100
room_counter = 1
enemy_health = 50
game_over_state = False  # Добавляем переменную для отслеживания состояния "Game Over"

# Новые переменные для подсчета статистики
enemies_killed = 0
damage_dealt = 0
attacks_made = 0
potions_used = 0


# Загрузка шрифта 
font = pygame.font.Font("fonts/hohenzollernlamont.ttf", 36)  # Путь к файлу шрифта

# Таймер для анимации или изменения игры
clock = pygame.time.Clock()

# Загрузка текстур
background_texture = pygame.image.load("textures/background.png").convert() # Текстура для интерфейса (например, фона)
bg_main_menu_texture = pygame.image.load("textures/bg_main_menu.png").convert() 
campfire_texture = pygame.image.load("textures/campfire.png").convert_alpha()  # Текстура костра
bg_battle = pygame.image.load("textures/blue-back.png").convert()
dead_hero = pygame.image.load("sprites/hero/death/death4.png").convert_alpha()

# Масштабирование текстур под размеры экрана
background_texture = pygame.transform.scale(background_texture, (WIDTH, HEIGHT))  # Масштабируем фон на весь экран
bg_main_menu_texture = pygame.transform.scale(bg_main_menu_texture, (WIDTH, HEIGHT))
campfire_texture = pygame.transform.scale(campfire_texture, (200, 200))  # Масштабируем текстуру костра
bg_battle = pygame.transform.scale(bg_battle, (WIDTH, HEIGHT))
dead_hero = pygame.transform.scale(dead_hero, (600, 400)) 

class Hero:
    def __init__(self):
        self.health = 100
        self.speed = 15
        self.image_width, self.image_height = 450, 750
        self.hitbox_width, self.hitbox_height = 450, 750
        self.offset_x, self.offset_y = 0, 50  # Смещение по оси X и Y
        self.rect = pygame.Rect(
            200,  # X координата
            HEIGHT // 2 - 380,  # Y координата (с центрированием)
            self.hitbox_width, self.hitbox_height
        )

        self.potions = 2
        self.is_moving = False  # Флаг для отслеживания движения
        self.is_attacking = False  # Флаг для отслеживания атаки

        self.status_effects = []  # Список активных состояний

        
        # Статистика
        self.attacks_made = 0
        self.damage_dealt = 0
        self.potions_used = 0
        self.enemies_killed = 0
        
        # Анимация покоя
        self.idle_frames = [
            pygame.transform.scale(pygame.image.load(f"sprites/hero/idle/idle{i}.png").convert_alpha(), (450, 750))
            for i in range(1, 9)
        ]
        self.idle_frame_index = 0  # Текущий кадр анимации
        self.idle_animation_speed = 0.1  # Скорость анимации покоя
        self.idle_time_accumulator = 0  # Время для переключения кадров

        # Анимация бега
        self.run_frames = [
            pygame.transform.scale(pygame.image.load(f"sprites/hero/run/run{i}.png").convert_alpha(), (450, 750))
            for i in range(1, 9)
        ]
        self.run_frame_index = 0  # Текущий кадр анимации бега
        self.run_animation_speed = 0.1  # Скорость анимации бега
        self.run_time_accumulator = 0  # Время для переключения кадров

        # Анимация атаки
        self.attack_frames = [
            pygame.transform.scale(pygame.image.load(f"sprites/hero/attack/attack{i}.png").convert_alpha(), (450, 750))
            for i in range(1, 8)
        ]
        self.attack_frame_index = 0  # Текущий кадр анимации атаки
        self.attack_animation_speed = 0.1  # Скорость анимации атаки
        self.attack_time_accumulator = 0  # Время для переключения кадров
        self.is_attacking = False  # Флаг атаки

    def draw(self, dt):
        """Метод для отрисовки героя на экране. Принимает dt (delta time) для обновления анимации."""
        if self.is_attacking:
            # Анимация атаки
            self.attack_time_accumulator += dt
            if self.attack_time_accumulator >= self.attack_animation_speed:
                self.attack_time_accumulator = 0
                self.attack_frame_index = (self.attack_frame_index + 1) % len(self.attack_frames)
            self.texture = self.attack_frames[self.attack_frame_index]
        elif self.is_moving:
            # Анимация бега
            self.run_time_accumulator += dt
            if self.run_time_accumulator >= self.run_animation_speed:
                self.run_time_accumulator = 0
                self.run_frame_index = (self.run_frame_index + 1) % len(self.run_frames)
            self.texture = self.run_frames[self.run_frame_index]
        else:
            # Анимация покоя
            self.idle_time_accumulator += dt
            if self.idle_time_accumulator >= self.idle_animation_speed:
                self.idle_time_accumulator = 0
                self.idle_frame_index = (self.idle_frame_index + 1) % len(self.idle_frames)
            self.texture = self.idle_frames[self.idle_frame_index]

        # Отрисовка текущей текстуры героя
        SCREEN.blit(self.texture, self.rect)
        draw_text(f"HP: {self.health}", font, GOLD, 20, HEIGHT - 50)


    def start_attack_animation(self):
        """Начало анимации атаки"""
        self.is_attacking = True
        self.attack_frame_index = 0
        music.play_hero_hit_enemy_sound() # Воспроизведение звука удара при начале анимации

    def stop_attack_animation(self):
        """Окончание анимации атаки, возвращение к покою"""
        self.is_attacking = False

    def move(self, keys):
        self.is_moving = False  # Сначала предполагаем, что герой не двигается

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x = max(0, self.rect.x - self.speed)
            self.is_moving = True
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x = min(WIDTH * 0.95 - self.rect.width, self.rect.x + self.speed)
            self.is_moving = True
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.rect.y = max(HEIGHT // 4, self.rect.y - self.speed)
            self.is_moving = True
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.y = min(HEIGHT // 3.5, self.rect.y + self.speed)
            self.is_moving = True

    def attack(self, enemy):
        self.attacks_made += 1
        damage = random.randint(5, 19)
        self.damage_dealt += damage
        enemy.health -= damage
        return damage

    def drink_potion(self):
        if self.potions > 0:
            self.health = min(100, self.health + 25)
            self.potions -= 1
            self.potions_used += 1
    
    def defend(self):
        # Защита: уменьшаем урон врага
        self.health += 5  # Небольшое восстановление здоровья
        self.health = min(self.health, 100)
    
    def heal(self):
        self.health = min(100, self.health + 30)

    def update_status_effects(self):
        """Обновляем активные состояния и применяем эффекты"""
        for effect in self.status_effects[:]:
            if not effect.apply(self):
                self.status_effects.remove(effect)  # Удаляем истекшие состояния

class Button:
    def __init__(self, x, y, width, height, text, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action  # действие при нажатии на кнопку
        self.color = (100, 100, 255)
        self.font = pygame.font.Font(None, 36)
    
    def draw(self):
        pygame.draw.rect(SCREEN, self.color, self.rect)
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        SCREEN.blit(text_surface, (self.rect.x + (self.rect.width - text_surface.get_width()) // 2,
                                   self.rect.y + (self.rect.height - text_surface.get_height()) // 2))
    
    def is_pressed(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)
    
class DamageText: #Данный класс нужен для отображения текста врага.
    def __init__(self, text, x, y, color, duration=1500):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.duration = duration  # Длительность отображения (в миллисекундах)
        self.start_time = pygame.time.get_ticks()  # Время начала анимации

    def draw(self):
        # Отрисовка текста
        draw_text(self.text, font, self.color, self.x, self.y)
        
    def is_expired(self):
        # Проверка, прошло ли заданное время
        return pygame.time.get_ticks() - self.start_time > self.duration


def combat(hero, enemy):
    if enemy.health > 0:
        hero.attack(enemy)
        if enemy.health > 0:
            enemy.attack(hero)

def battle_screen(hero, enemy):
    running = True
    battle_phase = "hero_turn"  # Фаза боя: ход героя или врага
    action = None  # Действие, выбранное игроком (атаковать, защищаться или использовать зелье)
    damage_texts = []  # Список текстов урона

    # Обнуляем флаг движения героя, чтобы анимация была "покой"
    hero.is_moving = False  # Важно сбросить движение при начале боя

    # Позиции для битвы: используем текущие координаты героя
    hero_battle_pos = (200, HEIGHT // 2 - 380)
    enemy_battle_pos = (WIDTH * 3 // 4 - enemy.rect.width // 2, HEIGHT // 2 - enemy.rect.height // 2)

    # Создаем кнопки атаки, защиты и зелья
    attack_button = Button(WIDTH // 4 - 50, HEIGHT - 150, 200, 50, "Атака", "attack")
    defend_button = Button(WIDTH // 4 - 300, HEIGHT - 150, 200, 50, "Защита", "defend")
    heal_button = Button(WIDTH // 4 + 200, HEIGHT - 150, 200, 50, f"Зелье X{hero.potions}", "heal")
    
    while running:
        SCREEN.blit(bg_battle, (0, 0))  # Очищаем экран
        dt = clock.tick(30) / 1000.0  # Время, прошедшее с предыдущего кадра

        # Отображаем информацию о герое и враге
        draw_text(f"Enemy HP: {enemy.health}", font, WHITE, WIDTH - 190, HEIGHT - 50)

        # Отображаем героя на той же позиции и обновляем анимацию
        hero.rect.x, hero.rect.y = hero_battle_pos  # Восстанавливаем позицию героя
        hero.draw(dt)  # Отображаем героя с текущей анимацией (по умолчанию покой)

        # Отображаем врага
        enemy.draw(dt)

        # Рисуем кнопки
        attack_button.draw()
        defend_button.draw()
        heal_button.draw()

        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if attack_button.is_pressed(mouse_pos):
                    action = "attack"
                elif defend_button.is_pressed(mouse_pos):
                    action = "defend"
                elif heal_button.is_pressed(mouse_pos):
                    action = "heal"

        # Логика пошагового боя
        if battle_phase == "hero_turn":
            if action == "attack":
                if not hero.is_attacking:
                    # Запуск анимации атаки
                    hero.start_attack_animation()

                if hero.attack_frame_index == len(hero.attack_frames) - 1:  # Если последний кадр анимации атаки
                    damage = hero.attack(enemy)  # Герой атакует
                    damage_texts.append(DamageText(f"-{damage}", enemy_battle_pos[0] + enemy.rect.width // 2,
                                                   enemy_battle_pos[1] - 30, RED))  # Добавляем текст урона
                    hero.stop_attack_animation()  # Остановка анимации атаки, возврат к покою
                    battle_phase = "enemy_turn"  # Переход к ходу врага
                    action = None
            elif action == "defend":
                hero.defend()  # Герой защищается
                music.play_enemy_hit_hero_in_shield_sound()
                battle_phase = "enemy_turn"  # Переход к ходу врага
                action = None
            elif action == "heal":
                hero.drink_potion()
                heal_button.text = f"Зелье X{hero.potions}"
                action = None
        elif battle_phase == "enemy_turn":
            if not enemy.is_attacking:
                enemy.start_attack_animation()

            if enemy.attack_frame_index == len(enemy.attack_frames) - 1:  # Если последний кадр анимации атаки
                    damage = enemy.attack(hero)  # Герой атакует
                    music.play_enemy_hit_hero_sound()
                    damage_texts.append(DamageText(f"-{damage}", hero_battle_pos[0] + hero.rect.width // 2,
                                                hero_battle_pos[1] - 30, RED)) 
                    enemy.stop_attack_animation()  
                    battle_phase = "hero_turn"  # Переход к ходу героя

        # Обновляем и рисуем текст урона
        for damage_text in damage_texts[:]:
            damage_text.draw()
            if damage_text.is_expired():
                damage_texts.remove(damage_text)

        # Проверка на окончание боя
        if hero.health <= 0:
            running = False
            return False
            
        if enemy.health <= 0:
            hero.enemies_killed += 1  # Увеличиваем счетчик убитых врагов
            return True

        pygame.display.update()

def display_text_from_file(file_path):
    """Чтение текста из файла."""
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Отображаем текст по строкам
    for line in lines:
        display_line(line.strip())  # Отображаем каждую строку
        wait_for_space_press()  # Ожидаем нажатия пробела или пропуска
    return True

def display_line(line):
    """Отображение строки текста по буквенно с центрированием."""
    current_text = ""
    text_surface = font.render(current_text, True, GOLD)
    text_width, text_height = text_surface.get_size()
    x_position = (WIDTH - text_width) // 2  # Центрируем текст по ширине экрана
    y_position = HEIGHT // 2 - 200  # Позиция по высоте

    for char in line:
        if "Потерянный в тенях" in line:
            # Отображаем фразу красным и курсивом
            current_text = "Потерянный в тенях"
            text_surface = font.render(current_text, True, RED)  # Красный текст с курсивом
        else:
            # Обычное отображение
            current_text += char
            text_surface = font.render(current_text, True, GOLD)

        text_width, text_height = text_surface.get_size()  # Получаем актуальную ширину текста
        x_position = (WIDTH - text_width) // 2  # Пересчитываем x-координату для центрирования текста

        SCREEN.fill(BLACK)  # Заливаем экран для обновления
        SCREEN.blit(text_surface, (x_position, y_position))  # Отображаем текущий текст
        pygame.display.update()
        time.sleep(0.05)  # Пауза между выводом символов

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Если нажали ESC, выходим
                    pygame.quit()
                    quit()

def wait_for_space_press():
    """Ожидание нажатия пробела или пропуска."""
    waiting_for_space = True
    while waiting_for_space:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Когда нажали пробел
                    waiting_for_space = False
                    break
        pygame.display.update()

# Главный игровой цикл
def game_loop():
    global room_counter, game_over_state, chest

    hero = Hero()
    enemy = None
    in_combat = False

    while not game_over_state:
        dt = clock.tick(30) / 1200.0
        SCREEN.blit(background_texture, (0, 0))  # Отрисовка фона

        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Если нажали ESC, выходим
                    pygame.quit()
                    quit()

        keys = pygame.key.get_pressed()  # Список нажатых клавиш
       

        # Логика комнат
        if room_counter % 4 == 0:  # Комната для отдыха каждые 4 комнаты
            draw_text("Resting Room. Press R to rest.", font, GOLD, WIDTH // 2 - 180, HEIGHT // 2 - 100)
            SCREEN.blit(campfire_texture, (WIDTH // 2 - 100, HEIGHT // 2 + 200))  # Рисуем костёр
            if keys[pygame.K_r]:  # Восстанавливаем здоровье при нажатии R
                hero.heal()
                room_counter += 1
                enemy = None  # Удаляем врага
                hero.potions = 2
                in_combat = False
        else:
            if not in_combat:
                if enemy:
                    enemy.draw(dt) # Рисуем врага с передачей dt
                else:
                    enemy = random.choice([FlyingDemon(font), Goblin(font), Skeleton(font), Mushroom(font)])  # Создаём врага
                
                # Рисуем героя и даём ему возможность двигаться
                    
                hero.move(keys)
                hero.draw(clock.tick(30) / 1000.0) 
                hero.update_status_effects()

                # Если враг есть, отрисовываем его и проверяем на столкновение
                if enemy:
                    enemy.draw(dt)
                    if hero.rect.colliderect(enemy.rect):  # Если герой столкнулся с врагом
                        battle_result = battle_screen(hero, enemy)  # Переход на экран боя

                        # Проверка состояния после боя
                        if battle_result:  # Если враг побеждён
                            room_counter += 1
                            enemy = None  # Удаляем врага
                            in_combat = False  # Возвращаемся к нормальной игре
                        else:  # Если герой погиб
                            game_over_state = True

        # Проверка на проигрыш
        if hero.health <= 0:
            music.play_hero_death_sound()
            game_over_state = True
            music.play_game_over_music()  # Проигрывание музыки "Game Over"

        # Если герой мёртв, отрисовываем анимацию смерти и Game Over экран
        if game_over_state:
            SCREEN.fill(BLACK)  # Заливаем экран чёрным цветом
            SCREEN.blit(background_texture, (0, 0))
            
            # Отображаем текстуру мертвого героя
            dead_hero_x = WIDTH // 2 - dead_hero.get_width() // 2  # Центрируем текстуру по ширине
            dead_hero_y = HEIGHT // 2 - dead_hero.get_height() // 2 + 200 
            SCREEN.blit(dead_hero, (dead_hero_x, dead_hero_y))

            # Отображение текста Game Over
            draw_text("Game Over", pygame.font.Font("fonts/hohenzollernlamont.ttf", 50), RED, WIDTH // 2 - 50, 300)

            # Отображение статистики
            draw_text(f"Убито врагов: {hero.enemies_killed}", font, RED, WIDTH // 2 - 180, HEIGHT // 2 - 150)
            draw_text(f"Нанесено урона: {hero.damage_dealt}", font, RED, WIDTH // 2 - 180, HEIGHT // 2 - 110)
            draw_text(f"Ударов сделано: {hero.attacks_made}", font, RED, WIDTH // 2 - 180, HEIGHT // 2 - 70)
            draw_text(f"Выпито зелий: {hero.potions_used}", font, RED, WIDTH // 2 - 180, HEIGHT // 2 - 30)

            # Отображение дополнительного текста
            draw_text(f'Смерть — лишь ворота. Настоящая бездна начинается здесь.', 
                    pygame.font.Font("fonts/hohenzollernlamont.ttf", 40), GOLD, WIDTH // 2 - 420, HEIGHT // 2 + 150)

        pygame.display.update()

    # После завершения игры, ждем, пока игрок не нажмет ESC для выхода
    while game_over_state:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Если нажали ESC, выходим
                    pygame.quit()
                    quit()

        pygame.display.update()

def prolog():
    SCREEN.fill(BLACK)   # Отрисовка фона
    # Отображаем на экране текст из файла, с кнопкой Skip
    flag = display_text_from_file("prolog.txt")
    if flag:
        return 0

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # Если нажали ESC, выходим
                pygame.quit()
                quit()


if __name__ == "__main__":
    #main_menu.main_menu_loop(SCREEN, BLACK, font, GOLD, WIDTH, HEIGHT, RED, WHITE, clock, bg_main_menu_texture)
    music.play_menu_music()
    #prolog()
    music.play_classical_music()
    game_loop()