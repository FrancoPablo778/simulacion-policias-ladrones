
import numpy as np

from src.environment import FOREST, JAIL
from src.agents import Prisoner, Police


NUM_PRISONERS = 100
NUM_POLICE = 15


def initialize_agents(environment, seed=None):
    rng = np.random.default_rng(seed)

    # Buscar las posiciones disponibles de bosque y cárcel.
    forest_positions = np.argwhere(environment == FOREST)
    jail_positions = np.argwhere(environment == JAIL)

    # Verificar que existan suficientes posiciones.
    if len(forest_positions) < NUM_PRISONERS:
        raise ValueError("No hay suficiente espacio para los prisioneros.")

    if len(jail_positions) < NUM_POLICE:
        raise ValueError("No hay suficiente espacio para los policías.")

    # Crear prisioneros en el bosque.
    selected_forest = rng.choice(
        len(forest_positions),
        size=NUM_PRISONERS,
        replace=False
    )

    prisoners = [
        Prisoner(tuple(map(int, forest_positions[index])))
        for index in selected_forest
    ]

    # Crear policías dentro de la cárcel.
    selected_jail = rng.choice(
        len(jail_positions),
        size=NUM_POLICE,
        replace=False
    )

    police = [
        Police(tuple(map(int, jail_positions[index])))
        for index in selected_jail
    ]

    # Asignar a cada policía un prisionero libre distinto.
    selected_targets = rng.choice(
        NUM_PRISONERS,
        size=min(NUM_POLICE, NUM_PRISONERS),
        replace=False
    )

    for officer, target in zip(police, selected_targets):
        officer.target = int(target)

    return prisoners, police
