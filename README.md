# Simulador de Algoritmos de Despacho

Este es un simulador interactivo para visualizar el funcionamiento de tres algoritmos de despacho de procesos: **FIFO (First In, First Out)**, **SJF (Shortest Job First)** y **Despacho por Prioridad**. El programa está desarrollado en Python utilizando `PyQt5` para la interfaz gráfica, y permite al usuario agregar procesos, visualizar su ejecución a través de un **diagrama de Gantt**, y calcular tiempos de espera y de sistema para cada proceso.

![image](https://github.com/user-attachments/assets/d82efc99-0548-44f3-b13a-03dd5317eb85)

## Características

- Simulación de tres algoritmos de despacho:
  - **FIFO (First In, First Out)**: Procesa los trabajos en el orden de llegada.
  - **SJF (Shortest Job First)**: Procesa los trabajos con la ráfaga más corta primero.
  - **Despacho por Prioridad**: Procesa los trabajos según la prioridad asignada, con desempate por FIFO.
  
- **Visualización del diagrama de Gantt** para mostrar el orden de ejecución de los procesos.
- **Cálculo de tiempos de espera y tiempos en el sistema** para cada proceso.
- Presentación de los resultados en una tabla con la opción de mostrar el **promedio de los tiempos**.
- Validación de los datos de entrada para asegurar que los valores sean correctos:
  - No se permiten valores negativos para los campos de ráfaga, tiempo de llegada o prioridad.
  - Si la columna de prioridad no está visible, no se requiere validar ese campo (solo para FIFO y SJF).
- **Alternancia de colores** en las filas de la tabla de procesos para mejorar la visualización.
- Colores personalizados en el diagrama de Gantt para cada proceso.

## Requisitos

Para ejecutar este programa, necesitas tener instalado lo siguiente:

- **Python 3.x**
- **PyQt5**: Para la interfaz gráfica.
- **matplotlib**: Para la visualización del diagrama de Gantt.

### Instalación de dependencias

Se pueden instalar las dependencias necesarias ejecutando el siguiente comando:

```bash
pip install PyQt5 matplotlib
```

Instrucciones de Instalación
Clona el repositorio en tu máquina local:

```bash
git clone https://github.com/tu_usuario/tu_repositorio.git
cd tu_repositorio
```

Instala las dependencias del proyecto:

```bash
pip install -r requirements.txt
```

Ejecuta el programa:

```bash
python simulador_algoritmos.py
```

## Uso del Programa
- Interfaz Gráfica
- **Al iniciar el programa, verás una ventana con un menú desplegable donde podrás seleccionar uno de los tres algoritmos de despacho.**
- **Agrega los procesos necesarios utilizando el botón "Agregar Proceso".**
- **Completa los campos de ráfaga (CPU) y tiempo de llegada. Si seleccionas el algoritmo de prioridad, también se debe ingresar la prioridad.**
- **Para cada proceso, se asignará un color diferente en el diagrama de Gantt.**
- **Una vez agregados los procesos, haz clic en "Ejecutar Algoritmo" para visualizar el diagrama de Gantt y los tiempos de espera y tiempos en el sistema de cada proceso.**
- **Se mostrará una tabla con los tiempos calculados, y en la última fila, se presentará el promedio de estos tiempos.**

## Validación de Datos
- La entrada de datos está validada para evitar errores:
- **Solo se permiten números positivos en los campos de ráfaga, tiempo de llegada y prioridad.**
- **Si se seleccionan los algoritmos FIFO o SJF, el campo de prioridad no será visible ni requerido.**
- **Si los campos no son válidos, se mostrará un mensaje de advertencia y no se procederá con la ejecución del algoritmo.**

## Ejemplo de Diagrama de Gantt
- Una vez que se ejecuta un algoritmo, se generará un diagrama de Gantt como el siguiente:


## Resultados en la Tabla
- Los resultados para los tiempos de espera y tiempos en el sistema aparecerán en una tabla, con una fila adicional que muestra el promedio:

![image](https://github.com/user-attachments/assets/21b1fa35-07df-49c6-8c7f-73f0da991cb9)

Funciones Principales del Código:
- run_algorithm(): Ejecuta el algoritmo seleccionado y recoge los datos ingresados.
- show_gantt_chart(): Genera el diagrama de Gantt con los procesos en ejecución.
- show_results_table(): Muestra los tiempos de espera y los tiempos en el sistema en una tabla, calculando y añadiendo una fila con el promedio.
- validate_input(): Verifica que todos los datos ingresados sean válidos (números positivos, campos completos).
