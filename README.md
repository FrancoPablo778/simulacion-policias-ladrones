# Simulación de Policías y Ladrones

Proyecto de simulación basada en agentes, desarrollado en Python, que representa la interacción entre policías y prisioneros dentro de un entorno de cuadrícula.

El proyecto incluye una visualización gráfica del entorno, el movimiento de los agentes y el seguimiento de los prisioneros durante la simulación.

## Características principales

- Representación visual del entorno mediante una cuadrícula.
- Diferenciación de elementos mediante colores.
- Movimiento de prisioneros dentro del entorno.
- Movimiento de policías para perseguir a los prisioneros.
- Captura y traslado de prisioneros a la cárcel.
- Visualización animada del desarrollo de la simulación.
- Pruebas automatizadas para comprobar el funcionamiento de diferentes comportamientos.

## Tecnologías utilizadas

- **Python:** lenguaje principal del proyecto.
- **NumPy:** manejo de arreglos y datos del entorno.
- **Matplotlib:** representación gráfica y animación de la simulación.
- **Pytest:** ejecución de pruebas automatizadas.

## Requisitos

- Python 3 instalado.
- pip, administrador de paquetes de Python.

## Instalación y ejecución

### 1. Clonar el repositorio

```bash
git clone URL_DEL_REPOSITORIO
```

### 2. Entrar a la carpeta del proyecto

```bash
cd NOMBRE_DEL_REPOSITORIO
```

### 3. Crear un entorno virtual

```bash
python -m venv .venv
```

### 4. Activar el entorno virtual

En Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 5. Instalar las dependencias

```bash
python -m pip install -r requirements.txt
```

### 6. Ejecutar la simulación

```bash
python main.py
```

## Ejecución de pruebas

Para ejecutar las pruebas automatizadas, utiliza:

```bash
python -m pytest -v
```

Este comando permite verificar diferentes comportamientos de la simulación y mostrar los resultados de cada prueba.

## Estructura del proyecto

```text
ABM/
│
├── src/                  # Código fuente de la simulación
│
├── main.py               # Archivo principal de ejecución
├── requirements.txt      # Dependencias del proyecto
├── .gitignore            # Archivos excluidos de Git
│
├── Test_environment.py   # Pruebas del entorno
├── test_movement.py      # Pruebas de movimiento
└── test_police.py        # Pruebas del comportamiento policial
```

## Contexto del proyecto

Este proyecto comenzó como una implementación en MATLAB y posteriormente fue migrado a Python, con el propósito de desarrollar y comprobar su funcionamiento utilizando herramientas de programación y pruebas automatizadas.

---

**Estado:** Proyecto funcional en desarrollo académico.