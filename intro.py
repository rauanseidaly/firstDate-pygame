import pygame
import sys

def play_intro(screen):
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 60)
    text_surface = font.render("14 февраля 17:28, офис", True, (255, 255, 255))

    alpha = 0
    fading_in = True
    fading_out = False
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill((0, 0, 0))

        text_surface.set_alpha(alpha)
        screen.blit(text_surface, (screen.get_width() // 2 - text_surface.get_width() // 2,
                                   screen.get_height() // 2 - text_surface.get_height() // 2))

        if fading_in:
            alpha += 3
            if alpha >= 255:
                alpha = 255
                fading_in = False
                pygame.time.delay(1000)  # Задержка перед исчезновением
                fading_out = True
        elif fading_out:
            alpha -= 3
            if alpha <= 0:
                alpha = 0
                done = True

        pygame.display.flip()
        clock.tick(60)
