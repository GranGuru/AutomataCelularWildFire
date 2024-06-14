# constants.py

# Dimensiones de la ventana
WINDOW_WIDTH, WINDOW_HEIGHT = 1400, 700
CELL_SIZE = 2  # Tamaño de cada celda en píxeles

# Posición del tablero dentro de la ventana
BOARD_X, BOARD_Y = 0, 100

# Configuración inicial del viento (dx, dy, intensidad)
WIND = [1, 0, 0.8]  # Sin dirección inicial, intensidad media
WIND_RANDOM = False
WIND_CHANGE_INTERVAL = 5  # Intervalo de cambio de viento en segundos

# Velocidad del juego
GAME_SPEED = 0.5  # Inicializar GAME_SPEED

# Colores para los botones
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
HOVER_COLOR = (200, 200, 200)  # Color para el efecto hover

# Path to images
SIERRA_IMAGE_PATH = "_internal//images//sierra.png"  # Ruta de la imagen de fondo
CLASSIFIED_SOIL_IMAGE_PATH = "_internal//images//classified_soil.png"  # Ruta de la imagen clasificada del suelo
MODEL_PATH = "_internal//model_unet//unet_forest_segmentation_model.h5"  # Ruta del modelo U-Net