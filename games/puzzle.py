import pygame
import random
import os

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
GRID_SIZE = 4
TILE_SIZE = min((WIDTH - 200) // GRID_SIZE, HEIGHT // GRID_SIZE)  # 200px reserved for preview panel
BACKGROUND_COLOR = (240, 240, 255)

# Add new constants for victory screen
VICTORY_COLOR = (0, 0, 0, 180)  # Semi-transparent black
VICTORY_TEXT_COLOR = (255, 255, 255)
VICTORY_FONT_SIZE = 48
BUTTON_COLOR = (70, 130, 180)
BUTTON_HOVER_COLOR = (100, 160, 210)

# Load or create puzzle image
def load_puzzle_image():
    if os.path.exists("puzzle_image.png"):
        image = pygame.image.load("puzzle_image.png")
    else:
        print("No puzzle_image.png found, using default pattern")
        image = pygame.Surface((TILE_SIZE * GRID_SIZE, TILE_SIZE * GRID_SIZE))
        image.fill((200, 200, 255))
    return pygame.transform.scale(image, (TILE_SIZE * GRID_SIZE, TILE_SIZE * GRID_SIZE))

image = load_puzzle_image()

class PuzzleTile:
    def __init__(self, image, correct_pos):
        self.image = image
        self.correct_pos = correct_pos
        self.current_pos = None
        self.rect = pygame.Rect(0, 0, TILE_SIZE, TILE_SIZE)
        self.is_dragging = False
        self.drag_offset = (0, 0)

# Split image into tiles
def split_image(image):
    tiles = []
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            x, y = col * TILE_SIZE, row * TILE_SIZE
            rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
            tile = image.subsurface(rect).copy()
            tiles.append(PuzzleTile(tile, (col, row)))
    random.shuffle(tiles)
    return tiles

tiles = split_image(image)
preview_index = 0  # Index for previewed piece

# Create game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Relaxing Jigsaw Puzzle")

# Draw grid
def draw_grid():
    for x in range(0, GRID_SIZE * TILE_SIZE, TILE_SIZE):
        pygame.draw.line(screen, (0, 0, 0), (x, 0), (x, GRID_SIZE * TILE_SIZE))
    for y in range(0, GRID_SIZE * TILE_SIZE, TILE_SIZE):
        pygame.draw.line(screen, (0, 0, 0), (0, y), (GRID_SIZE * TILE_SIZE, y))

# Draw tiles on the board
def draw_tiles():
    for tile in tiles:
        if tile.current_pos and not tile.is_dragging:
            x, y = tile.current_pos[0] * TILE_SIZE, tile.current_pos[1] * TILE_SIZE
            screen.blit(tile.image, (x, y))
            tile.rect.topleft = (x, y)
    # Draw dragged tile last (on top)
    for tile in tiles:
        if tile.is_dragging:
            screen.blit(tile.image, tile.rect.topleft)

# Draw preview panel
def draw_preview():
    pygame.draw.rect(screen, (200, 200, 200), (GRID_SIZE * TILE_SIZE, 0, 200, HEIGHT))
    font = pygame.font.Font(None, 30)
    text = font.render("Preview", True, (0, 0, 0))
    screen.blit(text, (GRID_SIZE * TILE_SIZE + 70, 20))
    
    # Fix: Access PuzzleTile object properties correctly
    if preview_index < len(tiles) and tiles[preview_index].current_pos is None:
        preview_tile = tiles[preview_index]
        screen.blit(preview_tile.image, (GRID_SIZE * TILE_SIZE + 50, 100))
    
    next_button = font.render("Next", True, (0, 0, 0))
    screen.blit(next_button, (GRID_SIZE * TILE_SIZE + 70, 500))

# Get tile position
def get_tile_pos(mouse_pos):
    x, y = mouse_pos[0] // TILE_SIZE, mouse_pos[1] // TILE_SIZE
    return (x, y) if x < GRID_SIZE and y < GRID_SIZE else None

# Check if puzzle is completed
def check_completion():
    return all(tile.current_pos == tile.correct_pos for tile in tiles)

# Add after existing constants
victory_screen = False
button_rect = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 + 50, 200, 50)

def draw_victory_screen():
    # Create semi-transparent overlay
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill(VICTORY_COLOR)
    screen.blit(overlay, (0,0))
    
    # Victory text
    font = pygame.font.Font(None, VICTORY_FONT_SIZE)
    text = font.render("Puzzle Completed!", True, VICTORY_TEXT_COLOR)
    text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2 - 50))
    screen.blit(text, text_rect)
    
    # Draw restart button
    mouse_pos = pygame.mouse.get_pos()
    button_color = BUTTON_HOVER_COLOR if button_rect.collidepoint(mouse_pos) else BUTTON_COLOR
    pygame.draw.rect(screen, button_color, button_rect, border_radius=10)
    
    # Button text
    button_font = pygame.font.Font(None, 36)
    button_text = button_font.render("Play Again", True, VICTORY_TEXT_COLOR)
    button_text_rect = button_text.get_rect(center=button_rect.center)
    screen.blit(button_text, button_text_rect)

def reset_puzzle():
    global tiles, preview_index, victory_screen
    tiles = split_image(image)
    preview_index = 0
    victory_screen = False

# Main game loop
running = True
dragging_tile = None
mouse_pos = (0, 0)

while running:
    screen.fill(BACKGROUND_COLOR)
    
    if not victory_screen:
        # Update dragged tile position
        if dragging_tile:
            dragging_tile.rect.topleft = (
                mouse_pos[0] - dragging_tile.drag_offset[0],
                mouse_pos[1] - dragging_tile.drag_offset[1]
            )
        
        draw_tiles()
        draw_grid()
        draw_preview()
        
        if check_completion():
            victory_screen = True
            pygame.mixer.music.load("victory.wav") if os.path.exists("victory.wav") else None
            pygame.mixer.music.play() if os.path.exists("victory.wav") else None
    else:
        # Draw completed puzzle in background
        draw_tiles()
        draw_grid()
        draw_victory_screen()
    
    pygame.display.flip()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if victory_screen:
                if button_rect.collidepoint(event.pos):
                    reset_puzzle()
            else:
                mouse_pos = event.pos
                # Check for Next button click
                if (GRID_SIZE * TILE_SIZE + 70 <= mouse_pos[0] <= GRID_SIZE * TILE_SIZE + 170 and 
                    500 <= mouse_pos[1] <= 530):
                    # Find next unplaced tile
                    for i in range(len(tiles)):
                        preview_index = (preview_index + 1) % len(tiles)
                        if tiles[preview_index].current_pos is None:
                            break
                else:
                    tile_pos = get_tile_pos(mouse_pos)
                    
                    # Try to pick up a tile from the board
                    if tile_pos:
                        for tile in tiles:
                            if tile.current_pos == tile_pos:
                                dragging_tile = tile
                                tile.is_dragging = True
                                tile.drag_offset = (
                                    mouse_pos[0] - tile.current_pos[0] * TILE_SIZE,
                                    mouse_pos[1] - tile.current_pos[1] * TILE_SIZE
                                )
                                break
                    # Check preview panel click
                    elif (GRID_SIZE * TILE_SIZE < mouse_pos[0] < WIDTH and 
                          100 < mouse_pos[1] < 100 + TILE_SIZE and 
                          preview_index < len(tiles) and 
                          not tiles[preview_index].current_pos):
                        dragging_tile = tiles[preview_index]
                        dragging_tile.is_dragging = True
                        dragging_tile.drag_offset = (TILE_SIZE // 2, TILE_SIZE // 2)
            
        elif event.type == pygame.MOUSEMOTION:
            if not victory_screen:
                mouse_pos = event.pos
            
        elif event.type == pygame.MOUSEBUTTONUP:
            if not victory_screen:
                if dragging_tile:
                    tile_pos = get_tile_pos(mouse_pos)
                    if tile_pos:
                        # Check if there's already a tile at the target position
                        existing_tile = next((t for t in tiles if t.current_pos == tile_pos), None)
                        if existing_tile:
                            # Swap positions
                            existing_tile.current_pos, dragging_tile.current_pos = (
                                dragging_tile.current_pos,
                                tile_pos
                            )
                        else:
                            dragging_tile.current_pos = tile_pos
                    
                    dragging_tile.is_dragging = False
                    dragging_tile = None
                    
                    if check_completion():
                        print("Puzzle Completed!")
                        # You could add a victory animation or message here

pygame.quit()
