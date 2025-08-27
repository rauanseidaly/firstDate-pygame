# bazar.py
import pygame
import os
import time
from taxi import start_taxi_scene

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (100, 149, 237)
PINK = (255, 182, 193)
GRAY = (200, 200, 200)
GREEN = (100, 180, 100)


def start_bazar_scene(screen):
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 20)
    small_font = pygame.font.SysFont("arial", 16)

    # Загружаем фоны
    bazar_1_img_path = os.path.join("assets", "images", "bazar_1.png")
    bazar_1_img = pygame.image.load(bazar_1_img_path).convert()
    bazar_1_img = pygame.transform.scale(bazar_1_img, (screen.get_width(), screen.get_height()))

    bazar_2_img_path = os.path.join("assets", "images", "bazar_2.png")
    bazar_2_img = pygame.image.load(bazar_2_img_path).convert()
    bazar_2_img = pygame.transform.scale(bazar_2_img, (screen.get_width(), screen.get_height()))

    # Состояние сцены
    scene_state = "drift_scene"
    current_bg = bazar_1_img

    # Диалоговое окно (высота изменена на 120, позиция - выше)
    dialog_rect = pygame.Rect(50, screen.get_height() - 600, screen.get_width() - 100, 120)

    # Текущий диалог
    current_dialog = []
    dialog_index = 0
    waiting_for_click = False
    final_button_rect = None

    # Диалоги
    drift_dialog = [
        ("Система", "Сидим просто и в моменте машина резко дрифтит..."),
        ("Система", "Потом в момент девушка по середине дороги истерично орет...")
    ]

    girl_screaming_dialog = [
        ("Бегимжан", "мы в какую вселенную попали?"),
        ("Рауан", "в ночь 14 февраля..")
    ]

    taxi_dialog = [
        ("Бегимжан", "вот уже мое такси подъезжает"),
        ("Рауан", "ну чтож, Бегимжан, мне очень понравилось с тобой провести сегодняшний день) да и в целом.."),
        ("Бегимжан", "что? ау-ау?"),
        ("Рауан", "ничего-ничего.."),
        ("Бегимжан", "вот мое такси едет уже"),
        ("Рауан", "пока Бегимжан, спасибо за вечер!"),
        ("Бегимжан", "и тебе спасибо!")
    ]

    # Инициализация первого состояния
    current_dialog = drift_dialog
    dialog_index = 0
    waiting_for_click = True

    running = True
    while running:
        screen.fill(WHITE)
        screen.blit(current_bg, (0, 0))

        # Рисуем диалоговое окно
        pygame.draw.rect(screen, WHITE, dialog_rect, border_radius=10)
        pygame.draw.rect(screen, BLACK, dialog_rect, 3, border_radius=10)

        if scene_state in ["drift_scene", "girl_screaming", "taxi_scene"]:
            if current_dialog and dialog_index < len(current_dialog):
                speaker, message = current_dialog[dialog_index]
                if speaker == "Рауан":
                    speaker_color = BLUE
                elif speaker == "Бегимжан":
                    speaker_color = PINK
                else:
                    speaker_color = GRAY
                speaker_text = small_font.render(f"{speaker}:", True, speaker_color)
                screen.blit(speaker_text, (dialog_rect.x + 20, dialog_rect.y + 10))

                words = message.split(' ')
                lines = []
                current_line = ""
                max_width = dialog_rect.width - 40
                for word in words:
                    test_line = current_line + word + " "
                    if font.size(test_line)[0] < max_width:
                        current_line = test_line
                    else:
                        if current_line:
                            lines.append(current_line.strip())
                            current_line = word + " "
                        else:
                            lines.append(word)
                            current_line = ""
                if current_line:
                    lines.append(current_line.strip())

                for i, line in enumerate(lines):
                    line_text = font.render(line, True, BLACK)
                    screen.blit(line_text, (dialog_rect.x + 20, dialog_rect.y + 35 + i * 20))

                if not waiting_for_click:
                    hint_text = small_font.render("Кликните для продолжения", True, GRAY)
                    screen.blit(hint_text, (dialog_rect.x + 20, dialog_rect.y + 85))

        elif scene_state == "final":
            final_text = font.render("Сцена завершена", True, BLACK)
            screen.blit(final_text, (dialog_rect.x + 20, dialog_rect.y + 35))
            if final_button_rect is None:
                final_button_rect = pygame.Rect(dialog_rect.x + 20, dialog_rect.y + 80, 200, 40)
            pygame.draw.rect(screen, GREEN, final_button_rect, border_radius=5)
            pygame.draw.rect(screen, BLACK, final_button_rect, 2, border_radius=5)
            button_text = font.render("В такси", True, WHITE)
            text_rect = button_text.get_rect(center=final_button_rect.center)
            screen.blit(button_text, text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos

                if scene_state == "drift_scene" and waiting_for_click:
                    if dialog_index < len(current_dialog) - 1:
                        dialog_index += 1
                    else:
                        scene_state = "girl_screaming"
                        current_dialog = girl_screaming_dialog
                        dialog_index = 0
                        waiting_for_click = True

                elif scene_state == "girl_screaming" and waiting_for_click:
                    if dialog_index < len(current_dialog) - 1:
                        dialog_index += 1
                    else:
                        scene_state = "taxi_scene"
                        current_bg = bazar_2_img
                        current_dialog = taxi_dialog
                        dialog_index = 0
                        waiting_for_click = True

                elif scene_state == "taxi_scene" and waiting_for_click:
                    if dialog_index < len(current_dialog) - 1:
                        dialog_index += 1
                    else:
                        scene_state = "final"
                        waiting_for_click = False

                elif scene_state == "final" and final_button_rect:
                    if final_button_rect.collidepoint(mouse_pos):
                        print("Переход к сцене такси")
                        running = False
                        start_taxi_scene(screen)
                        return "taxi"

        pygame.display.flip()
        clock.tick(60)
    return None