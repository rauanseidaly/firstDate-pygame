# cu.py
import pygame
import os
import time
from bazar import start_bazar_scene

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (100, 149, 237)
PINK = (255, 182, 193)
GRAY = (200, 200, 200)
GREEN = (100, 180, 100)


def start_cu_scene(screen):
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 20)
    small_font = pygame.font.SysFont("arial", 16)
    choice_font = pygame.font.SysFont("arial", 18)

    # Загружаем фоны
    cu_img_path = os.path.join("assets", "images", "cu.png")
    cu_img = pygame.image.load(cu_img_path).convert()
    cu_img = pygame.transform.scale(cu_img, (screen.get_width(), screen.get_height()))

    cu_kimpap_img_path = os.path.join("assets", "images", "cu_kimpap.png")
    cu_kimpap_img = pygame.image.load(cu_kimpap_img_path).convert()
    cu_kimpap_img = pygame.transform.scale(cu_kimpap_img, (screen.get_width(), screen.get_height()))

    cu_kormil_img_path = os.path.join("assets", "images", "cu_kormil.png")
    cu_kormil_img = pygame.image.load(cu_kormil_img_path).convert()
    cu_kormil_img = pygame.transform.scale(cu_kormil_img, (screen.get_width(), screen.get_height()))

    # Состояние сцены
    scene_state = "intro_dialog"
    current_choice = None
    current_bg = cu_img

    # Диалоговое окно (расположено ниже)
    dialog_rect = pygame.Rect(50, screen.get_height() - 600, screen.get_width() - 100, 120)

    # Кнопки выбора
    choice_buttons = []

    # Текущий диалог
    current_dialog = []
    dialog_index = 0
    show_choices = False

    # Флаги для управления переходами
    waiting_for_click = False
    show_button = False
    final_button_rect = None

    # Диалоги
    intro_dialog = [
        ("Рауан", "вообще-то я не фанат корейской еды, я вообще не умею выбирать, кушать и держа…")
    ]

    kimpap_dialog = [
        ("Бегимжан", "хах, ничего страшного)")
    ]

    kormil_dialog = [
        ("Рауан", "мне стыдно и я не могу, давай нет, я не хочу"),
        ("Бегимжан", "да ладно тебе, в следующий раз колымды кайтарма!")
    ]

    final_dialog = [
        ("Рауан", "фух, вроде наелись, ну что пойдем дальше?")
    ]

    def create_choice_buttons(choices):
        buttons = []
        button_height = 30
        button_margin = 8
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
            "1. Ру",
            "2. Школа",
            "3. Семья"
        ]
        return create_choice_buttons(choices)

    def get_topic_dialog(choice_index):
        dialogs = [
            # Ру
            [
                ("Рауан", "а какой у тебя ру?"),
                ("Бегимжан", "у мен ру керей, ал сенде?"),
                ("Рауан", "мен жалайырмын, получается мы оба были в учебнике 8 класса по истории) "
                          "я просто был в олимпийской команде по истории казахстана"),
                ("Бегимжан", "да? я не знала..")
            ],
            # Школа
            [
                ("Рауан", "скажи, а где ты училась, тут?"),
                ("Бегимжан", "да, я закончила школу тут"),
                ("Рауан", "аа, я в Астане только учился"),
                ("Бегимжан", "я кстати в Астане тоже училась, но закончила тут")
            ],
            # Семья
            [
                ("Рауан", "а сколько вас в семье?"),
                ("Бегимжан", "нас 4 детей, младший брат ему 18 будет и две сестренки"),
                ("Рауан", "ааа, нас в семье 3, включая меня, сестренка, ей 18 и братишка 12."),
                ("Бегимжан", "моей сестренке тоже 12!!")
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
        screen.blit(current_bg, (0, 0))

        # Рисуем диалоговое окно
        pygame.draw.rect(screen, WHITE, dialog_rect, border_radius=10)
        pygame.draw.rect(screen, BLACK, dialog_rect, 3, border_radius=10)

        # Логика отображения диалогов
        if scene_state in ["intro_dialog", "kimpap_scene", "kormil_scene", "topic_response", "final"]:
            if not show_button:
                if current_dialog and dialog_index < len(current_dialog):
                    speaker, message = current_dialog[dialog_index]
                    speaker_color = BLUE if speaker == "Рауан" else PINK if speaker == "Бегимжан" else GRAY
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

                    if waiting_for_click:
                        hint_text = small_font.render("Кликните для продолжения", True, GRAY)
                        screen.blit(hint_text, (dialog_rect.x + 20, dialog_rect.y + 85))
                else:
                    show_button = True

            if show_button:
                final_text = font.render("Сцена завершена", True, BLACK)
                screen.blit(final_text, (dialog_rect.x + 20, dialog_rect.y + 35))

                if final_button_rect is None:
                    final_button_rect = pygame.Rect(dialog_rect.x + 20, dialog_rect.y + 80, 200, 40)

                pygame.draw.rect(screen, GREEN, final_button_rect, border_radius=5)
                pygame.draw.rect(screen, BLACK, final_button_rect, 2, border_radius=5)

                button_text = font.render("Дальше", True, WHITE)
                text_rect = button_text.get_rect(center=final_button_rect.center)
                screen.blit(button_text, text_rect)

        elif scene_state == "choice":
            if show_choices:
                title_text = font.render("О чем поговорить?", True, BLACK)
                screen.blit(title_text, (dialog_rect.x + 20, dialog_rect.y + 10))

                for button_rect, choice_text, choice_index in choice_buttons:
                    pygame.draw.rect(screen, GRAY, button_rect, border_radius=5)
                    pygame.draw.rect(screen, BLACK, button_rect, 2, border_radius=5)
                    choice_render = choice_font.render(choice_text, True, BLACK)
                    text_rect = choice_render.get_rect(center=button_rect.center)
                    screen.blit(choice_render, text_rect)

        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos

                if scene_state == "intro_dialog" and waiting_for_click:
                    if dialog_index < len(current_dialog) - 1:
                        dialog_index += 1
                    else:
                        scene_state = "kimpap_scene"
                        current_bg = cu_kimpap_img
                        current_dialog = kimpap_dialog
                        dialog_index = 0
                        waiting_for_click = True

                elif scene_state == "kimpap_scene" and waiting_for_click:
                    if dialog_index < len(current_dialog) - 1:
                        dialog_index += 1
                    else:
                        scene_state = "kormil_scene"
                        current_bg = cu_kormil_img
                        current_dialog = kormil_dialog
                        dialog_index = 0
                        waiting_for_click = True

                elif scene_state == "kormil_scene" and waiting_for_click:
                    if dialog_index < len(current_dialog) - 1:
                        dialog_index += 1
                    else:
                        scene_state = "choice"
                        current_bg = cu_img
                        choice_buttons = set_topic_choices()
                        show_choices = True
                        waiting_for_click = False

                elif scene_state == "choice" and show_choices:
                    for button_rect, choice_text, choice_index in choice_buttons:
                        if button_rect.collidepoint(mouse_pos):
                            current_choice = choice_index
                            current_dialog = get_topic_dialog(choice_index)
                            dialog_index = 0
                            show_choices = False
                            scene_state = "topic_response"
                            waiting_for_click = True
                            break

                elif scene_state == "topic_response" and waiting_for_click:
                    if dialog_index < len(current_dialog) - 1:
                        dialog_index += 1
                    else:
                        scene_state = "final"
                        current_dialog = final_dialog
                        dialog_index = 0
                        waiting_for_click = True
                        show_button = False

                elif scene_state == "final" and waiting_for_click:
                    if dialog_index < len(current_dialog) - 1:
                        dialog_index += 1
                    else:
                        show_button = True
                        waiting_for_click = False

                elif show_button and final_button_rect:
                    if final_button_rect.collidepoint(mouse_pos):
                        print("Переход к сцене базар")
                        running = False
                        start_bazar_scene(screen)
                        return "bazar"

        pygame.display.flip()
        clock.tick(60)
    return None