import pygame
import sys
import time
import whereisshe  # файл следующей сцены

def start_bus_scene(screen):
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 36)

    # Загружаем фон автобуса
    bus_image = pygame.image.load("assets/images/bus.png").convert()
    bus_image = pygame.transform.scale(bus_image, (screen.get_width(), screen.get_height()))

    # Звук автобуса (добавь путь позже)
    bus_sound = pygame.mixer.Sound("assets/sounds/bus.MP3")
    pygame.mixer.music.set_volume(0.3)

    start_time = time.time()
    show_button = False
    button_rect = None

    running = True
    while running:
        screen.fill((30, 30, 30))
        screen.blit(bus_image, (0, 0))

        elapsed = time.time() - start_time
        if elapsed >= 8:  # спустя 8 секунд показать кнопку
            show_button = True

        if show_button:
            button_text = font.render("Дальше", True, (255, 255, 255))
            button_rect = pygame.Rect(
                screen.get_width() // 2 - 100,
                screen.get_height() - 100,
                200, 60
            )
            pygame.draw.rect(screen, (100, 100, 200), button_rect, border_radius=10)
            screen.blit(
                button_text,
                (button_rect.centerx - button_text.get_width() // 2,
                 button_rect.centery - button_text.get_height() // 2)
            )

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and show_button:
                if button_rect and button_rect.collidepoint(event.pos):
                    bus_sound.stop()
                    whereisshe.start_whereisshe_scene(screen)
                    return

        pygame.display.flip()
        clock.tick(60)
