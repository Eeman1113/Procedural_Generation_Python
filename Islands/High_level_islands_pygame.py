import pygame
import noise
import numpy as np
import time

# Terrain settings
resolution = 500
scale = 45
octaves = 6
persistence = 0.55
lacunarity = 2.0
seed = 0
sea_level = 120

# Pygame settings
width, height = 800, 600
zoom_factor = 1.2
scroll_speed = 50
cell_size = 5

# Define layers
layers = np.array([
    ["blue1", (22, 156, 233), -10],
    ["blue2", (45, 166, 235), -5],
    ["blue3", (68, 176, 238), 0],
    ["beach", (244, 218, 138), 3],
    ["green0", (181, 202, 116), 6],
    ["green1", (116, 186, 94), 25],
    ["green2", (80, 143, 61), 35],
    ["green3", (50, 89, 38), 42],
    ["grey1", (58, 29, 19), 46],
    ["grey2", (92, 61, 61), 52],
    ["snow", (245, 240, 240), 255]
])

class TerrainGenerator:
    def __init__(self, seed=None):
        self.seed = seed if seed is not None else 0

    def get_random_noise(self, scale, shape, octaves, persistence, lacunarity):
        world = np.zeros(shape)
        for i in range(shape[0]):
            for j in range(shape[1]):
                world[i][j] = noise.pnoise2(i / scale, j / scale,
                                            octaves=octaves,
                                            persistence=persistence,
                                            lacunarity=lacunarity,
                                            base=self.seed)
        return ((world + 1) * 128).astype(np.uint8)

    def assign_colors(self, layers, noise_array, sea_level):
        altitudes = (layers[:, 2] + sea_level).astype(int)
        colors = np.array([np.array([*color], dtype=np.uint8) for color in layers[:, 1]])
        color_indices = np.digitize(noise_array, altitudes)
        color_array = np.array([colors[ind] for ind in color_indices])
        return color_array

# Initialize terrain and Pygame
terrain_generator = TerrainGenerator()
noise_array = terrain_generator.get_random_noise(scale, (resolution, resolution), octaves, persistence, lacunarity)
color_array = terrain_generator.assign_colors(layers, noise_array, sea_level)

pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Zoomable Terrain Map")

running = True
zoom_level = 1
dragging = False
offset_x, offset_y = 0, 0

# Convert NumPy array to Pygame surface
terrain_surface = pygame.surfarray.make_surface(color_array)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                zoom_level /= zoom_factor
            elif event.key == pygame.K_RIGHT:
                zoom_level *= zoom_factor
            elif event.key == pygame.K_r:
                # Regenerate noise array on 'r' key press
                noise_array = terrain_generator.get_random_noise(scale, (resolution, resolution), octaves, persistence, lacunarity)
                color_array = terrain_generator.assign_colors(layers, noise_array, sea_level)
                terrain_surface = pygame.surfarray.make_surface(color_array)
            elif event.key == pygame.K_q:
                # Quit on 'q' key press
                running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                dragging = True
                start_x, start_y = event.pos
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if dragging:
                dx, dy = event.rel
                offset_x += dx
                offset_y += dy
    
    screen.fill((255, 255, 255))

    zoomed_width = int(width * zoom_level)
    zoomed_height = int(height * zoom_level)

    # Scale and move the terrain surface
    zoomed_terrain_surface = pygame.transform.scale(terrain_surface, (zoomed_width, zoomed_height))
    zoomed_terrain_rect = zoomed_terrain_surface.get_rect()
    zoomed_terrain_rect.topleft = (offset_x, offset_y)

    # Draw the scaled and moved surface on the screen
    screen.blit(zoomed_terrain_surface, zoomed_terrain_rect)

    pygame.display.flip()

pygame.quit()
