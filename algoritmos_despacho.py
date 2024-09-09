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
        ayuda_menu.addAction('About', self.mostrar_about)
        ayuda_menu.addAction('Help', self.mostrar_ayuda)
        menubar.addMenu(ayuda_menu)

        layout = QVBoxLayout()
        layout.setMenuBar(menubar) # Se añade el menú a la ventana

        # Se crea el menú desplegable para seleccionar el algortimo
        self.algoritmo_selector = QComboBox(self)
        self.algoritmo_selector.addItems(["FIFO", "SJF", "Prioridad"])
        self.algoritmo_selector.currentIndexChanged.connect(self.actualizar_columnas_tabla)
        layout.addWidget(QLabel("Seleccione Algoritmo:"))
        layout.addWidget(self.algoritmo_selector)

        # Se crea la tabla  para ingresar procesos
        self.tabla = QTableWidget(self)
        self.tabla.setAlternatingRowColors(True)  # Habilitar colores alternados
        self.tabla.setStyleSheet("""
            QTableWidget {
                background-color: #F5F5F5;  /* Color de fondo predeterminado */
                alternate-background-color: #E8FFEF;  /* Color de fondo alternado */
                selection-background-color: #BEF7D0;  /* Color de selección */
            }
            QTableWidget::item:selected {
                background-color: #D4FFE1;  /* Color de fondo al seleccionar */
            }
        """)
        self.tabla.setColumnCount(4)
        self.tabla.setHorizontalHeaderLabels(["Proceso", "Ráfaga (CPU)", "Tiempo de llegada", "Prioridad"])
        layout.addWidget(self.tabla)

        # Estilo para el encabezado horizontal
        self.tabla.horizontalHeader().setStyleSheet(
        "QHeaderView::section { background-color: lightblue; color: black; font-weight: bold; border: 1px solid black; }"
        )
        

        # Se ajusta el tamaño de las columnas
        self.tabla.setColumnWidth(0, 100) # Columna de proceso
        self.tabla.setColumnWidth(1, 100) # Columna de ráfaga
        self.tabla.setColumnWidth(2, 150) # Columna de tiempo de llegada
        self.tabla.setColumnWidth(3, 100) # Columna de prioridad

        # Se crea un botón para agregar filas a la tabla
        self.boton_adicionar_fila = QPushButton("Agregar Proceso", self)
        self.boton_adicionar_fila.clicked.connect(self.adicionar_fila)
        layout.addWidget(self.boton_adicionar_fila)

        # Se crea un botón para eliminar la última fila
        self.boton_remover_fila = QPushButton("Eliminar Última Fila", self)
        self.boton_remover_fila.clicked.connect(self.remover_ultima_fila)
        layout.addWidget(self.boton_remover_fila)

        # Se crea un botón para ejecutar el algoritmo seleccionado
        self.boton_ejecutar = QPushButton("Ejecutar Algoritmo", self)
        self.boton_ejecutar.clicked.connect(self.correr_algoritmo)
        layout.addWidget(self.boton_ejecutar)

        # Aplicar colores a los botones
        self.boton_adicionar_fila.setStyleSheet("background-color: '#6eff70'; color: black;")
        self.boton_remover_fila.setStyleSheet("background-color: '#ffc34c'; color: black;")
        self.boton_ejecutar.setStyleSheet("background-color: '#4cabff'; color: black;")


        # Cambiar el fondo de la ventana
        self.setStyleSheet("background-color: lightgray;")

        # Se establece el tamaño de la ventana
        self.resize(800, 500) # Se ajusta el tamaño de la ventana (ancho, alto)

        # Se establece el layout principal
        self.setLayout(layout)
        self.setWindowTitle("Simulador de Algoritmos de Despacho")
        self.actualizar_columnas_tabla() # Se asegura que las columnas se actualicen al inicio
        self.show()

    def adicionar_fila(self):
        """
        DESCRIPCIÓN:    Se añade una fila a la tabla de procesos con los campos necesarios para 
                        ingresar los datos de un nuevo proceso.

        ENTRADA: Ninguna.

        SALIDA: Ninguna.
        """
        Posicion_fila = self.tabla.rowCount()
        self.tabla.insertRow(Posicion_fila)
        # Se autocompleta el nombre del proceso para no estar ingresando el nombre de cada proceso manualmente
        self.tabla.setItem(Posicion_fila, 0, QTableWidgetItem(f"P{Posicion_fila + 1}"))

    def remover_ultima_fila(self):
        """
        DESCRIPCIÓN:    Se elimina la última fila de la tabla de procesos.

        ENTRADA: Ninguna.

        SALIDA: Ninguna.
        """
        posicion_fila = self.tabla.rowCount()
        if posicion_fila > 0:
            self.tabla.removeRow(posicion_fila - 1)


    def actualizar_columnas_tabla(self):
        """
        DESCRIPCIÓN:    Se actualizan las columnas de la tabla dependiendo del algoritmo seleccionado.
                        Se oculta la columna de prioridad si el algoritmo seleccionado es FIFO o SJF, y se muestra
                        en caso contrario.

        ENTRADA: Ninguna.

        SALIDA: Ninguna.
        """
        # Se actualizan las columnas de la tabla dependiendo del algoritmo seleccionado
        algoritmo_seleccionado = self.algoritmo_selector.currentText()
        self.tabla.setRowCount(0) # Se limpian las filas al cambiar de algoritmo

        if algoritmo_seleccionado in ["FIFO", "SJF"]:
            self.tabla.setColumnHidden(3, True) # Se oculta la columna de prioridad
        else:
            self.tabla.setColumnHidden(3, False) # Se muestra la columna de prioridad

    def validar_entrada_datos(self):
        """
        Se valida que los valores de la tabla sean mayores o iguales a cero, y que no estén vacíos.

        ENTRADA: Ninguna.

        SALIDA: bool - True si los datos son válidos, False en caso contrario.
        """
        for fila in range(self.tabla.rowCount()):
            # Validar los campos de ráfaga, tiempo de llegada (siempre presentes)
            for columna in range(1, 3):  # Columnas 1: ráfaga, 2: tiempo de llegada
                item = self.tabla.item(fila, columna)
                if not item or not item.text().isdigit() or int(item.text()) < 0:
                    QMessageBox.warning(self, "Error de Validación", "Por favor, complete todos los campos e ingrese números mayores o iguales a cero.")
                    return False  # Se detiene si hay error
            
            # Solo se valida la prioridad si la columna no está oculta (algoritmo de prioridad)
            if not self.tabla.isColumnHidden(3):  # La columna 3 es la prioridad
                campo_prioridad = self.tabla.item(fila, 3)
                if not campo_prioridad or not campo_prioridad.text().isdigit() or int(campo_prioridad.text()) < 0:
                    QMessageBox.warning(self, "Error de Validación", "Por favor, complete todos los campos e ingrese números mayores o iguales a cero.")
                    return False  # Se detiene si hay error
        return True


    # Función para ejecutar el algoritmo seleccionado
    def correr_algoritmo(self):
        """
        DESCRIPCIÓN:    Se ejecuta el algoritmo seleccionado en la tabla de procesos. Se obtienen los datos
                        ingresados en la tabla y se ejecuta el algoritmo correspondiente.
        
        ENTRADA: Ninguna.

        SALIDA: Ninguna.
        """
        if not self.validar_entrada_datos():
            return  # Detener si la validación falla

        # Aquí se ejecuta el algoritmo seleccionado
        algoritmo_seleccionado = self.algoritmo_selector.currentText()
        procesos = []

        # Se obtienen los datos ingresados en la tabla
        for fila in range(self.tabla.rowCount()):
            nombre_proceso = self.tabla.item(fila, 0).text() if self.tabla.item(fila, 0) else ''
            tiempo_ragafa = int(self.tabla.item(fila, 1).text()) if self.tabla.item(fila, 1) else 0
            tiempo_llegada = int(self.tabla.item(fila, 2).text()) if self.tabla.item(fila, 2) else 0
            prioridad = int(self.tabla.item(fila, 3).text()) if self.tabla.item(fila, 3) and not self.tabla.isColumnHidden(3) else 0

            """
            # Se valida que no falten datos
            if not burst_time or not arrival_time:
                QMessageBox.warning(self, "Advertencia", "Por favor, complete todos los campos.")
                return
            """
            
            # Se añaden los procesos a la lista
            procesos.append({
                'nombre': nombre_proceso,
                'ejecucion': tiempo_ragafa,
                'llegada': tiempo_llegada,
                'prioridad': prioridad
            })
        
        # Nos aseguramos de que haya al menos un proceso antes de continuar
        if not procesos:
            QMessageBox.warning(self, "Advertencia", "Por favor, añada al menos un proceso.")
            return
        
        if algoritmo_seleccionado == "FIFO":
            self.ejecutar_fifo(procesos)
        elif algoritmo_seleccionado == "SJF":
            self.ejecutar_sjf(procesos)
        elif algoritmo_seleccionado == "Prioridad":
            self.ejecutar_prioridad(procesos)
        else:
            QMessageBox.warning(self, f"El algoritmo {algoritmo_seleccionado} aún no está implementado")

    # Algoritmo de planificación de procesos FIFO
    def ejecutar_fifo(self, procesos):
        """
        DESCRIPCIÓN:    Se ejecuta el algoritmo de planificación de procesos FIFO. Se organizan los procesos
                        por tiempo de llegada y se ejecutan en el orden en que llegaron.

        ENTRADA: processes (list) - Lista de procesos con los datos de cada proceso.

        SALIDA: Ninguna.
        """
        # Se organizan los procesos por tiempo de llegada
        procesos = sorted(procesos, key=lambda x: x['llegada'])
        tiempo_transcurrido = procesos[0]['llegada'] # Se inicializa el tiempo en el tiempo de llegada del primer proceso
        tiempos_de_finalizacion = []
        tiempos_de_espera = []
        tiempos_de_sistema = []

        for proceso in procesos:
            tiempo_transcurrido = max(tiempo_transcurrido, proceso['llegada']) # Se asegura que el tiempo de llegada sea el correcto
            tiempo_inicio = tiempo_transcurrido
            tiempo_transcurrido += proceso['ejecucion']
            tiempos_de_finalizacion.append(tiempo_transcurrido)

            tiempo_de_espera = tiempo_inicio - proceso['llegada']
            tiempo_de_sistema = tiempo_transcurrido - proceso['llegada']

            tiempos_de_espera.append(tiempo_de_espera)
            tiempos_de_sistema.append(tiempo_de_sistema)
        
        # Se muestra la gráfica y los resultados en el mismo diálogo
        self.mostrar_resultados(procesos, tiempos_de_espera, tiempos_de_sistema, tiempos_de_finalizacion)

    # Algoritmo de planificación de procesos SJF
    def ejecutar_sjf(self, procesos):
        """
        DESCRIPCIÓN:    Se ejecuta el algoritmo de planificación de procesos SJF. Se organizan los procesos
                        por ráfaga de CPU y se ejecutan en el orden en que llegaron.

        ENTRADA: processes (list) - Lista de procesos con los datos de cada proceso.

        SALIDA: Ninguna.
        """
        tiempo_transcurrido = 0
        tiempos_de_finalizacion = []
        procesos_ordenados = []
        tiempos_de_espera = []
        tiempos_de_sistema = []
        
        while procesos:
            # Se seleccionan los procesos que han llegado
            procesos_disponibles = [proceso for proceso in procesos if proceso['llegada'] <= tiempo_transcurrido]
            if procesos_disponibles:
                # Se escoge el proceso con la ráfaga más corta
                proceso_actual = min(procesos_disponibles, key=lambda x: x['ejecucion'])
            else:
                # Si no hay procesos disponibles, se avanza al siguiente proceso
                proceso_actual = min(procesos, key=lambda x: x['llegada'])
                tiempo_transcurrido = proceso_actual['llegada']
            
            tiempo_inicio = tiempo_transcurrido
            tiempo_transcurrido = max(tiempo_transcurrido, proceso_actual['llegada'])
            tiempo_transcurrido += proceso_actual['ejecucion']
            tiempos_de_finalizacion.append(tiempo_transcurrido)
            procesos_ordenados.append(proceso_actual)

            tiempo_de_espera = tiempo_inicio - proceso_actual['llegada']
            tiempo_de_sistema = tiempo_transcurrido - proceso_actual['llegada']

            tiempos_de_espera.append(tiempo_de_espera)
            tiempos_de_sistema.append(tiempo_de_sistema)

            procesos.remove(proceso_actual)
        
        # Se muestra la gráfica y los resultados en el mismo diálogo
        self.mostrar_resultados(procesos_ordenados, tiempos_de_espera, tiempos_de_sistema, tiempos_de_finalizacion)
    

    # Algoritmo de planificación de procesos por prioridad
    def ejecutar_prioridad(self, procesos):
        """
        DESCRIPCIÓN:    Se ejecuta el algoritmo de planificación de procesos por prioridad. Se organizan los procesos
                        por prioridad y se ejecutan en el orden en que llegaron.

        ENTRADA: processes (list) - Lista de procesos con los datos de cada proceso.

        SALIDA: Ninguna.
        """
        # Se seleccionan los procesos que han llegado
        tiempo_transcurrido = 0
        tiempos_de_finalizacion = []
        procesos_ordenados = []
        tiempos_de_espera = []
        tiempos_de_sistema = []

        while procesos:
            # Se seleccionan los procesos que han llegado
            procesos_disponibles = [procesos for procesos in procesos if procesos['llegada'] <= tiempo_transcurrido]
            if procesos_disponibles:
                # Se escoge el proceso con la prioridad más alta (el menor número)
                proceso_actual = min(procesos_disponibles, key=lambda x: x['prioridad'])
            else:
                # Si no hay procesos disponibles, se avanza al siguiente proceso
                proceso_actual = min(procesos, key=lambda x: x['llegada'])
                tiempo_transcurrido = proceso_actual['llegada']
        
            tiempo_de_inicio = tiempo_transcurrido
            tiempo_transcurrido = max(tiempo_transcurrido, proceso_actual['llegada'])
            tiempo_transcurrido += proceso_actual['ejecucion']
            tiempos_de_finalizacion.append(tiempo_transcurrido)
            procesos_ordenados.append(proceso_actual)

            tiempo_de_espera = tiempo_de_inicio - proceso_actual['llegada']
            tiempo_de_sistema = tiempo_transcurrido - proceso_actual['llegada']

            tiempos_de_espera.append(tiempo_de_espera)
            tiempos_de_sistema.append(tiempo_de_sistema)

            procesos.remove(proceso_actual)
        
        # Se muestra la gráfica y los resultados en el mismo diálogo
        self.mostrar_resultados(procesos_ordenados, tiempos_de_espera, tiempos_de_sistema, tiempos_de_finalizacion)
    
    # Función para mostrar los resultados combinados
    def mostrar_resultados(self, procesos, tiempos_de_espera, tiempos_de_sistema, tiempos_de_finalizacion):
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
        figura = Figure(figsize=(7, 5), dpi=100)
        canvas = FigureCanvas(figura)
        ax = figura.add_subplot(111)

        # Se crea una lista de colores para los procesos
        colores = ['#FF5733', '#33FF57', '#3357FF', '#F3FF33', '#33FFF5', '#FF33F5']

        # Creamos una lista de tuplas que relacione cada proceso con su tiempo de finalización
        procesos_con_tiempo = list(zip(procesos, tiempos_de_finalizacion))

        # Ordenamos los procesos según el orden original por su 'nombre'
        orden_original = [proceso['nombre'] for proceso in procesos]
        orden_original = sorted(orden_original)
        procesos_con_tiempo_ordenados = sorted(procesos_con_tiempo, key=lambda p: orden_original.index(p[0]['nombre']))
        print(procesos_con_tiempo_ordenados)

        # Iteramos sobre los procesos en el orden original, respetando su tiempo de finalización
        for i, (proceso, tiempo_finalizacion) in enumerate(procesos_con_tiempo_ordenados):
            color = colores[i % len(colores)]  # Selecciona un color de la lista
            alto_barra = 0.8 if len(procesos) > 3 else 0.4  # Ajusta el alto de la barra si hay más de 3 procesos
    
            # Grafica cada barra, respetando el tiempo de finalización
            ax.barh(proceso['nombre'], proceso['ejecucion'], 
            left=tiempo_finalizacion - proceso['ejecucion'],  # Calcula dónde debe comenzar la barra
            height=alto_barra, color=color)
        
        ax.set_xlabel('Tiempo', fontsize=12, fontweight='bold')
        ax.set_ylabel('Proceso', fontsize=12, fontweight='bold')
        ax.set_title('Diagrama de Gantt - Algoritmo ' + self.algoritmo_selector.currentText(), fontsize=14, fontweight='bold')
        ax.set_xticks(range(0, int(max(tiempos_de_finalizacion) + 1), 2)) # Se ajusta la escala del eje x cada 2 unidades
        ax.grid(True)

        # Se agrega la gráfica al layout
        layout.addWidget(canvas)
        layout.setStretchFactor(canvas, 65)  # Se da más espacio a la gráfica (65% del total)


        # Se crea un layout vertical para la tabla y su título
        diseno_tabla = QVBoxLayout()
    
        # Se crea y se agrega un título para la tabla de resultados
        titulo_tabla = QLabel("Resultados del Algoritmo")
        fuente = QFont()
        fuente.setPointSize(12) # Se ajusta el tamaño de la fuente
        fuente.setBold(True) # Se establece la fuente en negrita
  
        titulo_tabla.setFont(fuente)
        titulo_tabla.setAlignment(Qt.AlignCenter)
        diseno_tabla.addWidget(titulo_tabla)  # Agregar el título al layout

        # Se crea y se agrega la tabla de resultados al lado derecho
        tabla = QTableWidget(dialog)
        tabla.setColumnCount(3)
        tabla.setHorizontalHeaderLabels(["Proceso", "Tiempo de espera", "Tiempo de sistema"])

        tabla.horizontalHeader().setStyleSheet(
        "QHeaderView::section { background-color: '#a9a8ff'; color: black; font-weight: bold; }"
        )
        
        # Se cambia la fuente del encabezado
        encabezado = tabla.horizontalHeader()
        fuente = QFont("Arial", 10, QFont.Bold)
        encabezado.setFont(fuente)

        tabla.setEditTriggers(QTableWidget.NoEditTriggers) # Se deshabilita la edición de la tabla
        tabla.setRowCount(len(procesos) + 1) # Se añade una fila adicional para los promedios

        # Se ajusta el tamaño de las columnas
        tabla.setColumnWidth(0, 100) # Columna de proceso
        tabla.setColumnWidth(1, 150) # Columna de Tiempo de espera
        tabla.setColumnWidth(2, 170) # Columna de tiempo en el sistema

        tiempo_total_espera = 0
        tiempo_total_sistema = 0

        # Creamos un diccionario para mapear el nombre del proceso a su índice original
        proceso_a_indice = {proceso['nombre']: idx for idx, proceso in enumerate(procesos)}

        # Creamos una lista de índices que reflejen el orden en 'procesos_con_tiempos_ordenados'
        indices_ordenados = [proceso_a_indice[proceso['nombre']] for proceso, _ in procesos_con_tiempo_ordenados]

        # Reordenar tiempos_de_espera y tiempos_de_sistema
        tiempos_de_espera_ordenados = [tiempos_de_espera[idx] for idx in indices_ordenados]
        tiempos_de_sistema_ordenados = [tiempos_de_sistema[idx] for idx in indices_ordenados]


        for i, proceso in enumerate(procesos_con_tiempo_ordenados):
            dic_proceso = proceso[0]
            nombre_proceso = dic_proceso['nombre']
            tiempo_total_espera += tiempos_de_espera[i]
            tiempo_total_sistema += tiempos_de_sistema[i]
            tabla.setItem(i, 0, QTableWidgetItem(nombre_proceso))
            tabla.setItem(i, 1, QTableWidgetItem(str(tiempos_de_espera_ordenados[i])))
            tabla.setItem(i, 2, QTableWidgetItem(str(tiempos_de_sistema_ordenados[i])))

        # Se calculan los promedios
        tiempo_promedio_espera = tiempo_total_espera / len(procesos)
        tiempo_promedio_sistema = tiempo_total_sistema / len(procesos)

        # Se crea una fila adicional para los promedios personalizada
        item_promedio = QTableWidgetItem("Promedio")
        item_promedio.setFont(QFont("Arial", 12, QFont.Bold)) # Se establece la fuente en negrita
        item_promedio.setForeground(Qt.black) # Se establece el color del texto en negro

        item_promedio_espera = QTableWidgetItem(str(round(tiempo_promedio_espera, 2)))
        item_promedio_espera.setFont(QFont("Arial", 10, QFont.Bold)) # Se establece la fuente en negrita

        item_promedio_sistema = QTableWidgetItem(str(round(tiempo_promedio_sistema, 2)))
        item_promedio_sistema.setFont(QFont("Arial", 10, QFont.Bold)) # Se establece la fuente en negrita

        # Se añaden los promedios a la tabla
        tabla.setItem(len(procesos), 0, item_promedio)
        tabla.setItem(len(procesos), 1, item_promedio_espera)
        tabla.setItem(len(procesos), 2, item_promedio_sistema)

        #table.resizeColumnsToContents()
        diseno_tabla.addWidget(tabla)  # Se agrega la tabla al layout

        # Se agrega el layout de la tabla al layout principal
        layout.addLayout(diseno_tabla)
        layout.setStretchFactor(diseno_tabla, 35)  # Se da menos espacio a la tabla (35% del total)

        dialog.setLayout(layout)
        dialog.exec_() # Se muestra la tabla de resultados en modo bloqueante


    def mostrar_about(self):
        """
        DESCRIPCIÓN:    Se muestra una ventana con información acerca del software y sus desarrolladores.

        ENTRADA: Ninguna.

        SALIDA: Ninguna.
        """
        QMessageBox.information(self, "About", "Este software fue desarrollado por Yuliana Melisa Vera y Alexander Castañeda.\nVersión 1.0 - 2024")

    def mostrar_ayuda(self):
        """
        DESCRIPCIÓN:    Se muestra una ventana con información acerca del uso del software y sus funcionalidades

        ENTRADA: Ninguna.

        SALIDA: Ninguna.
        """
        texto_ayuda = (
            "Este software permite seleccionar y ejecutar tres algoritmos de despacho para sistemas operativos:\n"
            "- FIFO: Primer proceso en llegar, primer proceso en ser ejecutado.\n"
            "- SJF: Proceso con la ráfaga más corta se ejecuta primero.\n"
            "- Prioridad: Proceso con la prioridad más alta se ejecuta primero.\n\n"
            "Instrucciones:\n"
            "1. Seleccione el algoritmo deseado desde el menú desplegable.\n"
            "2. Haga clic en 'Agregar Proceso' para añadir una fila a la tabla, el nombre del proceso se agrega automáticamente..\n"
            "3. Ingrese los datos de los procesos: Ráfaga de CPU, tiempo de llegada y prioridad (si aplica).\n"
            "4. Haga clic en 'Eliminar Última Fila' para eliminar la última fila de la tabla.\n"
            "5. Haga clic en 'Ejecutar Algoritmo' para generar la gráfica de Gantt, calcular los tiempos de espera, tiempos de sistema y los promedios correspondientes."
        )
        QMessageBox.information(self, "Help", texto_ayuda)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Despacho()
    sys.exit(app.exec_())
