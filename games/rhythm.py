import pygame
import random
import os
import sys

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Game Constants
WIDTH, HEIGHT = 400, 600
TILE_WIDTH, TILE_HEIGHT = 100, 150
FPS = 60
BACKGROUND_COLOR = (200, 230, 250)
TILE_COLOR = (50, 50, 50)

# Load BGM
bgm_path = "lofi-background-music-2-309039.mp3"
if not os.path.exists(bgm_path):
    print("BGM file not found!")
    sys.exit(1)

pygame.mixer.music.load(bgm_path)
pygame.mixer.music.set_volume(0.5)  # Set lower volume for background music
pygame.mixer.music.play(-1)  # Loop the BGM

# Load Keyboard Sound Effect
keyboard_sound_path = "keyboard-click.wav"  # You'll need to provide this sound file
try:
    keyboard_sound = pygame.mixer.Sound(keyboard_sound_path)
    keyboard_sound.set_volume(0.3)  # Set appropriate volume for the effect
except:
    print("Keyboard sound effect file not found! Continuing without sound effects.")
    keyboard_sound = None

def play_keyboard_sound():
    if keyboard_sound:
        keyboard_sound.play()

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rhythmic Tap Challenge")
clock = pygame.time.Clock()

# Tile Creation Function
def create_tile():
    return {'x': random.choice([0, 100, 200, 300]), 'y': -TILE_HEIGHT}

tiles = [create_tile()]
speed = 5
score = 0
music_position = 0  # Keeps track of music progress
running = True
missed = False  # Flag to stop music if missed

def play_next_beat():
    global music_position
    pygame.mixer.music.play(start=music_position)
    music_position += 1.0  # Move music forward by 1 second

while running:
    screen.fill(BACKGROUND_COLOR)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            for tile in tiles:
                if tile['x'] < x < tile['x'] + TILE_WIDTH and tile['y'] < y < tile['y'] + TILE_HEIGHT:
                    tiles.remove(tile)
                    tiles.append(create_tile())
                    play_next_beat()
                    play_keyboard_sound()  # Play keyboard sound
                    score += 1
                    missed = False  # Reset missed flag
                    break

    for tile in tiles:
        pygame.draw.rect(screen, TILE_COLOR, (tile['x'], tile['y'], TILE_WIDTH, TILE_HEIGHT))
        tile['y'] += speed
        if tile['y'] > HEIGHT:
            tiles.remove(tile)
            tiles.append(create_tile())
            missed = True  # Player missed a tile

    if missed:
        pygame.mixer.music.stop()
        music_position = 0  # Reset music

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
