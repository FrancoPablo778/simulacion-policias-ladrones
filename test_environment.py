
import numpy as np

from src.environment import (
    create_environment,
    FOREST,
    JAIL,
    OBSTACLE,
    NUM_ROWS,
    NUM_COLS,
)


def test_environment_dimensions():
    environment = create_environment(seed=42)

    assert environment.shape == (50, 50)


def test_jail_area():
    environment = create_environment(seed=42)

    assert np.all(environment[45:, 45:] == JAIL)


def test_obstacles_are_outside_jail():
    environment = create_environment(seed=42)

    assert not np.any(environment[45:, 45:] == OBSTACLE)


def test_obstacle_count():
    environment = create_environment(seed=42)

    assert np.count_nonzero(environment == OBSTACLE) == round(
        0.06 * NUM_ROWS * NUM_COLS
    )


def test_only_valid_terrain_values_exist():
    environment = create_environment(seed=42)

    assert set(np.unique(environment)).issubset(
        {FOREST, JAIL, OBSTACLE}
    )
