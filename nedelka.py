# nedelka.py
import pygame
import os
import time
from sobor import start_sobor_scene


def start_nedelka_scene(screen):
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 36)

    # Загружаем изображение
    nedelka_img_path = os.path.join("assets", "images", "nedelka.png")
    nedelka_img = pygame.image.load(nedelka_img_path).convert()

    # Исходные размеры изображения
    original_width = nedelka_img.get_width()
    original_height = nedelka_img.get_height()

    # Начальный масштаб (изображение на весь экран)
    screen_width = screen.get_width()
    screen_height = screen.get_height()

    # Вычисляем начальный масштаб для заполнения экрана
    scale_x = screen_width / original_width
    scale_y = screen_height / original_height
    initial_scale = max(scale_x, scale_y)  # берем больший масштаб для заполнения

    # Параметры зума
    current_scale = initial_scale
    zoom_speed = 0.0005  # очень медленная скорость зума
    max_scale = initial_scale * 1.3  # максимальный зум (130% от начального)

    # Звук
    try:
        nedelka_sound = pygame.mixer.Sound(os.path.join("assets", "sounds", "nedelka.mp3"))
        nedelka_sound.play()
        pygame.mixer.music.set_volume(0.4)
    except:
        print("Звуковой файл nedelka.mp3 не найден")

    # Кнопка "Дальше" (появляется через некоторое время)
    start_time = time.time()
    show_button = False
    button_rect = None

    running = True
    while running:
        screen.fill((0, 0, 0))  # черный фон

        # Медленный зум
        if current_scale < max_scale:
            current_scale += zoom_speed

        # Масштабируем изображение
        scaled_width = int(original_width * current_scale)
        scaled_height = int(original_height * current_scale)
        scaled_img = pygame.transform.scale(nedelka_img, (scaled_width, scaled_height))

        # Центрируем изображение
        img_x = (screen_width - scaled_width) // 2
        img_y = (screen_height - scaled_height) // 2

        screen.blit(scaled_img, (img_x, img_y))

        # Показываем кнопку через 10 секунд
        elapsed = time.time() - start_time
        if elapsed >= 10:
            show_button = True

        if show_button:
            button_text = font.render("Дальше", True, (255, 255, 255))
            button_rect = pygame.Rect(
                screen.get_width() // 2 - 100,
                screen.get_height() - 100,
                200, 60
            )
            # Полупрозрачная кнопка для лучшей видимости
            button_surface = pygame.Surface((200, 60))
            button_surface.set_alpha(180)
            button_surface.fill((50, 50, 100))
            screen.blit(button_surface, button_rect.topleft)

            pygame.draw.rect(screen, (100, 100, 200), button_rect, 3, border_radius=10)
            screen.blit(
                button_text,
                (button_rect.centerx - button_text.get_width() // 2,
                 button_rect.centery - button_text.get_height() // 2)
            )

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and show_button:
                if button_rect and button_rect.collidepoint(event.pos):
                    # Останавливаем звук
                    try:
                        nedelka_sound.stop()
                    except:
                        pass

                    # Переход к следующей сцене
                    start_sobor_scene(screen)
                    running = False
                    return
            elif event.type == pygame.KEYDOWN:
                # Возможность пропустить сцену нажатием любой клавиши
                if event.key == pygame.K_SPACE or event.key == pygame.K_ESCAPE:
                    try:
                        nedelka_sound.stop()
                    except:
                        pass
                    running = False
                    return

        pygame.display.flip()
        clock.tick(60)