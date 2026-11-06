from collections import deque

import numpy as np

from src.environment import (
    FOREST,
    JAIL,
    OBSTACLE,
    NUM_ROWS,
    NUM_COLS,
)

ESCAPE_RANGE = 6

DIRECTIONS = [
    (-1, 0),
    (1, 0),
    (0, -1),
    (0, 1),
    (-1, -1),
    (-1, 1),
    (1, -1),
    (1, 1),
]


def is_valid_position(position, environment):
    """Comprueba que una posición esté dentro del mapa
    y no contenga un obstáculo."""
    row, col = position

    if not (0 <= row < NUM_ROWS and 0 <= col < NUM_COLS):
        return False

    return environment[row, col] != OBSTACLE


def find_path(start, goal, environment):
    """Encuentra una ruta evitando obstáculos mediante BFS.

    Devuelve las posiciones que deben recorrerse después
    de start. Si no existe una ruta, devuelve una lista vacía.
    """
    start = tuple(start)
    goal = tuple(goal)

    if start == goal:
        return []

    if not is_valid_position(goal, environment):
        return []

    queue = deque([start])
    parents = {start: None}

    while queue:
        current = queue.popleft()

        for dr, dc in DIRECTIONS:
            neighbor = (current[0] + dr, current[1] + dc)

            if neighbor in parents:
                continue

            if not is_valid_position(neighbor, environment):
                continue

            parents[neighbor] = current

            if neighbor == goal:
                path = []
                position = goal

                while position != start:
                    path.append(position)
                    position = parents[position]

                path.reverse()
                return path

            queue.append(neighbor)

    return []


def move_prisoner(prisoner, police, environment, rng):
    """Mueve al prisionero libre o lo hace huir."""

    if prisoner.state != "free":
        return

    row, col = prisoner.position
    current_position = np.array([row, col])

    escape_direction = np.zeros(2, dtype=float)

    for officer in police:
        police_position = np.array(officer.position)
        distance = np.linalg.norm(
            current_position - police_position
        )

        if distance <= ESCAPE_RANGE:
            escape_direction += current_position - police_position

    if np.any(escape_direction):
        escape_direction = np.sign(escape_direction).astype(int)

        candidates = [
            tuple(current_position + escape_direction)
        ]

        alternatives = [
            tuple(current_position + direction)
            for direction in DIRECTIONS
        ]

        rng.shuffle(alternatives)
        candidates.extend(alternatives)

    else:
        candidates = [
            tuple(current_position + direction)
            for direction in DIRECTIONS
        ]

        rng.shuffle(candidates)

    for candidate in candidates:
        if is_valid_position(candidate, environment):
            prisoner.position = candidate
            return


def move_police(officer, prisoners, environment):
    """Persigue, captura o escolta a un prisionero.

    Cada llamada representa un turno de movimiento del policía.
    """

    # Si está escoltando, debe regresar a la cárcel.
    if officer.escorting != -1:
        prisoner = prisoners[officer.escorting]

        jail_positions = np.argwhere(environment == JAIL)

        # Si ya llegó a la cárcel, termina la escolta.
        if environment[officer.position] == JAIL:
            prisoner.position = officer.position
            prisoner.state = "removed"
            officer.escorting = -1
            officer.target = -1
            return

        # Buscar una celda de cárcel alcanzable.
        goals = sorted(
            [tuple(map(int, p)) for p in jail_positions],
            key=lambda p: abs(p[0] - officer.position[0])
            + abs(p[1] - officer.position[1])
        )

        for goal in goals:
            path = find_path(
                officer.position, goal, environment
            )

            if path:
                officer.position = path[0]
                prisoner.position = officer.position

                # La llegada se registra en el siguiente turno.
                return

        return

    # Validar el objetivo actual.
    if not (
        0 <= officer.target < len(prisoners)
        and prisoners[officer.target].state == "free"
    ):
        officer.target = -1

    # Elegir el prisionero libre más cercano si no hay objetivo.
    if officer.target == -1:
        available = [
            i for i, p in enumerate(prisoners)
            if p.state == "free"
        ]

        if not available:
            return

        officer.target = min(
            available,
            key=lambda i: (
                abs(prisoners[i].position[0] - officer.position[0])
                + abs(prisoners[i].position[1] - officer.position[1])
            )
        )

    target = prisoners[officer.target]

    # Si ya comparte la celda con el objetivo, lo captura.
    if officer.position == target.position:
        target.state = "captured"
        target.position = officer.position
        officer.escorting = officer.target
        officer.target = -1
        return

    # Avanzar una celda por la ruta hacia el objetivo.
    path = find_path(
        officer.position, target.position, environment
    )

    if not path:
        officer.target = -1
        return

    officer.position = path[0]

    # Capturar al alcanzar la posición del prisionero.
    if officer.position == target.position:
        target.state = "captured"
        target.position = officer.position
        officer.escorting = officer.target
        officer.target = -1
