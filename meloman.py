# meloman.py
import pygame
import os
import time
from strangers import start_strangers_scene  # добавляем импорт

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (100, 149, 237)
PINK = (255, 182, 193)
GRAY = (200, 200, 200)
GREEN = (100, 180, 100)


def start_meloman_dialog(screen):
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 22)
    small_font = pygame.font.SysFont("arial", 16)

    meloman_img_path = os.path.join("assets", "images", "meloman.png")
    meloman_img = pygame.image.load(meloman_img_path).convert()
    meloman_img = pygame.transform.scale(meloman_img, (screen.get_width(), screen.get_height()))

    dialog_state = "book_dialog"  # здесь сразу начинаем с диалога про книги
    dialog_rect = pygame.Rect(50, screen.get_height() - 200, screen.get_width() - 100, 150)

    # сам диалог
    book_dialog = [
        ("Бегимжан", "какую книги посоветуешь?"),
        ("Рауан", "вообще один из любимых писателей — Ремарк. Читал несколько его книг. "
                  "Очень нравится как он умеет описывать любовь, даже там где война, болезнь, страдания. "
                  "Так красиво описывает истории разных людей, словно так и было в жизни."),
        ("Бегимжан", "да, у меня тоже знакомый любил его книги, говорят интересно."),
        ("Рауан", "а еще мне нравится произведение другого немецкого писателя — Гессе…"),
        ("Бегимжан", "а что насчет этой книги? 1984"),
        ("Рауан", "оо я её читал помню, очень интересно, но очень страшно… страшно, что такое будущее может ждать и нас)"),
        ("Бегимжан", "а что там??"),
        ("Рауан", "прочтёшь — узнаешь)"),
        ("Бегимжан", "тогда берем! но я хочу еще одну книгу."),
        ("Рауан", "давай поищем. А какие книги ты любишь?"),
        ("Бегимжан", "я в целом читаю разные книги, читала японских писателей. "
                     "Помимо Мисимы читала Харуки Мураками. Вот прочтай отрывок из «Мужчины без женщинцы»."),
        ("Рауан", "*читает и потихоньку понимает о чем идет речь в книге… вместе с Бегимжан смеются*"),
        ("Бегимжан", "вот это кажется интересно — «Превращение»."),
        ("Рауан", "тогда берём?)"),
        ("За кадром",
         "Бегимжан и Рауан до покупки книги просидели ещё несколько часов в меломане, "
         "разговаривая о книгах, жизни, религии. В тот момент Рауан начал понимать всю глубину души Бегимжан "
         "и осознал, что перед ним не только красивая девушка, но и очень мудрый и умный человек."),
        ("За кадром",
         "Ему понравилось «как она мыслит», за что в будущем над ними один раз посмеются в стенд-ап клубе). "
         "Этот момент они запомнят на всю жизнь.")
    ]

    dialog_index = 0
    waiting_for_click = True
    final_button_rect = None
    running = True

    while running:
        screen.fill(WHITE)

        # фон из meloman
        screen.blit(meloman_img, (0, 0))

        # рисуем диалоговое окно
        pygame.draw.rect(screen, WHITE, dialog_rect, border_radius=10)
        pygame.draw.rect(screen, BLACK, dialog_rect, 3, border_radius=10)

        if dialog_index < len(book_dialog):
            speaker, message = book_dialog[dialog_index]

            # Цвет для "За кадром"
            if speaker == "За кадром":
                speaker_color = GRAY
            else:
                speaker_color = BLUE if speaker == "Рауан" else PINK

            speaker_text = small_font.render(f"{speaker}:", True, speaker_color)
            screen.blit(speaker_text, (dialog_rect.x + 20, dialog_rect.y + 10))

            # перенос длинных строк
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
                screen.blit(line_text, (dialog_rect.x + 20, dialog_rect.y + 35 + i * 22))

            hint_text = small_font.render("Кликните для продолжения", True, GRAY)
            screen.blit(hint_text, (dialog_rect.x + 20, dialog_rect.y + 120))

        else:
            # финал
            final_text = font.render("Диалог завершён", True, BLACK)
            screen.blit(final_text, (dialog_rect.x + 20, dialog_rect.y + 35))

            if final_button_rect is None:
                final_button_rect = pygame.Rect(dialog_rect.x + 20, dialog_rect.y + 80, 200, 40)

            pygame.draw.rect(screen, GREEN, final_button_rect, border_radius=5)
            pygame.draw.rect(screen, BLACK, final_button_rect, 2, border_radius=5)

            button_text = font.render("Дальше", True, WHITE)
            text_rect = button_text.get_rect(center=final_button_rect.center)
            screen.blit(button_text, text_rect)

        # события
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if dialog_index < len(book_dialog):
                    dialog_index += 1
                elif final_button_rect and final_button_rect.collidepoint(event.pos):
                    # Переход к сцене strangers
                    start_strangers_scene(screen)
                    running = False
                    return

        pygame.display.flip()
        clock.tick(60)