
import numpy as np
import matplotlib.pyplot as plt

from matplotlib.colors import ListedColormap
from matplotlib.animation import FuncAnimation

from src.environment import create_environment
from src.initialization import initialize_agents
from src.movement import move_prisoner, move_police


def main():

    # =================================
    # 1. CONFIGURACIÓN DE LA SIMULACIÓN
    # =================================

    TOTAL_ITERATIONS = 1000

    environment = create_environment(seed=42)

    prisoners, police = initialize_agents(
        environment,
        seed=42
    )

    rng = np.random.default_rng(123)

    # =================================
    # 2. DEFINIR LOS COLORES
    # =================================

    colors = [
        "#45A049",  # Bosque
        "#A0A0A0",  # Cárcel
        "#303030",  # Obstáculos
        "#FF8C00",  # Prisioneros
        "#0000FF",  # Policías
    ]

    cmap = ListedColormap(colors)

    # =================================
    # 3. CREAR LA VENTANA
    # =================================

    fig, ax = plt.subplots(figsize=(10, 9))

    # Título principal
    title_text = fig.text(
        0.5, 0.975,
        "POLICÍAS Y LADRONES - TURNO 0",
        ha="center",
        fontsize=16,
        fontweight="bold"
    )

    # Contador de iteraciones
    iteration_text = fig.text(
        0.5, 0.935,
        f"ITERACIONES: 0 / {TOTAL_ITERATIONS}",
        ha="center",
        fontsize=12,
        fontweight="bold"
    )

    # Estadísticas de los prisioneros
    stats_text = fig.text(
        0.5, 0.895,
        "Libres: 0 | Capturados: 0 | Entregados: 0",
        ha="center",
        fontsize=12
    )

    display_grid = environment.copy()

    image = ax.imshow(
        display_grid,
        cmap=cmap,
        vmin=1,
        vmax=5,
        interpolation="nearest"
    )

    ax.set_xlabel("Columnas")
    ax.set_ylabel("Filas")
    ax.set_xticks(range(0, 50, 5))
    ax.set_yticks(range(0, 50, 5))

    # =================================
    # 4. ACTUALIZAR LA SIMULACIÓN
    # =================================

    def update(frame):

        # Mover prisioneros libres
        for prisoner in prisoners:

            move_prisoner(
                prisoner,
                police,
                environment,
                rng
            )

        # Mover policías
        for officer in police:

            move_police(
                officer,
                prisoners,
                environment
            )

        # =================================
        # 5. RECONSTRUIR LA CUADRÍCULA
        # =================================

        display_grid = environment.copy()

        # Dibujar prisioneros
        for prisoner in prisoners:

            if prisoner.state != "removed":

                row, col = prisoner.position
                display_grid[row, col] = 4

        # Dibujar policías
        for officer in police:

            row, col = officer.position
            display_grid[row, col] = 5

        image.set_data(display_grid)

        # =================================
        # 6. CALCULAR ESTADÍSTICAS
        # =================================

        free = sum(
            p.state == "free" for p in prisoners
        )

        captured = sum(
            p.state == "captured" for p in prisoners
        )

        removed = sum(
            p.state == "removed" for p in prisoners
        )

        # Actualizar título
        title_text.set_text(
            f"POLICÍAS Y LADRONES - TURNO {frame + 1}"
        )

        # Actualizar iteraciones
        iteration_text.set_text(
            f"ITERACIONES: {frame + 1} / {TOTAL_ITERATIONS}"
        )

        # Actualizar estadísticas
        stats_text.set_text(
            f"Libres: {free}  |  "
            f"Capturados: {captured}  |  "
            f"Entregados: {removed}"
        )

        return [image]

    # =================================
    # 7. EJECUTAR LA ANIMACIÓN
    # =================================

    ani = FuncAnimation(
        fig,
        update,
        frames=TOTAL_ITERATIONS,
        interval=200,
        repeat=False,
        blit=False
    )

    # =================================
    # 8. AJUSTAR LA DISTRIBUCIÓN
    # =================================

    plt.subplots_adjust(
        top=0.85,
        bottom=0.08,
        left=0.08,
        right=0.95
    )

    plt.show()


if __name__ == "__main__":
    main()

