import pygame
import numpy as np
import math
from tkinter import Tk, filedialog
from constants import *


# Inicializar Pygame para fuentes
pygame.init()
small_font = pygame.font.Font(None, 18)  # Tamaño de la fuente reducido

# Inicializar Tkinter para el cuadro de diálogo de archivo
Tk().withdraw()

def np_array_to_surface(np_array):
    return pygame.surfarray.make_surface(np_array)

def mirror_and_rotate_image(np_array):
    mirrored = np.fliplr(np_array)  # Invertir como un espejo
    rotated = np.rot90(mirrored, k=1)  # Rotar 90 grados hacia la izquierda
    return rotated

def load_menu_images(original_image, classified_image):
    # Invertir y rotar las imágenes antes de convertirlas
    original_image_processed = mirror_and_rotate_image(original_image)
    classified_image_processed = mirror_and_rotate_image(classified_image)

    # Convertir las imágenes de numpy arrays a superficies de Pygame
    original_surface = np_array_to_surface(original_image_processed)
    classified_surface = np_array_to_surface(classified_image_processed)

    # Escalar las imágenes a miniaturas
    image1 = pygame.transform.scale(original_surface, (70, 70))  # Tamaño reducido
    image2 = pygame.transform.scale(classified_surface, (70, 70))  # Tamaño reducido
    return image1, image2

def load_background_image(background_image):
    # Invertir y rotar la imagen antes de convertirla
    background_image_processed = mirror_and_rotate_image(background_image)

    # Convertir la imagen de fondo de numpy array a superficie de Pygame
    return np_array_to_surface(background_image_processed)

def open_file_dialog(initialdir=None):
    if initialdir:
        file_path = filedialog.askopenfilename(initialdir=initialdir, filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
    else:
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
    return file_path

def draw_grid(screen, grid_width, grid_height):
    for y in range(grid_height):
        for x in range(grid_width):
            rect = pygame.Rect(x + BOARD_X, y + BOARD_Y, 1, 1)
            pygame.draw.rect(screen, WHITE, rect, 1)  # Dibujar borde blanco alrededor de cada celda

def draw_fire_and_fuel(screen, grid, fuel, terrain_map, burned, grid_width, grid_height, background_image, fire_start_positions):
    # Dibujar la imagen de fondo
    screen.blit(background_image, (BOARD_X, BOARD_Y))

    for y in range(grid_height):
        for x in range(grid_width):
            intensity = grid[y][x]

            # Aplicar colores diferentes según el nivel de combustible
            if intensity > 0:
                if fuel[y][x] > 150:
                    color = (255, 0, 0)  # Rojo intenso
                elif fuel[y][x] > 50:
                    color = (255, 165, 0)  # Naranja
                else:
                    color = (255, 255, 0)  # Amarillo
            elif burned[y][x] == 1:
                color = (0, 0, 0)  # Negro para celdas quemadas
            else:
                continue  # No dibujar celdas no quemadas

            # Dibujar la celda del fuego
            pygame.draw.rect(screen, color, (x + BOARD_X, y + BOARD_Y, 1, 1))

    # Dibujar las posiciones de inicio del fuego
    for pos in fire_start_positions:
        pygame.draw.circle(screen, (0, 0, 255), (pos[0] + BOARD_X, pos[1] + BOARD_Y), 5)  # Dibujar un círculo azul en la posición de inicio del fuego

def display_stats(screen, cells_on_fire, updates, burned, total_fuel_used):
    total_cells = len(burned) * len(burned[0])
    cells_burned = sum(sum(row) for row in burned)
    percent_burned = (cells_burned / total_cells) * 100
    wind_text = f"Viento: dirección=({WIND[0]}, {WIND[1]}), intensidad={WIND[2]:.2f}"
    stats_text = small_font.render(
        f"Celdas en llamas: {cells_on_fire} | Actualizaciones: {updates} | % quemado: {percent_burned:.2f} | Combustible usado: {total_fuel_used} | {wind_text}",
        True, (255, 255, 255))
    screen.blit(stats_text, (10, 60))

def draw_wind_controls(screen):
    # Dibujar controles deslizantes para la intensidad del viento
    intensity_slider = pygame.draw.rect(screen, RED, (850, 220, int(WIND[2] * 100), 20))
    pygame.draw.rect(screen, WHITE, (850, 220, 100, 20), 1)

    # Dibujar brújula para la dirección del viento
    center_x, center_y = 900, 155
    radius = 50
    pygame.draw.circle(screen, WHITE, (center_x, center_y), radius, 1)
    directions = [0, 90, 180, 270]
    for angle in directions:
        rad = math.radians(angle)
        x = center_x + radius * math.cos(rad)
        y = center_y + radius * math.sin(rad)  # Ajuste aquí para que las flechas apunten correctamente

        arrow_length = 20
        arrow_width = 10

        # Calcular puntos para el triángulo de la flecha
        arrow_points = [
            (x, y),
            (x - arrow_width * math.sin(rad), y + arrow_width * math.cos(rad)),
            (x + arrow_width * math.sin(rad), y - arrow_width * math.cos(rad))
        ]

        pygame.draw.polygon(screen, WHITE, arrow_points)

    # Dibujar la dirección actual del viento
    wind_angle = math.atan2(WIND[1], WIND[0])
    wind_x = center_x + radius * math.cos(wind_angle) * WIND[2]
    wind_y = center_y + radius * math.sin(wind_angle) * WIND[2]  # Ajuste aquí para que la dirección sea correcta
    pygame.draw.line(screen, RED, (center_x, center_y), (wind_x, wind_y), 2)
def draw_menu(screen, image1, image2, game_speed):
    mouse_pos = pygame.mouse.get_pos()
    # Definir rectángulos de los botones y sus colores
    button_width, button_height = 72, 36
    # Definir rectángulos de los botones y sus colores
    buttons = {
        "start": pygame.Rect(10, 10, button_width, button_height),
        "pause": pygame.Rect(92, 10, button_width, button_height),
        "reset": pygame.Rect(174, 10, button_width, button_height),
        "new": pygame.Rect(256, 10, button_width, button_height),
        "toggle_wind": pygame.Rect(338, 10, button_width+10, button_height),
        "power +": pygame.Rect(430, 10, button_width, button_height),
        "power -": pygame.Rect(512, 10, button_width, button_height)
    }

    # Dibujar botones con efecto hover
    for name, rect in buttons.items():
        color = HOVER_COLOR if rect.collidepoint(mouse_pos) else WHITE
        pygame.draw.rect(screen, color, rect)
        screen.blit(small_font.render(name.replace("_", " ").title(), True, BLACK), (rect.x + 5, rect.y + 10))  # Ajustar posición del texto

    # Dibujar la barra de velocidad
    speed_bar_x, speed_bar_y = 600, 25
    speed_bar_width, speed_bar_height = 100, 10  # Tamaño reducido
    pygame.draw.rect(screen, WHITE, (speed_bar_x, speed_bar_y, speed_bar_width, speed_bar_height))
    pygame.draw.rect(screen, RED, (speed_bar_x, speed_bar_y, int(game_speed / 16.0 * speed_bar_width), speed_bar_height))

    draw_wind_controls(screen)

    # Dibujar las imágenes del menú después de la barra de viento
    screen.blit(image1, (790, 10))  # Ajustar la posición de las miniaturas
    screen.blit(image2, (880, 10))  # Ajustar la posición de las miniaturas

    return buttons["start"], buttons["pause"], buttons["reset"], buttons["new"], buttons["toggle_wind"], \
           buttons["power +"], buttons["power -"], \
           pygame.Rect(790, 10, 50, 50), \
           pygame.Rect(880, 10, 50, 50)
