import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH = 800
HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
COLORS = [(0, 0, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]

# Setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Relaxing Doodle")
screen.fill(WHITE)

# Drawing settings
current_color = BLACK
brush_size = 5
drawing = False
last_pos = None

# Create color buttons
color_rects = []
for i, color in enumerate(COLORS):
    color_rects.append(pygame.Rect(10 + i * 60, 10, 50, 50))

# Create clear button
clear_button = pygame.Rect(WIDTH - 100, 10, 90, 50)

def draw_interface():
    # Draw color palette
    for i, (color, rect) in enumerate(zip(COLORS, color_rects)):
        pygame.draw.rect(screen, color, rect)
        if color == current_color:
            pygame.draw.rect(screen, WHITE, rect, 2)  # Highlight selected color
    
    # Draw clear button
    pygame.draw.rect(screen, (200, 200, 200), clear_button)
    font = pygame.font.Font(None, 36)
    text = font.render("Clear", True, BLACK)
    text_rect = text.get_rect(center=clear_button.center)
    screen.blit(text, text_rect)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check color selection
            for i, rect in enumerate(color_rects):
                if rect.collidepoint(event.pos):
                    current_color = COLORS[i]
                    break
            # Check clear button
            if clear_button.collidepoint(event.pos):
                screen.fill(WHITE)
            else:
                drawing = True
                pygame.draw.circle(screen, current_color, event.pos, brush_size)
            last_pos = event.pos
            
        elif event.type == pygame.MOUSEBUTTONUP:
            drawing = False
            
        elif event.type == pygame.MOUSEMOTION and drawing:
            if last_pos:
                pygame.draw.line(screen, current_color, last_pos, event.pos, brush_size * 2)
            last_pos = event.pos
            
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                brush_size = min(brush_size + 1, 50)
            elif event.key == pygame.K_DOWN:
                brush_size = max(brush_size - 1, 1)
    
    # Redraw interface
    draw_interface()
    pygame.display.flip()

pygame.quit()
