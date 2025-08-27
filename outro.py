# outro.py
import pygame
import sys
import os
import time

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PINK = (255, 192, 203)
GRAY = (200, 200, 200)


def start_outro_scene(screen):
    running = True
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 20)
    small_font = pygame.font.SysFont("arial", 16)

    # Загружаем фон, если есть
    try:
        outro_img_path = os.path.join("assets", "images", "outro.png")
        outro_img = pygame.image.load(outro_img_path).convert()
        outro_img = pygame.transform.scale(outro_img, (screen.get_width(), screen.get_height()))
        use_image = True
    except pygame.error:
        print("Фон outro.png не найден, будет использоваться черный экран.")
        use_image = False

    # Диалоговое окно внизу
    dialog_rect = pygame.Rect(50, screen.get_height() - 200, screen.get_width() - 100, 150)
    dialog_index = 0
    current_line = 0

    # Разбиваем текст на части для отображения в диалоговом окне
    full_text = "Ну что же, моя дорогая Бегимжан! Поздравляю нас с такой датой! Думаю что мы большие молодцы, мы многое успели испытать и увидеть, главное что вместе! Осылай журе берейык бирге, жаным! Это игра посвящена тебе! Нам! Люблю тебя!"

    # Разбиваем текст на строки для отображения в диалоговом окне
    words = full_text.split(' ')
    text_lines = []
    current_line_text = ""
    max_width = dialog_rect.width - 40

    for word in words:
        test_line = current_line_text + word + " "
        if font.size(test_line)[0] < max_width:
            current_line_text = test_line
        else:
            if current_line_text:
                text_lines.append(current_line_text.strip())
                current_line_text = word + " "
            else:
                text_lines.append(word)
                current_line_text = ""
    if current_line_text:
        text_lines.append(current_line_text.strip())

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if current_line < len(text_lines) - 1:
                    current_line += 1
                else:
                    running = False

        if use_image:
            screen.blit(outro_img, (0, 0))
        else:
            screen.fill(BLACK)

        # Рисуем диалоговое окно
        pygame.draw.rect(screen, WHITE, dialog_rect, border_radius=10)
        pygame.draw.rect(screen, BLACK, dialog_rect, 3, border_radius=10)

        # Отображаем текст построчно в диалоговом окне
        for i in range(min(5, len(text_lines) - current_line)):
            if current_line + i < len(text_lines):
                line_text = font.render(text_lines[current_line + i], True, BLACK)
                screen.blit(line_text, (dialog_rect.x + 20, dialog_rect.y + 15 + i * 25))

        # Подсказка для продолжения или выхода
        if current_line < len(text_lines) - 1:
            hint_text = small_font.render("Кликните для продолжения", True, GRAY)
            screen.blit(hint_text, (dialog_rect.x + 20, dialog_rect.y + 130))
        else:
            hint_text = small_font.render("Кликните, чтобы выйти", True, GRAY)
            screen.blit(hint_text, (dialog_rect.x + 20, dialog_rect.y + 130))

        pygame.display.flip()
        clock.tick(60)

    # Выход из игры
    pygame.quit()
    sys.exit()