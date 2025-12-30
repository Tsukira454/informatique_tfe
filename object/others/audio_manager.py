import pygame

pygame.mixer.init()

bg_music = None

def play_bg_music(path, volume=1.0, loop=True):
    global bg_music
    if bg_music:
        bg_music.stop()
    bg_music = pygame.mixer.Sound(path)
    bg_music.set_volume(volume)
    bg_music.play(-1 if loop else 0)

def stop_bg_music():
    global bg_music
    if bg_music:
        bg_music.stop()
        bg_music = None

def play_fx(path, volume=1.0):
    fx = pygame.mixer.Sound(path)
    fx.set_volume(volume)
    fx.play()
