# night.py
import pygame
import os
import time
from nedelka import start_nedelka_scene

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (100, 149, 237)
PINK = (255, 182, 193)
GRAY = (200, 200, 200)
GREEN = (100, 180, 100)


def start_night_scene(screen):
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 20)
    small_font = pygame.font.SysFont("arial", 16)
    choice_font = pygame.font.SysFont("arial", 18)

    # Загружаем фон
    night_img_path = os.path.join("assets", "images", "night.png")
    night_img = pygame.image.load(night_img_path).convert()
    night_img = pygame.transform.scale(night_img, (screen.get_width(), screen.get_height()))

    # Состояния диалога
    dialog_state = "greeting_choice"  # greeting_choice -> greeting_response -> topic_choice -> topic_response -> final
    current_greeting_choice = None
    current_topic_choice = None

    # Диалоговое окно
    dialog_rect = pygame.Rect(50, screen.get_height() - 200, screen.get_width() - 100, 150)

    # Кнопки выбора
    choice_buttons = []

    # Текущий диалог
    current_dialog = []
    dialog_index = 0
    show_choices = False

    # Переходы между состояниями
    waiting_for_click = False
    final_button_rect = None

    def create_choice_buttons(choices):
        buttons = []
        button_height = 35
        button_margin = 10
        start_y = dialog_rect.y + 35  # увеличил отступ сверху с 20 до 35

        for i, choice in enumerate(choices):
            button_rect = pygame.Rect(
                dialog_rect.x + 20,
                start_y + i * (button_height + button_margin),
                dialog_rect.width - 40,
                button_height
            )
            buttons.append((button_rect, choice, i))
        return buttons

    def set_greeting_choices():
        choices = [
            "1. Ты выглядишь прекрасно!",
            "2. Сегодня прекрасный день",
            "3. Как твои дела?"
        ]
        return create_choice_buttons(choices)

    def set_topic_choices():
        choices = [
            "1. Учеба",
            "2. Работа",
            "3. Зрение"
        ]
        return create_choice_buttons(choices)

    def get_greeting_response(choice_index):
        responses = [
            [("Бегимжан", "Спасибо, ты тоже!")],
            [("Бегимжан", "Согласна с тобой!")],
            [("Бегимжан", "Хорошо, спасибо!")]
        ]
        return responses[choice_index]

    def get_topic_dialog(choice_index):
        dialogs = [
            # Учеба
            [
                ("Рауан", "как дела с учебой?"),
                ("Бегимжан", "да вот летник попала, по физкультуре"),
                ("Рауан", "физкультура? хех, и такое бывает"),
                ("Бегимжан", "да")
            ],
            # Работа
            [
                ("Рауан", "а где ты работаешь?"),
                ("Бегимжан", "вон там здание там сверху надпись есть, в той компании работаю)"),
                ("Рауан", "аа, в том здании?"),
                ("Бегимжан", "нет, на Нурлы-Тау, там офис Фридома")
            ],
            # Зрение
            [
                ("Рауан", "а какое у тебя зрение?"),
                ("Бегимжан", "минус пять)"),
                ("Рауан", "аа хорошо, запомню)")
            ]
        ]
        return dialogs[choice_index]

    # Инициализация первого состояния
    choice_buttons = set_greeting_choices()
    show_choices = True

    running = True
    while running:
        screen.fill(WHITE)
        screen.blit(night_img, (0, 0))

        # Рисуем диалоговое окно
        pygame.draw.rect(screen, WHITE, dialog_rect, border_radius=10)
        pygame.draw.rect(screen, BLACK, dialog_rect, 3, border_radius=10)

        if dialog_state == "greeting_choice":
            # Показываем выборы приветствия
            if show_choices:
                title_text = font.render("Как начать разговор?", True, BLACK)
                screen.blit(title_text, (dialog_rect.x + 20, dialog_rect.y + 5))

                for button_rect, choice_text, choice_index in choice_buttons:
                    pygame.draw.rect(screen, GRAY, button_rect, border_radius=5)
                    pygame.draw.rect(screen, BLACK, button_rect, 2, border_radius=5)

                    choice_render = choice_font.render(choice_text, True, BLACK)
                    text_rect = choice_render.get_rect(center=button_rect.center)
                    screen.blit(choice_render, text_rect)

        elif dialog_state == "greeting_response":
            # Показываем ответ на приветствие
            if current_dialog and dialog_index < len(current_dialog):
                speaker, message = current_dialog[dialog_index]

                speaker_text = small_font.render(f"{speaker}:", True, BLUE if speaker == "Рауан" else PINK)
                screen.blit(speaker_text, (dialog_rect.x + 20, dialog_rect.y + 10))

                message_text = font.render(message, True, BLACK)
                screen.blit(message_text, (dialog_rect.x + 20, dialog_rect.y + 35))

                if not waiting_for_click:
                    hint_text = small_font.render("Кликните для продолжения", True, GRAY)
                    screen.blit(hint_text, (dialog_rect.x + 20, dialog_rect.y + 120))

        elif dialog_state == "topic_choice":
            # Показываем выбор темы
            if show_choices:
                title_text = font.render("О чем спросить?", True, BLACK)
                screen.blit(title_text, (dialog_rect.x + 20, dialog_rect.y + 10))  # изменил с 5 на 10

                for button_rect, choice_text, choice_index in choice_buttons:
                    pygame.draw.rect(screen, GRAY, button_rect, border_radius=5)
                    pygame.draw.rect(screen, BLACK, button_rect, 2, border_radius=5)

                    choice_render = choice_font.render(choice_text, True, BLACK)
                    text_rect = choice_render.get_rect(center=button_rect.center)
                    screen.blit(choice_render, text_rect)

        elif dialog_state == "topic_response":
            # Показываем диалог по выбранной теме
            if current_dialog and dialog_index < len(current_dialog):
                speaker, message = current_dialog[dialog_index]

                speaker_text = small_font.render(f"{speaker}:", True, BLUE if speaker == "Рауан" else PINK)
                screen.blit(speaker_text, (dialog_rect.x + 20, dialog_rect.y + 10))

                # Разбиваем длинное сообщение на строки
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
                    screen.blit(hint_text, (dialog_rect.x + 20, dialog_rect.y + 120))

        elif dialog_state == "final":
            # Финальная фраза и кнопка перехода
            final_text = font.render("давай может зайдем сюда?", True, BLACK)
            screen.blit(final_text, (dialog_rect.x + 20, dialog_rect.y + 35))

            if final_button_rect is None:
                final_button_rect = pygame.Rect(dialog_rect.x + 20, dialog_rect.y + 80, 200, 40)

            pygame.draw.rect(screen, GREEN, final_button_rect, border_radius=5)
            pygame.draw.rect(screen, BLACK, final_button_rect, 2, border_radius=5)

            button_text = font.render("Зайти в кафе", True, WHITE)
            text_rect = button_text.get_rect(center=final_button_rect.center)
            screen.blit(button_text, text_rect)

        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos

                if dialog_state == "greeting_choice" and show_choices:
                    for button_rect, choice_text, choice_index in choice_buttons:
                        if button_rect.collidepoint(mouse_pos):
                            current_greeting_choice = choice_index
                            current_dialog = get_greeting_response(choice_index)
                            dialog_index = 0
                            show_choices = False
                            dialog_state = "greeting_response"
                            waiting_for_click = True
                            break

                elif dialog_state == "greeting_response" and waiting_for_click:
                    if dialog_index < len(current_dialog) - 1:
                        dialog_index += 1
                    else:
                        # Переход к выбору темы
                        dialog_state = "topic_choice"
                        choice_buttons = set_topic_choices()
                        show_choices = True
                        waiting_for_click = False

                elif dialog_state == "topic_choice" and show_choices:
                    for button_rect, choice_text, choice_index in choice_buttons:
                        if button_rect.collidepoint(mouse_pos):
                            current_topic_choice = choice_index
                            current_dialog = get_topic_dialog(choice_index)
                            dialog_index = 0
                            show_choices = False
                            dialog_state = "topic_response"
                            waiting_for_click = True
                            break

                elif dialog_state == "topic_response" and waiting_for_click:
                    if dialog_index < len(current_dialog) - 1:
                        dialog_index += 1
                    else:
                        # Переход к финалу
                        dialog_state = "final"
                        waiting_for_click = False

                elif dialog_state == "final" and final_button_rect:
                    if final_button_rect.collidepoint(mouse_pos):
                        # Переход к следующей сцене
                        start_nedelka_scene(screen)
                        running = False

        pygame.display.flip()
        clock.tick(60)