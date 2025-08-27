import pygame
import os
from phone_dialog import run_phone_scene
from bus import start_bus_scene  # импорт второй главы

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def run_office_scene(screen, clock):
    font = pygame.font.SysFont("arial", 24)
    small_font = pygame.font.SysFont("arial", 16)  # для подсказок

    office_img_path = os.path.join("assets", "images", "office_rauan.png")
    office_img = pygame.image.load(office_img_path).convert_alpha()

    laptop_rect = pygame.Rect(310, 370, 80, 40)   # ноутбук
    phone_rect = pygame.Rect(480, 400, 25, 40)    # телефон
    back_btn_rect = pygame.Rect(10, 10, 180, 40)



    # Кнопка перехода в главу 2
    next_chapter_btn_rect = pygame.Rect(screen.get_width()//2 - 150, screen.get_height()//2, 300, 60)

    current_mission = 1
    running = True
    while running:
        screen.fill(WHITE)
        screen.blit(office_img, (0, 0))

        # Кнопка "Назад"
        pygame.draw.rect(screen, (200, 200, 200), back_btn_rect)
        pygame.draw.rect(screen, BLACK, back_btn_rect, 2)
        back_text = font.render("Вернуться назад", True, BLACK)
        screen.blit(back_text, back_text.get_rect(center=back_btn_rect.center))

        # Миссия справа сверху
        if current_mission == 1:
            mission_text = "Миссия: Закрыть задачу в ноутбуке"
            hint_text = "Кликните по ноутбуку"
        elif current_mission == 2:
            mission_text = "Миссия: Проверить сообщение в телефоне"
            hint_text = "Кликните по телефону"
        else:
            mission_text = "Миссия завершена"
            hint_text = "Нажмите кнопку, чтобы начать главу 2"

        mission_render = font.render(mission_text, True, BLACK)
        screen.blit(mission_render, (screen.get_width() - mission_render.get_width() - 20, 10))

        # Подсказка справа снизу
        hint_label = small_font.render("Подсказка: " + hint_text, True, BLACK)
        screen.blit(hint_label, (screen.get_width() - hint_label.get_width() - 10,
                                 screen.get_height() - hint_label.get_height() - 10))

        # Если миссия завершена — показать кнопку перехода
        if current_mission == 3:
            pygame.draw.rect(screen, (100, 180, 100), next_chapter_btn_rect)
            pygame.draw.rect(screen, BLACK, next_chapter_btn_rect, 2)
            btn_text = font.render("Перейти в главу 2", True, WHITE)
            screen.blit(btn_text, btn_text.get_rect(center=next_chapter_btn_rect.center))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                if back_btn_rect.collidepoint(mouse_pos):
                    running = False
                    break
                if current_mission == 1 and laptop_rect.collidepoint(mouse_pos):
                    current_mission = 2
                elif current_mission == 2 and phone_rect.collidepoint(mouse_pos):
                    run_phone_scene(screen, clock)
                    current_mission = 3
                elif current_mission == 3 and next_chapter_btn_rect.collidepoint(mouse_pos):
                    start_bus_scene(screen)  # запуск второй главы
                    running = False

        pygame.display.flip()
        clock.tick(60)
