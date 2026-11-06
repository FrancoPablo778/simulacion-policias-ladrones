
import numpy as np

from src.environment import create_environment, FOREST
from src.agents import Prisoner, Police
from src.movement import move_prisoner, is_valid_position


def test_prisoner_moves_to_valid_position():
    environment = create_environment(seed=42)
    prisoner = Prisoner((10, 10))
    rng = np.random.default_rng(123)

    move_prisoner(prisoner, [], environment, rng)

    assert prisoner.position != (10, 10)
    assert is_valid_position(prisoner.position, environment)


def test_captured_prisoner_does_not_move():
    environment = create_environment(seed=42)
    prisoner = Prisoner((10, 10), state="captured")
    original_position = prisoner.position

    move_prisoner(
        prisoner, [], environment, np.random.default_rng(123)
    )

    assert prisoner.position == original_position


def test_prisoner_does_not_enter_obstacle():
    environment = np.ones((50, 50), dtype=int)
    environment[10, 11] = 3

    prisoner = Prisoner((10, 10))
    police = []
    rng = np.random.default_rng(5)

    # Repetir varios movimientos para comprobar que nunca
    # termina dentro de una celda con obstáculo.
    for _ in range(100):
        move_prisoner(prisoner, police, environment, rng)
        assert environment[prisoner.position] != 3
