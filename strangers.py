# strangers.py
import pygame
import os
import time
from cu import start_cu_scene


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (100, 149, 237)
PINK = (255, 182, 193)
RED = (220, 50, 50)
GRAY = (200, 200, 200)
GREEN = (100, 180, 100)


def start_strangers_scene(screen):
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 20)
    small_font = pygame.font.SysFont("arial", 16)
    narrator_font = pygame.font.SysFont("arial", 18)

    # Загружаем фоны
    stranger_1_img_path = os.path.join("assets", "images", "street_with_begim.png")
    stranger_1_img = pygame.image.load(stranger_1_img_path).convert()
    stranger_1_img = pygame.transform.scale(stranger_1_img, (screen.get_width(), screen.get_height()))

    stranger_2_img_path = os.path.join("assets", "images", "stranger_2.png")
    stranger_2_img = pygame.image.load(stranger_2_img_path).convert()
    stranger_2_img = pygame.transform.scale(stranger_2_img, (screen.get_width(), screen.get_height()))

    # Состояния сцены
    scene_state = "part1"  # part1 -> part2 -> final

    # Диалоговое окно
    dialog_rect = pygame.Rect(50, screen.get_height() - 200, screen.get_width() - 100, 150)

    # Диалоги для первой части
    part1_dialog = [
        ("Рауан",
         "блин так классно, мы словно персонажи из фильма или игры сидели вдвоем в два часа ночи в книжном магазине, общались"),
        ("Бегимжан", "дааа"),
        ("Незнакомец", "ЭЭЭЭЭ Е$#%^($(("),
        ("Бегимжан", "могу взять твою руку?"),
        ("Рауан", "да-да конечно…")
    ]

    # Диалоги для второй части
    part2_dialog = [
        ("Narrator", "Так они прошли еще несколько часов весело общаясь.."),
        ("Рауан", "не хочешь покушать?"),
        ("Бегимжан", "давай")
    ]

    current_dialog = part1_dialog
    dialog_index = 0
    waiting_for_click = True
    final_button_rect = None

    # Время показа нарратора
    narrator_start_time = None
    show_narrator = False
    narrator_duration = 3  # секунды

    def draw_dialog_message(speaker, message, rect):
        # Определяем цвет говорящего
        if speaker == "Рауан":
            speaker_color = BLUE
        elif speaker == "Бегимжан":
            speaker_color = PINK
        elif speaker == "Незнакомец":
            speaker_color = RED
        elif speaker == "Narrator":
            speaker_color = (100, 100, 100)  # серый для нарратора
        else:
            speaker_color = BLACK

        # Отображаем имя говорящего (кроме нарратора)
        y_offset = 10
        if speaker != "Narrator":
            speaker_text = small_font.render(f"{speaker}:", True, speaker_color)
            screen.blit(speaker_text, (rect.x + 20, rect.y + y_offset))
            y_offset += 25

        # Разбиваем длинное сообщение на строки
        words = message.split(' ')
        lines = []
        current_line = ""
        max_width = rect.width - 40

        for word in words:
            test_line = current_line + word + " "
            text_font = narrator_font if speaker == "Narrator" else font
            if text_font.size(test_line)[0] < max_width:
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

        # Отображаем строки
        for i, line in enumerate(lines):
            text_font = narrator_font if speaker == "Narrator" else font
            line_color = speaker_color if speaker == "Narrator" else BLACK
            line_text = text_font.render(line, True, line_color)
            screen.blit(line_text, (rect.x + 20, rect.y + y_offset + i * 22))

    running = True
    while running:
        screen.fill(WHITE)

        # Выбираем фон в зависимости от части
        if scene_state == "part1":
            screen.blit(stranger_1_img, (0, 0))
        else:
            screen.blit(stranger_2_img, (0, 0))

        # Рисуем диалоговое окно
        pygame.draw.rect(screen, WHITE, dialog_rect, border_radius=10)
        pygame.draw.rect(screen, BLACK, dialog_rect, 3, border_radius=10)

        if scene_state == "part1":
            # Показываем диалог первой части
            if current_dialog and dialog_index < len(current_dialog):
                speaker, message = current_dialog[dialog_index]
                draw_dialog_message(speaker, message, dialog_rect)

                if not waiting_for_click:
                    hint_text = small_font.render("Кликните для продолжения", True, GRAY)
                    screen.blit(hint_text, (dialog_rect.x + 20, dialog_rect.y + 120))

        elif scene_state == "part2":
            # Показываем диалог второй части или нарратора
            if show_narrator and narrator_start_time:
                # Показываем нарратор без диалогового окна
                narrator_text = narrator_font.render("Так они прошли еще несколько часов весело общаясь..", True, WHITE)
                # Добавляем тень для лучшей читаемости
                shadow_text = narrator_font.render("Так они прошли еще несколько часов весело общаясь..", True, BLACK)
                screen.blit(shadow_text, (screen.get_width() // 2 - narrator_text.get_width() // 2 + 2,
                                          screen.get_height() // 2 - narrator_text.get_height() // 2 + 2))
                screen.blit(narrator_text, (screen.get_width() // 2 - narrator_text.get_width() // 2,
                                            screen.get_height() // 2 - narrator_text.get_height() // 2))

                # Проверяем, прошло ли достаточно времени
                if time.time() - narrator_start_time >= narrator_duration:
                    show_narrator = False
                    current_dialog = part2_dialog[1:]  # пропускаем нарратора
                    dialog_index = 0
                    waiting_for_click = True

            elif current_dialog and dialog_index < len(current_dialog):
                speaker, message = current_dialog[dialog_index]
                draw_dialog_message(speaker, message, dialog_rect)

                if not waiting_for_click:
                    hint_text = small_font.render("Кликните для продолжения", True, GRAY)
                    screen.blit(hint_text, (dialog_rect.x + 20, dialog_rect.y + 120))

        elif scene_state == "final":
            # Финальная кнопка
            final_text = font.render("История завершена", True, BLACK)
            screen.blit(final_text, (dialog_rect.x + 20, dialog_rect.y + 35))

            if final_button_rect is None:
                final_button_rect = pygame.Rect(dialog_rect.x + 20, dialog_rect.y + 80, 250, 40)

            pygame.draw.rect(screen, GREEN, final_button_rect, border_radius=5)
            pygame.draw.rect(screen, BLACK, final_button_rect, 2, border_radius=5)

            button_text = font.render("Следующая глава", True, WHITE)
            text_rect = button_text.get_rect(center=final_button_rect.center)
            screen.blit(button_text, text_rect)

        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos

                if scene_state == "part1" and waiting_for_click:
                    if dialog_index < len(current_dialog) - 1:
                        dialog_index += 1
                    else:
                        # Переход ко второй части
                        scene_state = "part2"
                        show_narrator = True
                        narrator_start_time = time.time()
                        waiting_for_click = False

                elif scene_state == "part2" and waiting_for_click and not show_narrator:
                    if dialog_index < len(current_dialog) - 1:
                        dialog_index += 1
                    else:
                        # Переход к финалу
                        scene_state = "final"
                        waiting_for_click = False

                elif scene_state == "final" and final_button_rect:
                    if final_button_rect.collidepoint(mouse_pos):
                        start_cu_scene(screen)
                        print("Переход к следующей главе")
                        running = False

        pygame.display.flip()
        clock.tick(60)