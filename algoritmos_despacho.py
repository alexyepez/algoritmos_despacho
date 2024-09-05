import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QComboBox, QTableWidget, QTableWidgetItem
from PyQt5.QtWidgets import QHBoxLayout, QPushButton, QLabel, QMessageBox, QDialog, QMenuBar, QMenu
from PyQt5.QtCore import Qt # Se importa la clase Qt para alinear el texto
from PyQt5.QtGui import QFont # Se importa la clase QFont para cambiar el tamaño de la fuente
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class Despacho(QWidget):
    def __init__(self):
        super().__init__()

        # Se inicializa la interfaz de usuario
        self.initializeUserInterface()

    def initializeUserInterface(self):
        """
        DESCRIPCIÓN:    Se inicializa la interfaz de usuario con los elementos necesarios para ingresar los datos

        ENTRADA: Ninguna.

        SALIDA: Ninguna.
        """
        # menú desplegable en la barra superior
        menubar = QMenuBar(self)
        ayuda_menu = QMenu('Ayuda', self)
        ayuda_menu.addAction('About', self.show_about)
        ayuda_menu.addAction('Help', self.show_help)
        menubar.addMenu(ayuda_menu)

        layout = QVBoxLayout()
        layout.setMenuBar(menubar) # Se añade el menú a la ventana

        # Se crea el menú desplegable para seleccionar el algortimo
        self.algoritmo_selector = QComboBox(self)
        self.algoritmo_selector.addItems(["FIFO", "SJF", "Prioridad", "About", "Help"])
        self.algoritmo_selector.currentIndexChanged.connect(self.update_table_columns)
        layout.addWidget(QLabel("Seleccione Algoritmo:"))
        layout.addWidget(self.algoritmo_selector)

        # Se crea la tabla  para ingresar procesos
        self.table = QTableWidget(self)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Proceso", "Ráfaga (CPU)", "Tiempo de llegada", "Prioridad"])
        layout.addWidget(self.table)

        # Se ajusta el tamaño de las columnas
        self.table.setColumnWidth(0, 100) # Columna de proceso
        self.table.setColumnWidth(1, 100) # Columna de ráfaga
        self.table.setColumnWidth(2, 150) # Columna de tiempo de llegada
        self.table.setColumnWidth(3, 100) # Columna de prioridad

        # Se crea un botón para agregar filas a la tabla
        self.add_row_button = QPushButton("Agregar Proceso", self)
        self.add_row_button.clicked.connect(self.add_row)
        layout.addWidget(self.add_row_button)

        # Se crea un botón para eliminar la última fila
        self.remove_row_button = QPushButton("Eliminar Última Fila", self)
        self.remove_row_button.clicked.connect(self.remove_last_row)
        layout.addWidget(self.remove_row_button)

        # Se crea un botón para ejecutar el algoritmo seleccionado
        self.run_button = QPushButton("Ejecutar Algoritmo", self)
        self.run_button.clicked.connect(self.run_algorithm)
        layout.addWidget(self.run_button)

        # Se establece el tamaño de la ventana
        self.resize(800, 500) # Se ajusta el tamaño de la ventana (ancho, alto)

        # Se establece el layout principal
        self.setLayout(layout)
        self.setWindowTitle("Simulador de Algoritmos de Despacho")
        self.update_table_columns() # Se asegura que las columnas se actualicen al inicio
        self.show()

    def add_row(self):
        """
        DESCRIPCIÓN:    Se añade una fila a la tabla de procesos con los campos necesarios para 
                        ingresar los datos de un nuevo proceso.

        ENTRADA: Ninguna.

        SALIDA: Ninguna.
        """
        row_Position = self.table.rowCount()
        self.table.insertRow(row_Position)
        # Se autocompleta el nombre del proceso para no estar ingresando el nombre de cada proceso manualmente
        self.table.setItem(row_Position, 0, QTableWidgetItem(f"P{row_Position + 1}"))

    def remove_last_row(self):
        """
        DESCRIPCIÓN:    Se elimina la última fila de la tabla de procesos.

        ENTRADA: Ninguna.

        SALIDA: Ninguna.
        """
        row_position = self.table.rowCount()
        if row_position > 0:
            self.table.removeRow(row_position - 1)


    def update_table_columns(self):
        """
        DESCRIPCIÓN:    Se actualizan las columnas de la tabla dependiendo del algoritmo seleccionado.
                        Se oculta la columna de prioridad si el algoritmo seleccionado es FIFO o SJF, y se muestra
                        en caso contrario.

        ENTRADA: Ninguna.

        SALIDA: Ninguna.
        """
        # Se actualizan las columnas de la tabla dependiendo del algoritmo seleccionado
        selected_algorithm = self.algoritmo_selector.currentText()
        self.table.setRowCount(0) # Se limpian las filas al cambiar de algoritmo

        if selected_algorithm in ["FIFO", "SJF"]:
            self.table.setColumnHidden(3, True) # Se oculta la columna de prioridad
        else:
            self.table.setColumnHidden(3, False) # Se muestra la columna de prioridad

    # Función para ejecutar el algoritmo seleccionado
    def run_algorithm(self):
        """
        DESCRIPCIÓN:    Se ejecuta el algoritmo seleccionado en la tabla de procesos. Se obtienen los datos
                        ingresados en la tabla y se ejecuta el algoritmo correspondiente.
        
        ENTRADA: Ninguna.

        SALIDA: Ninguna.
        """
        # Aquí se ejecuta el algoritmo seleccionado
        selected_algorithm = self.algoritmo_selector.currentText()
        processes = []

        # Se obtienen los datos ingresados en la tabla
        for row in range(self.table.rowCount()):
            process_name = self.table.item(row, 0).text() if self.table.item(row, 0) else ''
            burst_time = int(self.table.item(row, 1).text()) if self.table.item(row, 1) else 0
            arrival_time = int(self.table.item(row, 2).text()) if self.table.item(row, 2) else 0
            priority = int(self.table.item(row, 3).text()) if self.table.item(row, 3) and not self.table.isColumnHidden(3) else 0

            """
            # Se valida que no falten datos
            if not burst_time or not arrival_time:
                QMessageBox.warning(self, "Advertencia", "Por favor, complete todos los campos.")
                return
            """
            
            # Se añaden los procesos a la lista
            processes.append({
                'nombre': process_name,
                'ejecucion': burst_time,
                'llegada': arrival_time,
                'prioridad': priority
            })
        
        # Nos aseguramos de que haya al menos un proceso antes de continuar
        if not processes:
            QMessageBox.warning(self, "Advertencia", "Por favor, añada al menos un proceso.")
            return
        
        if selected_algorithm == "FIFO":
            self.run_fifo(processes)
        elif selected_algorithm == "SJF":
            self.run_sjf(processes)
        elif selected_algorithm == "Prioridad":
            self.run_priority(processes)
        else:
            QMessageBox.warning(self, f"El algoritmo {selected_algorithm} aún no está implementado")

    # Algoritmo de planificación de procesos FIFO
    def run_fifo(self, processes):
        """
        DESCRIPCIÓN:    Se ejecuta el algoritmo de planificación de procesos FIFO. Se organizan los procesos
                        por tiempo de llegada y se ejecutan en el orden en que llegaron.

        ENTRADA: processes (list) - Lista de procesos con los datos de cada proceso.

        SALIDA: Ninguna.
        """
        # Se organizan los procesos por tiempo de llegada
        processes = sorted(processes, key=lambda x: x['llegada'])
        time_elapsed = processes[0]['llegada'] # Se inicializa el tiempo en el tiempo de llegada del primer proceso
        completion_times = []
        wait_times = []
        system_times = []

        for process in processes:
            time_elapsed = max(time_elapsed, process['llegada']) # Se asegura que el tiempo de llegada sea el correcto
            start_time = time_elapsed
            time_elapsed += process['ejecucion']
            completion_times.append(time_elapsed)

            wait_time = start_time - process['llegada']
            system_time = time_elapsed - process['llegada']

            wait_times.append(wait_time)
            system_times.append(system_time)
        
        # Se muestra la gráfica y los resultados en el mismo diálogo
        self.show_combined_results(processes, wait_times, system_times, completion_times)

    # Algoritmo de planificación de procesos SJF
    def run_sjf(self, processes):
        """
        DESCRIPCIÓN:    Se ejecuta el algoritmo de planificación de procesos SJF. Se organizan los procesos
                        por ráfaga de CPU y se ejecutan en el orden en que llegaron.

        ENTRADA: processes (list) - Lista de procesos con los datos de cada proceso.

        SALIDA: Ninguna.
        """
        time_elapsed = 0
        completion_times = []
        processes_sorted = []
        wait_times = []
        system_times = []
        
        while processes:
            # Se seleccionan los procesos que han llegado
            procesos_disponibles = [process for process in processes if process['llegada'] <= time_elapsed]
            if procesos_disponibles:
                # Se escoge el proceso con la ráfaga más corta
                proceso_actual = min(procesos_disponibles, key=lambda x: x['ejecucion'])
            else:
                # Si no hay procesos disponibles, se avanza al siguiente proceso
                proceso_actual = min(processes, key=lambda x: x['llegada'])
                time_elapsed = proceso_actual['llegada']
            
            start_time = time_elapsed
            time_elapsed = max(time_elapsed, proceso_actual['llegada'])
            time_elapsed += proceso_actual['ejecucion']
            completion_times.append(time_elapsed)
            processes_sorted.append(proceso_actual)

            wait_time = start_time - proceso_actual['llegada']
            system_time = time_elapsed - proceso_actual['llegada']

            wait_times.append(wait_time)
            system_times.append(system_time)

            processes.remove(proceso_actual)
        
        # Se muestra la gráfica y los resultados en el mismo diálogo
        self.show_combined_results(processes, wait_times, system_times, completion_times)
    

    # Algoritmo de planificación de procesos por prioridad
    def run_priority(self, processes):
        """
        DESCRIPCIÓN:    Se ejecuta el algoritmo de planificación de procesos por prioridad. Se organizan los procesos
                        por prioridad y se ejecutan en el orden en que llegaron.

        ENTRADA: processes (list) - Lista de procesos con los datos de cada proceso.

        SALIDA: Ninguna.
        """
        # Se seleccionan los procesos que han llegado
        time_elapsed = 0
        completion_times = []
        processes_sorted = []
        wait_times = []
        system_times = []

        while processes:
            # Se seleccionan los procesos que han llegado
            procesos_disponibles = [process for process in processes if process['llegada'] <= time_elapsed]
            if procesos_disponibles:
                # Se escoge el proceso con la prioridad más alta (el menor número)
                proceso_actual = min(procesos_disponibles, key=lambda x: x['prioridad'])
            else:
                # Si no hay procesos disponibles, se avanza al siguiente proceso
                proceso_actual = min(processes, key=lambda x: x['llegada'])
                time_elapsed = proceso_actual['llegada']
        
            start_time = time_elapsed
            time_elapsed = max(time_elapsed, proceso_actual['llegada'])
            time_elapsed += proceso_actual['ejecucion']
            completion_times.append(time_elapsed)
            processes_sorted.append(proceso_actual)

            wait_time = start_time - proceso_actual['llegada']
            system_time = time_elapsed - proceso_actual['llegada']

            wait_times.append(wait_time)
            system_times.append(system_time)

            processes.remove(proceso_actual)
        
        # Se muestra la gráfica y los resultados en el mismo diálogo
        self.show_combined_results(processes, wait_times, system_times, completion_times)
    
    # Función para mostrar los resultados combinados
    def show_combined_results(self, processes, wait_times, system_times, completion_times):
        """
        DESCRIPCIÓN:    Se la tabla de Gantt con los procesos y tiempos de ejecución.

        ENTRADA: procesos (list) - Lista de procesos con los datos de cada proceso.
                 wait_times (list) - Lista de tiempos de espera de cada proceso.
                 system_times (list) - Lista de tiempos de sistema de cada proceso.

        SALIDA: Ninguna.
        """
        dialog = QDialog(self)
        dialog.setWindowTitle("Resultados del Algoritmo")
        dialog.resize(1300, 500)

        # Se crea el contendor principal
        layout = QHBoxLayout(dialog)

        # Se crea y se agrega la gráfica de Gantt al lado izquierdo
        figure = Figure(figsize=(7, 5), dpi=100)
        canvas = FigureCanvas(figure)
        ax = figure.add_subplot(111)

        for i, process in enumerate(processes):
            ax.barh(process['nombre'], process['ejecucion'], left=completion_times[i] - process['ejecucion'], color='purple')

        ax.set_xlabel('Tiempo', fontsize=12, fontweight='bold')
        ax.set_ylabel('Proceso', fontsize=12, fontweight='bold')
        ax.set_title('Diagrama de Gantt - Algoritmo ' + self.algoritmo_selector.currentText(), fontsize=14, fontweight='bold')
        ax.set_xticks(range(0, int(max(completion_times) + 1), 2)) # Se ajusta la escala del eje x cada 2 unidades
        ax.grid(True)

        # Se agrega la gráfica al layout
        layout.addWidget(canvas)
        layout.setStretchFactor(canvas, 65)  # Se da más espacio a la gráfica (3/4 del total)


        # Se crea un layout vertical para la tabla y su título
        table_layout = QVBoxLayout()
    
        # Se crea y se agrega un título para la tabla de resultados
        table_title = QLabel("Resultados del Algoritmo")
        font = QFont()
        font.setPointSize(12) # Se ajusta el tamaño de la fuente
        font.setBold(True) # Se establece la fuente en negrita
        table_title.setFont(font)
        table_title.setAlignment(Qt.AlignCenter)
        table_layout.addWidget(table_title)  # Agregar el título al layout

        # Se crea y se agrega la tabla de resultados al lado derecho
        table = QTableWidget(dialog)
        table.setColumnCount(3)
        table.setHorizontalHeaderLabels(["Proceso", "Tiempo de espera", "Tiempo de sistema"])
        table.setRowCount(len(processes))

        # Se ajusta el tamaño de las columnas
        table.setColumnWidth(0, 100) # Columna de proceso
        table.setColumnWidth(1, 150) # Columna de Tiempo de espera
        table.setColumnWidth(2, 150) # Columna de tiempo en el sistema

        for i, process in enumerate(processes):
            table.setItem(i, 0, QTableWidgetItem(process['nombre']))
            table.setItem(i, 1, QTableWidgetItem(str(wait_times[i])))
            table.setItem(i, 2, QTableWidgetItem(str(system_times[i])))

        #table.resizeColumnsToContents()
        table_layout.addWidget(table)  # Se agrega la tabla al layout

        # Se agrega el layout de la tabla al layout principal
        layout.addLayout(table_layout)
        layout.setStretchFactor(table_layout, 35)  # Se da menos espacio a la tabla (1/4 del total)

        dialog.setLayout(layout)
        dialog.exec_() # Se muestra la tabla de resultados en modo bloqueante


    def show_about(self):
        """
        DESCRIPCIÓN:    Se muestra una ventana con información acerca del software y sus desarrolladores.

        ENTRADA: Ninguna.

        SALIDA: Ninguna.
        """
        QMessageBox.information(self, "About", "Este software fue desarrollado por Yuliana Melisa Vera y Alexander Castañeda.\nVersión 1.0 - 2024")

    def show_help(self):
        """
        DESCRIPCIÓN:    Se muestra una ventana con información acerca del uso del software y sus funcionalidades

        ENTRADA: Ninguna.

        SALIDA: Ninguna.
        """
        help_text = (
            "Este software permite seleccionar y ejecutar tres algoritmos de despacho para sistemas operativos:\n"
            "- FIFO: Primer proceso en llegar, primer proceso en ser ejecutado.\n"
            "- SJF: Proceso con la ráfaga más corta se ejecuta primero.\n"
            "- Prioridad: Proceso con la prioridad más alta se ejecuta primero.\n\n"
            "Instrucciones:\n"
            "1. Seleccione el algoritmo deseado desde el menú desplegable.\n"
            "2. Ingrese los datos de los procesos: nombre, ráfaga de CPU, tiempo de llegada y prioridad (si aplica).\n"
            "3. Haga clic en 'Ejecutar Algoritmo' para generar la gráfica de Gantt."
        )
        QMessageBox.information(self, "Help", help_text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Despacho()
    sys.exit(app.exec_())