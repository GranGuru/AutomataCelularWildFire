import random
import numpy as np
from constants import WIND

def initialize_fire_and_fuel(grid_width, grid_height, risk_map):
    # Crear el grid de fuego, combustible y escudo
    grid = [[0 for _ in range(grid_width)] for _ in range(grid_height)]
    fuel = [[0 for _ in range(grid_width)] for _ in range(grid_height)]
    shield = [[0 for _ in range(grid_width)] for _ in range(grid_height)]

    for y in range(grid_height):
        for x in range(grid_width):
            risk_level = risk_map[y, x]  # Obtener el nivel de riesgo del mapa
            if risk_level == 1:
                fuel[y][x] = 0  # Rocas, no se queman
                shield[y][x] = float('inf')  # Infinita resistencia
            elif risk_level == 2:
                fuel[y][x] = random.randint(50, 100)
                shield[y][x] = 50
            elif risk_level == 3:
                fuel[y][x] = random.randint(100, 150)
                shield[y][x] = 30
            elif risk_level == 4:
                fuel[y][x] = random.randint(150, 200)
                shield[y][x] = 20
            elif risk_level == 5:
                fuel[y][x] = random.randint(200, 250)
                shield[y][x] = 10

    return grid, fuel, shield  # Devolver el grid de fuego, combustible y escudo

def update_fire(grid, fuel, burned, terrain_map, shield, game_speed):
    grid_width = len(grid[0])
    grid_height = len(grid)
    new_grid = [[0 for _ in range(grid_width)] for _ in range(grid_height)]
    total_fuel_used = 0
    cells_on_fire = 0

    wind_speed_threshold = 0.5  # Umbral de velocidad del viento para detener propagación en contra

    for y in range(grid_height):
        for x in range(grid_width):
            if grid[y][x] > 0:
                risk_level = terrain_map[y, x]  # Obtener nivel de riesgo del mapa de terreno
                if risk_level == 1:
                    continue  # El fuego no puede quemar esta célula (rocas)
                elif fuel[y][x] > 0:
                    # Ajustar la reducción de intensidad según el riesgo del terreno y la velocidad del juego
                    reduction_rate = {
                        2: random.randint(1, 2),  # Muy lento (riesgo bajo)
                        3: random.randint(3, 6),  # Normal (riesgo moderado)
                        4: random.randint(7, 10),  # Rápido (riesgo alto)
                        5: random.randint(11, 15)  # Muy rápido (riesgo extremo)
                    }.get(risk_level, random.randint(5, 10))

                    # Mantener la reducción de combustible constante, sin depender de game_speed
                    reduction_rate = int(reduction_rate)

                    # Reducir la intensidad del fuego según el nivel de riesgo
                    new_intensity = max(0, grid[y][x] - reduction_rate)
                    new_grid[y][x] = new_intensity

                    # Reducir el combustible
                    fuel[y][x] -= reduction_rate
                    total_fuel_used += reduction_rate

                    # Apagar la celda si el combustible es <= 10
                    if fuel[y][x] <= 10:
                        fuel[y][x] = 0
                        new_grid[y][x] = 0

                    cells_on_fire += 1
                    burned[y][x] = 1

                    # Poder de quemado
                    burning_power = 1
                    if grid[y][x] == 255:
                        burning_power = 2
                    if WIND[2] > wind_speed_threshold:
                        burning_power *= 2

                    # Propagar fuego a las celdas vecinas
                    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Direcciones básicas
                    for dy, dx in directions:
                        ny, nx = y + dy, x + dx
                        # Verificar la dirección del viento
                        if WIND[2] > wind_speed_threshold and (dx, dy) == (-WIND[0], -WIND[1]):
                            continue  # No propagar en contra del viento fuerte

                        if 0 <= ny < grid_height and 0 <= nx < grid_width and fuel[ny][nx] > 0:
                            # Verificar y reducir escudo
                            if shield[ny][nx] > 0:
                                shield[ny][nx] -= burning_power
                            if shield[ny][nx] <= 0:
                                wind_factor = 1.0
                                if (dx, dy) == (WIND[0], WIND[1]):
                                    wind_factor += WIND[2]  # Aumentar probabilidad si está en la dirección del viento
                                propagation_chance = {
                                    2: 0.1,  # Muy bajo (riesgo bajo)
                                    3: 0.3,  # Moderado (riesgo moderado)
                                    4: 0.6,  # Alto (riesgo alto)
                                    5: 0.9  # Muy alto (riesgo extremo)
                                }.get(risk_level, 0.5)
                                if random.random() < propagation_chance * wind_factor * game_speed:  # Probabilidad de propagación ajustada por velocidad
                                    propagation_intensity = max(0, new_intensity - random.randint(0, 5))
                                    new_grid[ny][nx] = max(new_grid[ny][nx], propagation_intensity)
                                    print(f"Fire propagated to ({ny}, {nx}) with intensity {propagation_intensity}")

    # Clasificar las celdas como frente, cola e interior del fuego
    for y in range(grid_height):
        for x in range(grid_width):
            if new_grid[y][x] > 200:
                # Frente del fuego
                new_grid[y][x] = 255
            elif new_grid[y][x] > 100:
                # Cola del fuego
                new_grid[y][x] = 150
            elif new_grid[y][x] > 0:
                # Interior del fuego
                new_grid[y][x] = 75
            elif burned[y][x] == 1:
                # Celda quemada permanece negra
                new_grid[y][x] = 0

            # Apagar las celdas con poco combustible
            if fuel[y][x] <= 10:
                new_grid[y][x] = 0

    return new_grid, fuel, cells_on_fire, total_fuel_used  # Devolver el nuevo grid, el combustible, las celdas en fuego y el combustible total usado
