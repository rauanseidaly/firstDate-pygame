import pygame
import sys
from office import run_office_scene
from intro import play_intro

# Инициализация
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("First Date: Начало")

pygame.mixer.music.load("assets/sounds/tyler_forgame.MP3")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)  # -1 — бесконечно


clock = pygame.time.Clock()

play_intro(screen)
# Запуск первой сцены (офис)
run_office_scene(screen, clock)

pygame.quit()
sys.exit()
