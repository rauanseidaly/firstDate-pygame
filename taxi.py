# taxi.py
import pygame
import os
import time
from outro import start_outro_scene

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (100, 149, 237)
PINK = (255, 182, 193)
GRAY = (200, 200, 200)
GREEN = (100, 180, 100)
DARK_BLUE = (70, 70, 120)


def start_taxi_scene(screen):
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 20)
    small_font = pygame.font.SysFont("arial", 16)
    thoughts_font = pygame.font.SysFont("arial", 18)

    # Загружаем фон
    taxi_img_path = os.path.join("assets", "images", "taxi.png")
    taxi_img = pygame.image.load(taxi_img_path).convert()
    taxi_img = pygame.transform.scale(taxi_img, (screen.get_width(), screen.get_height()))

    # Состояние сцены
    scene_state = "thoughts"
    current_bg = taxi_img

    # Диалоговое окно (высота изменена на 120, позиция - выше)
    dialog_rect = pygame.Rect(50, screen.get_height() - 150, screen.get_width() - 100, 120)

    # Текущий диалог
    current_dialog = []
    dialog_index = 0
    waiting_for_click = False
    final_button_rect = None

    # Диалоги - мысли Рауана
    thoughts_dialog = [
        ("Рауан (мысли)", "Уау, это было очень круто.."),
        ("Рауан (мысли)", "было бы классно продолжить с ней общение и может быть наше общение может вырасти во что-то,"),
        ("Рауан (мысли)", "она очень сильно мне понравилась, но пока я не мог это сказать.."),
        ("Рауан (мысли)", "она такая милая)"),
        ("Рауан (мысли)", "Впервые провел 14 февраля..")
    ]

    # Инициализация первого состояния
    current_dialog = thoughts_dialog
    dialog_index = 0
    waiting_for_click = True

    running = True
    while running:
        screen.fill(WHITE)
        screen.blit(current_bg, (0, 0))

        if scene_state == "thoughts":
            pygame.draw.rect(screen, (240, 240, 255), dialog_rect, border_radius=10)
            pygame.draw.rect(screen, DARK_BLUE, dialog_rect, 3, border_radius=10)
        else:
            pygame.draw.rect(screen, WHITE, dialog_rect, border_radius=10)
            pygame.draw.rect(screen, BLACK, dialog_rect, 3, border_radius=10)

        if scene_state == "thoughts":
            if current_dialog and dialog_index < len(current_dialog):
                speaker, message = current_dialog[dialog_index]
                speaker_text = small_font.render(f"{speaker}:", True, DARK_BLUE)
                screen.blit(speaker_text, (dialog_rect.x + 20, dialog_rect.y + 10))

                words = message.split(' ')
                lines = []
                current_line = ""
                max_width = dialog_rect.width - 40
                for word in words:
                    test_line = current_line + word + " "
                    if thoughts_font.size(test_line)[0] < max_width:
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
                    line_text = thoughts_font.render(line, True, DARK_BLUE)
                    screen.blit(line_text, (dialog_rect.x + 20, dialog_rect.y + 35 + i * 22))

                if not waiting_for_click:
                    hint_text = small_font.render("Кликните для продолжения", True, GRAY)
                    screen.blit(hint_text, (dialog_rect.x + 20, dialog_rect.y + 85))

        elif scene_state == "final":
            final_text = font.render("Размышления в такси закончены", True, BLACK)
            screen.blit(final_text, (dialog_rect.x + 20, dialog_rect.y + 35))
            description_text = small_font.render("Рауан размышляет о прекрасно проведенном дне...", True, GRAY)
            screen.blit(description_text, (dialog_rect.x + 20, dialog_rect.y + 65))
            if final_button_rect is None:
                final_button_rect = pygame.Rect(dialog_rect.x + 20, dialog_rect.y + 80, 200, 40)
            pygame.draw.rect(screen, GREEN, final_button_rect, border_radius=5)
            pygame.draw.rect(screen, BLACK, final_button_rect, 2, border_radius=5)
            button_text = font.render("К финалу", True, WHITE)
            text_rect = button_text.get_rect(center=final_button_rect.center)
            screen.blit(button_text, text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                if scene_state == "thoughts" and waiting_for_click:
                    if dialog_index < len(current_dialog) - 1:
                        dialog_index += 1
                    else:
                        scene_state = "final"
                        waiting_for_click = False

                elif scene_state == "final" and final_button_rect:
                    if final_button_rect.collidepoint(mouse_pos):
                        print("Переход к финальной сцене")
                        running = False
                        start_outro_scene(screen)
                        return "outro"

        pygame.display.flip()
        clock.tick(60)
    return None