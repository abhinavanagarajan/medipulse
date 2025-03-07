import pygame
import time
import sys
import os

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Constants
WIDTH = 400
HEIGHT = 400
BLUE = (173, 216, 230)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Breathing Exercise")

# Use default system font instead of Ubuntu font
font = pygame.font.SysFont(None, 36)
timer_font = pygame.font.SysFont(None, 48)

def render_text(text, timer):
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=(WIDTH//2, HEIGHT//4))
    screen.blit(text_surface, text_rect)
    
    timer_surface = timer_font.render(str(timer), True, BLACK)
    timer_rect = timer_surface.get_rect(center=(WIDTH//2, HEIGHT//2))
    screen.blit(timer_surface, timer_rect)

def breathing_cycle():
    try:
        # Breathe In (4 seconds)
        for i in range(40):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
            
            radius = 50 + i * 3
            color = (255 - i * 3, 255, 255)
            screen.fill(color)
            pygame.draw.circle(screen, BLUE, (WIDTH//2, HEIGHT//2), radius)
            render_text("Breathe In", 4 - i // 10)
            pygame.display.flip()
            time.sleep(0.1)
        
        # Hold (7 seconds)
        for t in range(7, 0, -1):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                    
            screen.fill((200, 230, 255))
            pygame.draw.circle(screen, BLUE, (WIDTH//2, HEIGHT//2), 170)
            render_text("Hold...", t)
            pygame.display.flip()
            time.sleep(1)
        
        # Breathe Out (8 seconds)
        for i in range(40, 0, -1):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                    
            radius = 50 + i * 3
            color = (255, 230 - i * 3, 230 - i * 3)
            screen.fill(color)
            pygame.draw.circle(screen, BLUE, (WIDTH//2, HEIGHT//2), radius)
            render_text("Breathe Out", 8 - (40 - i) // 5)
            pygame.display.flip()
            time.sleep(0.1)
        
        return True
        
    except Exception as e:
        print(f"Error in breathing cycle: {e}")
        return False

def main():
    running = True
    while running:
        screen.fill(WHITE)
        running = breathing_cycle()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()