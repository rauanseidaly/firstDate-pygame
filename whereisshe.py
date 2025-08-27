# whereisshe.py
import pygame
import os
import time
from night import start_night_scene

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (100, 149, 237)

def start_whereisshe_scene(screen):
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 24)
    small_font = pygame.font.SysFont("arial", 16)

    # Фоны
    street_img_path = os.path.join("assets", "images", "street.png")
    street_img = pygame.image.load(street_img_path).convert()
    new_street_img_path = os.path.join("assets", "images", "street_with_begim.png")
    new_street_img = pygame.image.load(new_street_img_path).convert()

    # Координаты кликабельных зон
    cafe_right_rect = pygame.Rect(550, 200, 150, 250)  # здание справа
    cafe_left_rect = pygame.Rect(100, 200, 150, 250)   # здание слева
    phone_rect = pygame.Rect(380, 450, 40, 80)         # карман персонажа

    # Кнопка "Дальше"
    next_btn_rect = pygame.Rect(screen.get_width()//2 - 100, screen.get_height()//2 + 100, 200, 50)

    current_mission = 1
    show_message = False
    message_text = ""
    state = "missions"  # missions → phone_message → new_bg → next_btn
    new_bg_time = None

    running = True
    while running:
        screen.fill(WHITE)

        # Фон в зависимости от состояния
        if state == "new_bg" or state == "next_btn":
            screen.blit(new_street_img, (0, 0))
        else:
            screen.blit(street_img, (0, 0))

        # Миссии (показываются только пока state == missions)
        if state == "missions":
            if current_mission == 1:
                mission_text = "Миссия 1: Зайти в кафе (клик по зданию справа)"
                hint_text = "Кликните по зданию справа"
            elif current_mission == 2:
                mission_text = "Миссия 2: Зайти в другое кафе"
                hint_text = "Кликните по зданию слева"
            elif current_mission == 3:
                mission_text = "Миссия: Проверить смартфон"
                hint_text = "Кликните по карману персонажа"
            else:
                mission_text = "Миссия завершена"
                hint_text = "Ожидание следующей сцены..."

            mission_render = font.render(mission_text, True, WHITE)
            screen.blit(mission_render, (20, 5))

            hint_label = small_font.render("Подсказка: " + hint_text, True, WHITE)
            screen.blit(hint_label, (screen.get_width() - hint_label.get_width() - 10,
                                     screen.get_height() - hint_label.get_height() - 10))

        # Сообщения
        if show_message and current_mission in (1, 2):
            msg_surf = font.render(message_text, True, WHITE)
            pygame.draw.rect(screen, BLACK, (20, screen.get_height() - 80,
                                             msg_surf.get_width() + 20, 50))
            screen.blit(msg_surf, (30, screen.get_height() - 65))

        if state == "phone_message":
            # Рамка сообщения от Бегимжан
            pygame.draw.rect(screen, BLUE, (100, 150, 600, 300), border_radius=10)
            pygame.draw.rect(screen, WHITE, (110, 160, 580, 280), border_radius=10)

            title_text = font.render("Сообщение от Бегимжан", True, BLACK)
            msg_text = font.render("привет, я стою возле того здания", True, BLACK)

            screen.blit(title_text, (120, 180))
            screen.blit(msg_text, (120, 220))

        # Кнопка "Дальше"
        if state == "next_btn":
            pygame.draw.rect(screen, (100, 180, 100), next_btn_rect)
            pygame.draw.rect(screen, BLACK, next_btn_rect, 2)
            btn_text = font.render("Дальше", True, WHITE)
            screen.blit(btn_text, btn_text.get_rect(center=next_btn_rect.center))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if state == "missions":
                    if current_mission == 1 and cafe_right_rect.collidepoint(event.pos):
                        show_message = True
                        message_text = "Извините, у нас все занято"
                        current_mission = 2
                    elif current_mission == 2 and cafe_left_rect.collidepoint(event.pos):
                        show_message = True
                        message_text = "Извините, у нас все занято"
                        current_mission = 3
                    elif current_mission == 3 and phone_rect.collidepoint(event.pos):
                        show_message = False
                        state = "phone_message"

                elif state == "phone_message":
                    # Переход к новому фону
                    state = "new_bg"
                    new_bg_time = time.time()

                elif state == "next_btn" and next_btn_rect.collidepoint(event.pos):
                    running = start_night_scene(screen)  # здесь можно вызывать следующую сцену

        # Таймер появления кнопки
        if state == "new_bg" and new_bg_time is not None:
            if time.time() - new_bg_time >= 3.5:
                state = "next_btn"

        pygame.display.flip()
        clock.tick(60)
