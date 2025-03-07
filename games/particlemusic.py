import pygame
import numpy as np
import wave
import struct

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Screen settings
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Lofi Waveform Visualizer")

# Load lofi beats and extract audio data
def get_audio_waveform():
    try:
        with wave.open("lofi_beats.wav", "rb") as wf:
            frame_rate = wf.getframerate()
            chunk_size = frame_rate // 30  # Adjusted for smoother motion
            while True:
                frames = wf.readframes(chunk_size)
                if not frames:
                    wf.rewind()
                    continue
                samples = struct.unpack("<" + ("h" * (len(frames) // 2)), frames)
                yield np.array(samples) / 32768.0  # Normalize between -1 and 1
    except Exception as e:
        print("Error processing audio:", e)
        while True:
            yield np.zeros(100)  # Prevents crashing if audio fails

waveform_generator = get_audio_waveform()

# Play music using pygame.mixer
pygame.mixer.music.load("lofi_beats.wav")
pygame.mixer.music.play(-1)  # Loop indefinitely

def draw_waveform(samples):
    screen.fill((240, 240, 255))  # Light pastel background
    num_samples = len(samples)
    step = max(1, num_samples // 100)  # Fewer bars for aesthetic spacing
    bar_width = WIDTH // 100
    center_y = HEIGHT // 2
    max_height = HEIGHT // 3  # Control amplitude

    for i in range(100):
        x = i * bar_width
        sample_index = i * step
        amplitude = abs(samples[sample_index]) * max_height
        y_top = int(center_y - amplitude)
        y_bottom = int(center_y + amplitude)
        color = (255 - i * 2, 100 + i, 200)  # Gradient effect from pink to blue
        pygame.draw.line(screen, color, (x, y_top), (x, y_bottom), bar_width // 2)

clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
    
    samples = next(waveform_generator)
    draw_waveform(samples)
    
    pygame.display.flip()
    clock.tick(30)  # Smooth animation

pygame.mixer.music.stop()
pygame.quit()