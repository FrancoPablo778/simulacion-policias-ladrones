import numpy as np


# Tipos de terreno
FOREST = 1
JAIL = 2
OBSTACLE = 3

# Dimensiones del ambiente
NUM_ROWS = 50
NUM_COLS = 50

# Porcentaje de obstáculos
OBSTACLE_PERCENTAGE = 0.06


def create_environment(seed=None):
    """
    Crea el mapa de la simulación.

    FOREST = 1: bosque
    JAIL = 2: cárcel
    OBSTACLE = 3: obstáculo

    seed permite reproducir el mismo mapa en las pruebas.
    """
    rng = np.random.default_rng(seed)

    # Todo el mapa comienza como bosque.
    environment = np.full(
        (NUM_ROWS, NUM_COLS),
        FOREST,
        dtype=int
    )

    # La cárcel ocupa la esquina inferior derecha.
    jail_start_row = NUM_ROWS - 5
    jail_start_col = NUM_COLS - 5

    environment[
        jail_start_row:,
        jail_start_col:
    ] = JAIL

    # Calcular la cantidad de obstáculos.
    total_obstacles = round(
        OBSTACLE_PERCENTAGE * NUM_ROWS * NUM_COLS
    )

    # Elegir celdas del bosque sin repetir posiciones.
    forest_positions = np.argwhere(environment == FOREST)

    selected_indices = rng.choice(
        len(forest_positions),
        size=total_obstacles,
        replace=False
    )

    selected_positions = forest_positions[selected_indices]

    for row, col in selected_positions:
        environment[row, col] = OBSTACLE

    return environment
