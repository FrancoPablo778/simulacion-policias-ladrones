
import numpy as np

from src.environment import (
    FOREST,
    JAIL,
    OBSTACLE,
    NUM_ROWS,
    NUM_COLS,
)
from src.agents import Prisoner, Police
from src.movement import move_police, find_path


def test_police_moves_toward_prisoner():
    environment = np.full(
        (NUM_ROWS, NUM_COLS), FOREST, dtype=int
    )

    officer = Police((10, 10), target=0)
    prisoner = Prisoner((10, 13))

    old_distance = abs(10 - 10) + abs(13 - 10)

    move_police(officer, [prisoner], environment)

    new_distance = (
        abs(prisoner.position[0] - officer.position[0])
        + abs(prisoner.position[1] - officer.position[1])
    )

    assert new_distance < old_distance


def test_path_avoids_obstacles():
    environment = np.full(
        (NUM_ROWS, NUM_COLS), FOREST, dtype=int
    )

    environment[10, 11] = OBSTACLE
    path = find_path((10, 10), (10, 12), environment)

    assert path
    assert (10, 11) not in path
    assert path[-1] == (10, 12)


def test_police_captures_prisoner():
    environment = np.full(
        (NUM_ROWS, NUM_COLS), FOREST, dtype=int
    )

    officer = Police((10, 10), target=0)
    prisoner = Prisoner((10, 11))

    move_police(officer, [prisoner], environment)

    assert prisoner.state == "captured"
    assert officer.escorting == 0
    assert prisoner.position == officer.position



def test_prisoner_is_returned_to_jail():
    environment = np.full(
        (NUM_ROWS, NUM_COLS), FOREST, dtype=int
    )

    environment[45:50, 45:50] = JAIL

    officer = Police((44, 45), target=-1, escorting=0)
    prisoner = Prisoner((44, 45), state="captured")

    # Primer turno: el policía entra a la cárcel.
    move_police(officer, [prisoner], environment)

    assert environment[officer.position] == JAIL
    assert prisoner.state == "captured"

    # Segundo turno: se completa la entrega.
    move_police(officer, [prisoner], environment)

    assert prisoner.state == "removed"
    assert officer.escorting == -1
