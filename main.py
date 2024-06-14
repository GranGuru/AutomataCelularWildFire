import pygame
import sys
import os
import random
import time
from soil_classification import classify_soil, process_new_image, resize_and_crop_image
from fire_simulation import initialize_fire_and_fuel, update_fire
from gui import draw_fire_and_fuel, display_stats, draw_menu, load_menu_images, load_background_image, open_file_dialog
from constants import *
import tensorflow as tf
from unet_model import *

model_path = "_internal//model_unet//unet_model_final.h5"
custom_objects = {'dice_coefficient': dice_coefficient, 'dice_loss': dice_loss, 'EncoderBlock': EncoderBlock,
                  'DecoderBlock': DecoderBlock}
unet_model = tf.keras.models.load_model(model_path, custom_objects=custom_objects)

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller crea una carpeta temporal y almacena la ruta en _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Inicializar Pygame
pygame.init()

def update_window_size(new_width, new_height):
    global WINDOW_WIDTH, WINDOW_HEIGHT, screen
    WINDOW_WIDTH, WINDOW_HEIGHT = new_width+150, new_height + 150
    # Asegurarse de que las dimensiones mínimas sean 800x600
    if WINDOW_WIDTH < 1000:
        WINDOW_WIDTH = 1000
    if WINDOW_HEIGHT < 600:
        WINDOW_HEIGHT = 600
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# Clasificar el suelo y ajustar los colores según el riesgo de incendio
try:
    original_image, classified_image, risk_map = classify_soil(SIERRA_IMAGE_PATH, unet_model)
except FileNotFoundError as e:
    print(e)
    sys.exit()

# Configurar la ventana
WINDOW_WIDTH, WINDOW_HEIGHT = original_image.shape[1], original_image.shape[0]
# Asegurarse de que las dimensiones mínimas sean 800x600
if WINDOW_WIDTH < 1000:
    WINDOW_WIDTH = 1000
if WINDOW_HEIGHT < 600:
    WINDOW_HEIGHT = 600

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Simulación de Incendios sobre Imágenes Aéreas - Deep Learning Unet - Automata Celular")

# Inicializar el grid del fuego, el combustible, el escudo y el registro de celdas quemadas
GRID_WIDTH = original_image.shape[1]
GRID_HEIGHT = original_image.shape[0]

fire_grid, fuel_grid, shield = initialize_fire_and_fuel(GRID_WIDTH, GRID_HEIGHT, risk_map)
burned = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
updates = 0
total_fuel_used = 0
running = True
paused = True
fire_started = False
fire_start_positions = []  # Inicializar lista de posiciones de inicio del fuego
cells_on_fire = 0  # Inicializar cells_on_fire
game_speed = 1.0  # Inicializar la velocidad del juego, 1.0x velocidad normal

# Cargar imágenes del menú
image1, image2 = load_menu_images(original_image, classified_image)

# Convertir las imágenes de numpy arrays a superficies de Pygame
background_surface = load_background_image(original_image)
current_background = original_image  # Empezar con la imagen 1 como fondo

last_wind_change = time.time()
last_update_time = time.time()

def randomize_wind():
    WIND[0] = random.choice([-1, 0, 1])
    WIND[1] = random.choice([-1, 0, 1])
    WIND[2] = random.uniform(0.0, 1.0)

# Bucle principal del juego
while running:
    current_time = time.time()
    if WIND_RANDOM and current_time - last_wind_change > WIND_CHANGE_INTERVAL:
        randomize_wind()
        last_wind_change = current_time

    # Llama a draw_menu para definir los botones antes de usarlos
    start_button, pause_button, reset_button, new_button, toggle_wind_button, increase_speed_button, decrease_speed_button, image1_rect, image2_rect = draw_menu(
        screen, image1, image2, game_speed)  # Dibujar el menú

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                WIND[0] = -1
                WIND[1] = 0
            elif event.key == pygame.K_RIGHT:
                WIND[0] = 1
                WIND[1] = 0
            elif event.key == pygame.K_UP:
                WIND[0] = 0
                WIND[1] = -1
            elif event.key == pygame.K_DOWN:
                WIND[0] = 0
                WIND[1] = 1
            elif event.key == pygame.K_EQUALS or event.key == pygame.K_PLUS:
                WIND[2] = min(WIND[2] + 0.1, 1.0)  # Incrementar intensidad
            elif event.key == pygame.K_MINUS:
                WIND[2] = max(WIND[2] - 0.1, 0.0)  # Decrementar intensidad
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if start_button.collidepoint(mouse_pos):
                paused = False
                fire_started = True
                for pos in fire_start_positions:
                    x, y = pos
                    fire_grid[y][x] = 255  # Iniciar fuego en las posiciones especificadas
            elif pause_button.collidepoint(mouse_pos):
                paused = True
            elif reset_button.collidepoint(mouse_pos):
                fire_grid, fuel_grid, shield = initialize_fire_and_fuel(GRID_WIDTH, GRID_HEIGHT, risk_map)
                burned = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
                updates = 0
                total_fuel_used = 0
                paused = True
                fire_started = False
                fire_start_positions = []  # Reiniciar la lista de posiciones de inicio del fuego
            elif toggle_wind_button.collidepoint(mouse_pos):
                WIND_RANDOM = not WIND_RANDOM  # Alternar el estado del viento aleatorio
                print(f"Viento Aleatorio: {WIND_RANDOM}")
            elif increase_speed_button.collidepoint(mouse_pos):
                game_speed = min(game_speed * 2, 16.0)  # Aumentar la velocidad del juego, max 16x
                print(f"Velocidad del Juego: {game_speed}x")
            elif decrease_speed_button.collidepoint(mouse_pos):
                game_speed = max(game_speed / 2, 0.125)  # Disminuir la velocidad del juego, min 0.125x
                print(f"Velocidad del Juego: {game_speed}x")
            elif new_button.collidepoint(mouse_pos):
                file_path = open_file_dialog(initialdir='_internal//images')
                if file_path:
                    new_image, new_classified_image, new_risk_map = process_new_image(file_path, unet_model)
                    if new_image is not None:
                        original_image = new_image
                        classified_image = new_classified_image
                        risk_map = new_risk_map

                        # Actualiza las dimensiones del grid y la ventana
                        img_width = new_image.shape[1]
                        img_height = new_image.shape[0]
                        GRID_WIDTH = img_width
                        GRID_HEIGHT = img_height
                        update_window_size(img_width, img_height)

                        fire_grid, fuel_grid, shield = initialize_fire_and_fuel(GRID_WIDTH, GRID_HEIGHT, risk_map)
                        burned = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
                        updates = 0
                        total_fuel_used = 0
                        paused = True
                        fire_started = False
                        fire_start_positions = []  # Reiniciar la lista de posiciones de inicio del fuego

                        image1, image2 = load_menu_images(original_image, classified_image)
                        background_surface = load_background_image(original_image)
                        print("Nueva imagen cargada y procesada")
            elif image1_rect.collidepoint(mouse_pos):
                current_background = original_image
                background_surface = load_background_image(original_image)
                print("Imagen 1 seleccionada como fondo")
            elif image2_rect.collidepoint(mouse_pos):
                current_background = classified_image
                background_surface = load_background_image(classified_image)
                print("Imagen 2 seleccionada como fondo")
            else:
                if not fire_started:
                    # Convertir coordenadas del clic a coordenadas del grid
                    grid_x = mouse_pos[0] - BOARD_X
                    grid_y = mouse_pos[1] - BOARD_Y
                    if 0 <= grid_x < GRID_WIDTH and 0 <= grid_y < GRID_HEIGHT:
                        fire_start_positions.append((grid_x, grid_y))
                        print(f"Fire start position added at: {grid_x}, {grid_y}")

    screen.fill((0, 0, 0))
    draw_fire_and_fuel(screen, fire_grid, fuel_grid, risk_map, burned, GRID_WIDTH, GRID_HEIGHT, background_surface, fire_start_positions)
    display_stats(screen, cells_on_fire, updates, burned, total_fuel_used)

    # Vuelve a dibujar el menú después de procesar eventos
    start_button, pause_button, reset_button, new_button, toggle_wind_button, increase_speed_button, decrease_speed_button, image1_rect, image2_rect = draw_menu(
        screen, image1, image2, game_speed)  # Dibujar el menú

    # Cambiar el cursor cuando el ratón está sobre un botón
    if any(button.collidepoint(pygame.mouse.get_pos()) for button in
           [start_button, pause_button, reset_button, toggle_wind_button, increase_speed_button,
            decrease_speed_button, new_button, image1_rect, image2_rect]):
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
    else:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    # Actualizar la pantalla
    pygame.display.flip()

    if not paused:
        fire_grid, fuel_grid, cells_on_fire, total_fuel_used = update_fire(fire_grid, fuel_grid, burned, risk_map, shield, game_speed)
        updates += 1

# Salir de Pygame
pygame.quit()
sys.exit()
