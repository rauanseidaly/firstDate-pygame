# sobor.py
import pygame
import os
import time
from meloman import start_meloman_dialog

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (100, 149, 237)
PINK = (255, 182, 193)
GRAY = (200, 200, 200)
GREEN = (100, 180, 100)


def start_sobor_scene(screen):
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 20)
    small_font = pygame.font.SysFont("arial", 16)
    choice_font = pygame.font.SysFont("arial", 18)

    # Загружаем фон
    sobor_img_path = os.path.join("assets", "images", "sobor.png")
    sobor_img = pygame.image.load(sobor_img_path).convert()
    sobor_img = pygame.transform.scale(sobor_img, (screen.get_width(), screen.get_height()))

    # Состояния диалога
    dialog_state = "intro_dialog"  # intro_dialog -> choice -> response -> book_dialog -> final
    current_choice = None

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

    # Диалог о книгах
    book_dialog = [
        ("Бегимжан", "слушай а какие книги ты читаешь?"),
        ("Рауан",
         "на самом деле я не так часто читаю, в последний раз читал в прошлом году - перечитывал \"Богатый папа, бедный папа\". А ты?"),
        ("Бегимжан", "Я вот недавно прочла книгу Юкио Мисисма, но очень хочу новую книгу, может сходим в меломан?")
    ]

    # Начальный диалог
    intro_dialog = [
        ("Бегимжан", "Смотри какую сумочку я недавно купила"),
        ("Рауан", "уааау"),
        ("Бегимжан", "нравится?"),
        ("Рауан", "конечно да")
    ]

    def create_choice_buttons(choices):
        buttons = []
        button_height = 35
        button_margin = 10
        start_y = dialog_rect.y + 35

        for i, choice in enumerate(choices):
            button_rect = pygame.Rect(
                dialog_rect.x + 20,
                start_y + i * (button_height + button_margin),
                dialog_rect.width - 40,
                button_height
            )
            buttons.append((button_rect, choice, i))
        return buttons

    def set_topic_choices():
        choices = [
            "1. О торте в Недельке",
            "2. О учебе",
            "3. О стиле Бегимжанки"
        ]
        return create_choice_buttons(choices)

    def get_topic_dialog(choice_index):
        dialogs = [
            # О торте в Недельке
            [
                ("Рауан", "и как тебе японский пирог в Недельке?"),
                ("Бегимжан", "на самом деле не так плохо"),
                ("Рауан", "а вот мне не понравился, мой наполеон тоже"),
                ("Бегимжан", "да ладно было же вкусно")
            ],
            # О учебе
            [
                ("Рауан", "..ну я пока что изучаю еще.."),
                ("Бегимжан", "а я вот знаю вроде, пайтон, с++"),
                ("Рауан", "да-да, оно самое, я их и изучаю, кстати"),
                ("Бегимжан", "уау, я еще вот 1С знаю вроде"),
                ("Рауан", "это не совсем язык программирование, но да, тоже интересное"),
                ("Бегимжан", "круто"),
                ("Рауан", "уверен что и ты в один день сможешь все изучить")
            ],
            # О стиле Бегимжанки
            [
                ("Рауан", "знаешь, с самого начала я заметил твой лук, мне очень нравится"),
                ("Бегимжан", "правда?"),
                ("Рауан", "да, я был удивлен и не знал что ты так модно одеваешься, кепочка, шарфик, очки"),
                ("Бегимжан", "спасибо")
            ]
        ]
        return dialogs[choice_index]

    # Инициализация первого состояния
    current_dialog = intro_dialog
    dialog_index = 0
    waiting_for_click = True

    running = True
    while running:
        screen.fill(WHITE)
        screen.blit(sobor_img, (0, 0))

        # Рисуем диалоговое окно
        pygame.draw.rect(screen, WHITE, dialog_rect, border_radius=10)
        pygame.draw.rect(screen, BLACK, dialog_rect, 3, border_radius=10)

        if dialog_state == "intro_dialog":
            # Показываем начальный диалог
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

        elif dialog_state == "choice":
            # Показываем выбор темы
            if show_choices:
                title_text = font.render("Как продолжить разговор?", True, BLACK)
                screen.blit(title_text, (dialog_rect.x + 20, dialog_rect.y + 10))

                for button_rect, choice_text, choice_index in choice_buttons:
                    pygame.draw.rect(screen, GRAY, button_rect, border_radius=5)
                    pygame.draw.rect(screen, BLACK, button_rect, 2, border_radius=5)

                    choice_render = choice_font.render(choice_text, True, BLACK)
                    text_rect = choice_render.get_rect(center=button_rect.center)
                    screen.blit(choice_render, text_rect)

        elif dialog_state == "response":
            # Показываем ответный диалог
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
            # Финальный экран и кнопка перехода
            final_text = font.render("Разговор завершен", True, BLACK)
            screen.blit(final_text, (dialog_rect.x + 20, dialog_rect.y + 35))

            if final_button_rect is None:
                final_button_rect = pygame.Rect(dialog_rect.x + 20, dialog_rect.y + 80, 200, 40)

            pygame.draw.rect(screen, GREEN, final_button_rect, border_radius=5)
            pygame.draw.rect(screen, BLACK, final_button_rect, 2, border_radius=5)

            button_text = font.render("Дальше", True, WHITE)
            text_rect = button_text.get_rect(center=final_button_rect.center)
            screen.blit(button_text, text_rect)

        elif dialog_state == "book_dialog":
            # Показываем диалог о книгах
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

        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos

                if dialog_state == "intro_dialog" and waiting_for_click:
                    if dialog_index < len(current_dialog) - 1:
                        dialog_index += 1
                    else:
                        # Переход к выбору
                        dialog_state = "choice"
                        choice_buttons = set_topic_choices()
                        show_choices = True
                        waiting_for_click = False

                elif dialog_state == "choice" and show_choices:
                    for button_rect, choice_text, choice_index in choice_buttons:
                        if button_rect.collidepoint(mouse_pos):
                            current_choice = choice_index
                            current_dialog = get_topic_dialog(choice_index)
                            dialog_index = 0
                            show_choices = False
                            dialog_state = "response"
                            waiting_for_click = True
                            break

                elif dialog_state == "response" and waiting_for_click:
                    if dialog_index < len(current_dialog) - 1:
                        dialog_index += 1
                    else:
                        # Переход к диалогу о книгах
                        dialog_state = "book_dialog"
                        current_dialog = book_dialog
                        dialog_index = 0
                        waiting_for_click = True

                elif dialog_state == "book_dialog" and waiting_for_click:
                    if dialog_index < len(current_dialog) - 1:
                        dialog_index += 1
                    else:
                        # Переход к финалу
                        dialog_state = "final"
                        waiting_for_click = False

                elif dialog_state == "final" and final_button_rect:
                    if final_button_rect.collidepoint(mouse_pos):
                        # Переход к сцене в Меломане
                        start_meloman_dialog(screen)
                        running = False

        pygame.display.flip()
        clock.tick(60)