import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PINK = (255, 182, 193)   # Рауан
MSG_WHITE = (255, 255, 255)  # Бегимжан

# Диалог
dialog = [
    ("Бегимжан", "я тоже работаю иногда онлайн, когда на учебе или сижу с ноутом 😄"),
    ("Бегимжан", "Капеццц 😂"),
    ("Бегимжан", "это уже максимально классно 🤩"),
    ("Рауан", "ну"),
    ("Бегимжан", "Рауан, ты сегодня после работы в 18:00 выходишь?"),
    ("Рауан", "да, а что, пригласить куда-то хочешь? 😁😁"),
    ("Бегимжан", "ахахахахах блин, это было слишком предсказуемо? 😭"),
    ("Рауан", "а я угадал или как?"),
    ("Бегимжан", "да, верно ты угадал... пригласить за кофе ☕"),
    ("Рауан", "планов нет, я за"),
    ("Бегимжан", "мне неловко что я сама приглашаю 🙈"),
    ("Рауан", "мне тоже что меня приглашают"),
    ("Бегимжан", "всё, тогда договорились! 🎉"),
]

STATIC_COUNT = 4  # количество сообщений, которые всегда видны в начале
MAX_PAGE_HEIGHT = 400  # макс. высота сообщений на странице


def run_phone_scene(screen, clock):
    font = pygame.font.SysFont("arial", 20)
    name_font = pygame.font.SysFont("arial", 14)
    small_font = pygame.font.SysFont("arial", 16)

    # Индекс последнего сообщения, которое показываем
    index = STATIC_COUNT - 1
    running = True

    while running:
        screen.fill(WHITE)

        # Отображаем только часть диалога (странично)
        y = 80
        visible_msgs = []
        total_height = 0

        # Сначала берём статические сообщения
        for i in range(STATIC_COUNT):
            visible_msgs.append(dialog[i])

        # Потом — динамически по клику
        for i in range(STATIC_COUNT, index + 1):
            visible_msgs.append(dialog[i])

        # Пагинация: если не влезает — начинаем заново сверху
        page_msgs = []
        for sender, msg in visible_msgs:
            text_height = font.size(msg)[1] + 35  # с отступами
            if total_height + text_height > MAX_PAGE_HEIGHT:
                page_msgs = [(sender, msg)]  # начинаем новую страницу
                total_height = text_height
            else:
                page_msgs.append((sender, msg))
                total_height += text_height

        # Отрисовка сообщений текущей страницы
        for sender, msg in page_msgs:
            color = MSG_WHITE if sender == "Рауан" else PINK

            # Имя
            name_text = name_font.render(sender, True, BLACK)
            if sender == "Рауан":
                screen.blit(name_text, (screen.get_width() - name_text.get_width() - 60, y))
            else:
                screen.blit(name_text, (60, y))
            y += name_text.get_height() + 2

            # Пузырь
            text = font.render(msg, True, BLACK)
            bubble = pygame.Surface((text.get_width() + 20, text.get_height() + 10))
            bubble.fill(color)
            bubble.blit(text, (10, 5))

            if sender == "Рауан":
                screen.blit(bubble, (screen.get_width() - bubble.get_width() - 50, y))
            else:
                screen.blit(bubble, (50, y))
            y += bubble.get_height() + 10

        # Подсказка
        hint_label = small_font.render("Подсказка: Кликните, чтобы продолжить диалог", True, BLACK)
        screen.blit(hint_label, (screen.get_width() - hint_label.get_width() - 10,
                                 screen.get_height() - hint_label.get_height() - 10))

        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if index < len(dialog) - 1:
                    index += 1
                else:
                    running = False

        pygame.display.flip()
        clock.tick(60)
