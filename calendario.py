import tkinter as tk # Importa el módulo tkinter, que es la biblioteca estándar de Python para crear interfaces gráficas de usuario (GUI).
from tkinter import messagebox # Importa el submódulo messagebox de tkinter, utilizado para mostrar cuadros de diálogo de mensajes (información, advertencia, error).
from tkcalendar import Calendar # Importa la clase Calendar del módulo tkcalendar, que proporciona un widget de calendario para seleccionar fechas.
import json # Importa el módulo json, que permite trabajar con datos en formato JSON (serializar y deserializar).
import os # Importa el módulo os, que proporciona funciones para interactuar con el sistema operativo, como la gestión de rutas de archivos y directorios.

# Importar DateEntry también, ya que se usará en la ventana de ver/editar tarea
from tkcalendar import DateEntry # Importa la clase DateEntry del módulo tkcalendar, necesaria para el widget de entrada de fecha en la ventana de edición de tareas.

TAREAS_FILE = "data/tareas.json" # Define una constante con la ruta al archivo JSON donde se almacenarán las tareas.

def cargar_tareas():
    """Carga las tareas desde el archivo JSON.""" # Docstring que describe la función.
    if not os.path.exists(TAREAS_FILE): # Comprueba si el archivo de tareas no existe en la ruta especificada.
        return {} # Si el archivo no existe, devuelve un diccionario vacío, indicando que no hay tareas.
    with open(TAREAS_FILE, 'r') as f: # Abre el archivo de tareas en modo lectura ('r').
        return json.load(f) # Carga (deserializa) el contenido JSON del archivo y lo devuelve como un diccionario de Python.

def guardar_tareas(tareas):
    """Guarda las tareas en el archivo JSON.""" # Docstring que describe la función.
    # Asegurarse de que el directorio 'data' exista
    os.makedirs(os.path.dirname(TAREAS_FILE), exist_ok=True) # Crea el directorio 'data' si no existe; 'exist_ok=True' evita un error si ya existe.
    with open(TAREAS_FILE, 'w') as f: # Abre el archivo de tareas en modo escritura ('w'). Si no existe, lo crea; si existe, sobrescribe su contenido.
        json.dump(tareas, f, indent=4) # Guarda (serializa) el diccionario de tareas en el archivo JSON, con una indentación de 4 espacios para legibilidad.

# --- Funciones auxiliares para el estilo (copiadas de notas.py/tareas.py para consistencia) ---
def _centrar_ventana(win, width, height):
    """Centra una ventana Toplevel en la pantalla.""" # Docstring que describe la función.
    win.update_idletasks() # Fuerza a Tkinter a procesar todos los eventos pendientes y actualizar la geometría de la ventana, asegurando que win.winfo_width() y win.winfo_height() devuelvan valores correctos.
    
    # Obtener las dimensiones de la pantalla
    screen_width = win.winfo_screenwidth() # Obtiene el ancho de la pantalla del usuario en píxeles.
    screen_height = win.winfo_screenheight() # Obtiene la altura de la pantalla del usuario en píxeles.

    # Calcular la posición para centrar
    x = (screen_width // 2) - (width // 2) # Calcula la coordenada X para que la ventana quede centrada horizontalmente.
    y = (screen_height // 2) - (height // 2) # Calcula la coordenada Y para que la ventana quede centrada verticalmente.

    win.geometry(f'{width}x{height}+{x}+{y}') # Establece el tamaño y la posición de la ventana usando el formato "Ancho x Alto + X + Y".
    win.resizable(False, False) # Deshabilita la capacidad de la ventana para ser redimensionada por el usuario.

def _crear_boton_estilizado(parent_frame, texto, comando, bg_color, fg_color, icon_char=None):
    """
    Crea un botón con un estilo plano y moderno, y un posible ícono de texto.
    Simula un efecto de borde redondeado con el diseño.
    """ # Docstring que describe la función.
    button_frame = tk.Frame(parent_frame, bg=bg_color, relief="flat", bd=0) # Crea un Frame que actuará como contenedor del botón, con un color de fondo y sin relieve ni borde.
    button_frame.pack(pady=5, padx=5) # Empaqueta el Frame del botón, añadiendo un padding vertical y horizontal alrededor.

    # Usamos un Label dentro del Frame para el texto y el ícono
    label_text = f"{icon_char} {texto}" if icon_char else texto # Construye el texto del Label: si hay un ícono, lo añade antes del texto; si no, solo usa el texto.
    button_label = tk.Label( # Crea un widget Label que mostrará el texto y el ícono del botón.
        button_frame, # El Label se coloca dentro del button_frame.
        text=label_text, # El texto a mostrar en el Label.
        font=("Helvetica", 12, "bold"), # Define la fuente del texto (familia, tamaño, estilo).
        bg=bg_color, # Establece el color de fondo del Label igual al del Frame padre.
        fg=fg_color, # Establece el color del texto.
        padx=15, # Añade padding horizontal dentro del Label.
        pady=8 # Añade padding vertical dentro del Label.
    )
    button_label.pack(expand=True, fill="both") # Empaqueta el Label para que se expanda y rellene todo el espacio disponible dentro de button_frame.

    # Efecto hover
    def _on_enter(event): # Define una función interna que se ejecuta cuando el cursor entra en el área del botón.
        button_frame.config(bg=_darken_color(bg_color, 20)) # Oscurece el color de fondo del Frame del botón.
        button_label.config(bg=_darken_color(bg_color, 20)) # Oscurece el color de fondo del Label del botón.
        button_frame.config(cursor="hand2") # Cambia el cursor a una mano, indicando que es un elemento interactivo.

    def _on_leave(event): # Define una función interna que se ejecuta cuando el cursor sale del área del botón.
        button_frame.config(bg=bg_color) # Restaura el color de fondo original del Frame del botón.
        button_label.config(bg=bg_color) # Restaura el color de fondo original del Label del botón.
        button_frame.config(cursor="") # Restaura el cursor por defecto.

    button_frame.bind("<Enter>", _on_enter) # Vincula el evento de entrada del cursor al Frame del botón con la función _on_enter.
    button_frame.bind("<Leave>", _on_leave) # Vincula el evento de salida del cursor del Frame del botón con la función _on_leave.
    button_label.bind("<Enter>", _on_enter) # Vincula el evento de entrada del cursor al Label del botón con la función _on_enter.
    button_label.bind("<Leave>", _on_leave) # Vincula el evento de salida del cursor del Label del botón con la función _on_leave.

    # Vincula el comando al clic en el label y el frame
    button_frame.bind("<Button-1>", lambda e: comando()) # Vincula el clic izquierdo del ratón en el Frame del botón con la ejecución del comando.
    button_label.bind("<Button-1>", lambda e: comando()) # Vincula el clic izquierdo del ratón en el Label del botón con la ejecución del comando.

    return button_frame # Devuelve el Frame que contiene el botón estilizado.

def _darken_color(hex_color, amount):
    """Oscurece un color hexadecimal por un porcentaje dado.""" # Docstring que describe la función.
    hex_color = hex_color.lstrip('#') # Elimina el carácter '#' del inicio del string hexadecimal si está presente.
    rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4)) # Convierte el color hexadecimal a una tupla de valores RGB (rojo, verde, azul).
    darkened_rgb = tuple(max(0, c - amount) for c in rgb) # Resta la cantidad especificada a cada componente RGB, asegurándose de que el valor no sea menor que 0.
    return f'#{darkened_rgb[0]:02x}{darkened_rgb[1]:02x}{darkened_rgb[2]:02x}' # Convierte los valores RGB oscurecidos de nuevo a formato hexadecimal y los devuelve.
# --- Fin de funciones auxiliares ---

def _ver_tarea_desde_calendario(usuario, tarea_index, tareas_filtradas_por_fecha, main_calendar_win, refresh_calendar_list_callback):
    """
    Abre una nueva ventana para ver/editar una tarea seleccionada desde el calendario.
    Similar a ver_tarea en tareas.py, pero adaptada para este contexto.
    """ # Docstring que describe la función.
    # Obtenemos la tarea real de la lista filtrada por fecha
    tarea = tareas_filtradas_por_fecha[tarea_index] # Obtiene el diccionario de la tarea seleccionada de la lista de tareas filtradas.

    ver_win = tk.Toplevel() # Crea una nueva ventana de nivel superior para ver/editar la tarea.
    ver_win.title("Ver / Editar Tarea") # Establece el título de la ventana.
    ver_win.configure(bg="#F8F8F8") # Configura el color de fondo.
    ver_win.transient(main_calendar_win) # Hace que la ventana sea transitoria con respecto a la ventana principal del calendario.
    ver_win.grab_set() # Hace la ventana modal.

    ver_window_width = 450 # Define el ancho de la ventana.
    ver_window_height = 550 # Define la altura de la ventana (un poco más alta para la fecha).
    _centrar_ventana(ver_win, ver_window_width, ver_window_height) # Centra la ventana en la pantalla.

    # Encabezado destacado
    ver_header_frame = tk.Frame(ver_win, bg="#E0E0E0", padx=15, pady=10) # Crea un Frame para el encabezado.
    ver_header_frame.pack(fill="x", pady=(0, 15)) # Empaqueta el encabezado.
    tk.Label(ver_header_frame, text="✏️ Editar Tarea", font=("Helvetica", 16, "bold"), fg="#333333", bg="#E0E0E0").pack(anchor="w") # Crea la etiqueta del título del encabezado.

    ver_content_frame = tk.Frame(ver_win, bg="#F8F8F8", padx=20, pady=10) # Crea un Frame para el contenido principal.
    ver_content_frame.pack(expand=True, fill="both") # Empaqueta el contenido.

    tk.Label(ver_content_frame, text="Título:", font=("Helvetica", 12, "bold"), bg="#F8F8F8", fg="#555555").pack(anchor="w", pady=(5, 2)) # Etiqueta para el título.
    titulo_entry = tk.Entry(ver_content_frame, font=("Helvetica", 12), bd=1, relief="solid", # Campo de entrada para el título.
                            highlightbackground="#CCCCCC", highlightthickness=1, width=40)
    titulo_entry.insert(0, tarea["titulo"]) # Inserta el título actual de la tarea en el campo.
    titulo_entry.pack(fill="x", padx=5, pady=(0, 10)) # Empaqueta el campo de título.

    tk.Label(ver_content_frame, text="Contenido:", font=("Helvetica", 12, "bold"), bg="#F8F8F8", fg="#555555").pack(anchor="w", pady=(5, 2)) # Etiqueta para el contenido.
    contenido_text = tk.Text(ver_content_frame, height=10, width=40, bd=1, relief="solid", # Campo de texto para el contenido.
                             highlightbackground="#CCCCCC", highlightthickness=1)
    contenido_text.insert("1.0", tarea["contenido"]) # Inserta el contenido actual de la tarea en el campo.
    contenido_text.pack(fill="both", expand=True, padx=5, pady=(0, 15)) # Empaqueta el campo de contenido.

    tk.Label(ver_content_frame, text="Fecha de entrega:", font=("Helvetica", 12, "bold"), bg="#F8F8F8", fg="#555555").pack(anchor="w", pady=(5, 2)) # Etiqueta para la fecha de entrega.
    fecha_entry = DateEntry(ver_content_frame, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd', # Widget DateEntry para la fecha.
                            font=("Helvetica", 12))
    fecha_entry.set_date(tarea["fecha"]) # Establece la fecha actual de la tarea en el widget.
    fecha_entry.pack(padx=5, pady=(0, 15)) # Empaqueta el campo de fecha.

    def guardar_cambios():
        """Guarda los cambios en una tarea existente.""" # Docstring que describe la función interna.
        # Necesitamos encontrar la tarea original en la lista completa de tareas del usuario
        # para actualizarla, no solo en la lista filtrada por fecha.
        todas_las_tareas_usuario = cargar_tareas().get(usuario, []) # Carga todas las tareas del usuario desde el archivo.
        
        # Encontrar el índice de la tarea original en la lista completa
        # Esto asume que los títulos y contenidos son únicos o que la tarea original
        # no ha sido modificada en el título/contenido antes de esta edición para su identificación.
        # Una forma más robusta sería usar un ID único para cada tarea.
        original_index = -1 # Inicializa el índice de la tarea original.
        for idx, t in enumerate(todas_las_tareas_usuario): # Itera sobre todas las tareas del usuario con sus índices.
            if t == tarea: # Compara el diccionario completo de la tarea actual con la tarea original para encontrar su posición.
                original_index = idx # Almacena el índice si se encuentra la tarea.
                break # Sale del bucle una vez que se encuentra la tarea.
        
        if original_index != -1: # Si se encontró la tarea original.
            todas_las_tareas_usuario[original_index]["titulo"] = titulo_entry.get().strip() # Actualiza el título de la tarea.
            todas_las_tareas_usuario[original_index]["contenido"] = contenido_text.get("1.0", tk.END).strip() # Actualiza el contenido de la tarea.
            todas_las_tareas_usuario[original_index]["fecha"] = fecha_entry.get() # Actualiza la fecha de la tarea.
            
            todas_las_tareas_global = cargar_tareas() # Carga todas las tareas de todos los usuarios de nuevo.
            todas_las_tareas_global[usuario] = todas_las_tareas_usuario # Actualiza la sección del usuario actual con la lista modificada de tareas.
            guardar_tareas(todas_las_tareas_global) # Guarda todas las tareas (incluyendo los cambios) de nuevo en el archivo.
            messagebox.showinfo("Éxito", "Tarea actualizada") # Muestra un mensaje de éxito.
            ver_win.destroy() # Cierra la ventana de ver/editar tarea.
            ver_win.grab_release() # Libera el grab de la ventana.
            refresh_calendar_list_callback() # Llama a la función de callback para refrescar la lista de tareas en el calendario.
        else: # Si no se pudo encontrar la tarea original.
            messagebox.showerror("Error", "No se pudo encontrar la tarea original para actualizar.") # Muestra un mensaje de error.


    def eliminar_tarea():
        """Elimina la tarea seleccionada.""" # Docstring que describe la función interna.
        if messagebox.askyesno("Confirmar", "¿Eliminar esta tarea?"): # Pide confirmación al usuario antes de eliminar la tarea.
            todas_las_tareas_usuario = cargar_tareas().get(usuario, []) # Carga todas las tareas del usuario desde el archivo.
            original_index = -1 # Inicializa el índice de la tarea original.
            for idx, t in enumerate(todas_las_tareas_usuario): # Itera sobre todas las tareas del usuario.
                if t == tarea: # Compara el diccionario completo de la tarea para encontrar la original.
                    original_index = idx # Almacena el índice si se encuentra.
                    break # Sale del bucle.
            
            if original_index != -1: # Si se encontró la tarea original.
                todas_las_tareas_usuario.pop(original_index) # Elimina la tarea de la lista.
                todas_las_tareas_global = cargar_tareas() # Carga todas las tareas de todos los usuarios de nuevo.
                todas_las_tareas_global[usuario] = todas_las_tareas_usuario # Actualiza la sección del usuario actual con la lista modificada.
                guardar_tareas(todas_las_tareas_global) # Guarda todas las tareas (incluyendo la eliminación) de nuevo en el archivo.
                messagebox.showinfo("Éxito", "Tarea eliminada") # Muestra un mensaje de éxito.
                ver_win.destroy() # Cierra la ventana de ver/editar tarea.
                ver_win.grab_release() # Libera el grab de la ventana.
                refresh_calendar_list_callback() # Llama a la función de callback para refrescar la lista de tareas en el calendario.
            else: # Si no se pudo encontrar la tarea original.
                messagebox.showerror("Error", "No se pudo encontrar la tarea original para eliminar.") # Muestra un mensaje de error.

    # Botones de guardar cambios y eliminar tarea estilizados
    _crear_boton_estilizado(ver_content_frame, "Guardar cambios", guardar_cambios, "#3498DB", "white", icon_char="💾") # Crea el botón "Guardar cambios" con estilo.
    _crear_boton_estilizado(ver_content_frame, "Eliminar tarea", eliminar_tarea, "#E74C3C", "white", icon_char="🗑️") # Crea el botón "Eliminar tarea" con estilo.

    ver_win.protocol("WM_DELETE_WINDOW", lambda: [ver_win.grab_release(), ver_win.destroy()]) # Configura el protocolo de cierre para liberar el grab al cerrar la ventana con la "X".


def mostrar_calendario(usuario):
    """Muestra el calendario con las tareas del usuario.""" # Docstring que describe la función.
    # Cargamos todas las tareas del usuario una vez al inicio
    todas_las_tareas_del_usuario = cargar_tareas().get(usuario, []) # Carga todas las tareas del usuario actual desde el archivo.

    win = tk.Toplevel() # Crea una nueva ventana de nivel superior para el calendario.
    win.title("Calendario de Tareas") # Establece el título de la ventana.
    win.configure(bg="#F8F8F8") # Configura el color de fondo.
    win.transient(win.master) # Hace la ventana transitoria.
    win.grab_set() # Hace la ventana modal.

    # Dimensiones para centrar
    window_width = 600 # Define el ancho de la ventana.
    window_height = 650 # Define la altura de la ventana.
    _centrar_ventana(win, window_width, window_height) # Centra la ventana en la pantalla.

    # Encabezado destacado
    header_frame = tk.Frame(win, bg="#E0E0E0", padx=15, pady=10) # Crea un Frame para el encabezado.
    header_frame.pack(fill="x", pady=(0, 15)) # Empaqueta el encabezado.
    tk.Label(header_frame, text="📅 Calendario de Tareas", font=("Helvetica", 16, "bold"), fg="#333333", bg="#E0E0E0").pack(anchor="w") # Crea la etiqueta del título del encabezado.

    # Frame principal para el contenido
    content_frame = tk.Frame(win, bg="#F8F8F8", padx=20, pady=10) # Crea un Frame para el contenido principal.
    content_frame.pack(expand=True, fill="both") # Empaqueta el contenido.

    # Calendario
    tk.Label(content_frame, text="Selecciona una fecha:", font=("Helvetica", 12, "bold"), bg="#F8F8F8", fg="#555555").pack(pady=(5, 5)) # Etiqueta para el calendario.
    cal = Calendar(content_frame, selectmode='day', date_pattern='yyyy-mm-dd', # Crea el widget de calendario.
                   font=("Helvetica", 11), # Fuente del calendario.
                   background='darkblue', foreground='white', # Colores de fondo y texto del calendario.
                   normalbackground='white', # Fondo de los días normales.
                   weekendbackground='#F0F0F0', # Fondo de los fines de semana.
                   othermonthforeground='gray', # Color de texto de días de otros meses.
                   othermonthbackground='#E8E8E8', # Fondo de días de otros meses.
                   selectbackground='#3498DB', # Color de fondo del día seleccionado.
                   selectforeground='white', # Color de texto del día seleccionado.
                   headersbackground='#A9D0F5', # Color de fondo de los encabezados (días de la semana).
                   headersforeground='black', # Color de texto de los encabezados.
                   bordercolor='#CCCCCC', # Color del borde del calendario.
                   tooltipbackground='lightyellow', # Fondo del tooltip.
                   tooltipforeground='black' # Texto del tooltip.
                   )
    cal.pack(pady=10, padx=10, fill="both", expand=False) # Empaqueta el calendario.

    # Lista de tareas para la fecha seleccionada
    tk.Label(content_frame, text="Tareas para la fecha seleccionada:", font=("Helvetica", 12, "bold"), bg="#F8F8F8", fg="#555555").pack(anchor="w", pady=(15, 2)) # Etiqueta para la lista de tareas.
    lista = tk.Listbox(content_frame, width=60, height=10, font=("Helvetica", 11), bd=1, relief="solid", # Crea un widget Listbox para mostrar las tareas del día.
                       highlightbackground="#CCCCCC", highlightthickness=1, selectbackground="#B0E0E6", selectforeground="black") # Estilo para la Listbox.
    lista.pack(fill="both", expand=True, padx=5, pady=(0, 10)) # Empaqueta la Listbox.

    # Variable para almacenar las tareas que se muestran actualmente en la Listbox
    # Esto es crucial para saber qué tarea se selecciona al hacer clic
    tareas_en_listbox_actual = [] # Lista para almacenar los diccionarios completos de las tareas mostradas.

    def mostrar_tareas_fecha(event=None):
        """Muestra las tareas correspondientes a la fecha seleccionada en el calendario.""" # Docstring que describe la función interna.
        nonlocal tareas_en_listbox_actual # Declara que se usará la variable externa tareas_en_listbox_actual.
        fecha_seleccionada = cal.get_date() # Obtiene la fecha seleccionada del calendario.
        lista.delete(0, tk.END) # Limpia todos los elementos actuales de la Listbox.
        tareas_en_listbox_actual = [] # Resetea la lista de tareas mostradas.

        # Filtrar tareas por la fecha seleccionada
        tareas_para_fecha = [ # Crea una nueva lista conteniendo solo las tareas cuya fecha coincide con la seleccionada.
            tarea for tarea in todas_las_tareas_del_usuario if tarea["fecha"] == fecha_seleccionada
        ]
        
        if tareas_para_fecha: # Si hay tareas para la fecha seleccionada.
            for tarea in tareas_para_fecha: # Itera sobre las tareas filtradas.
                lista.insert(tk.END, f"{tarea['titulo']} - {tarea['fecha']}") # Inserta el título y la fecha de la tarea en la Listbox.
                tareas_en_listbox_actual.append(tarea) # Añade el diccionario completo de la tarea a la lista de tareas mostradas.
        else: # Si no hay tareas para la fecha seleccionada.
            lista.insert(tk.END, "No hay tareas para esta fecha.") # Inserta un mensaje indicando que no hay tareas.
            tareas_en_listbox_actual = [] # Asegura que la lista de tareas mostradas esté vacía.

    # Función para refrescar la lista de tareas en el calendario (llamada después de editar/eliminar)
    def refresh_calendar_tasks_list():
        nonlocal todas_las_tareas_del_usuario # Declara que se usará la variable externa todas_las_tareas_del_usuario.
        todas_las_tareas_del_usuario = cargar_tareas().get(usuario, []) # Recarga todas las tareas del usuario desde el archivo.
        mostrar_tareas_fecha() # Vuelve a llamar a mostrar_tareas_fecha para actualizar la Listbox con las tareas recargadas.

    def on_tarea_click(event):
        """Maneja el clic en un elemento de la lista de tareas.""" # Docstring que describe la función interna.
        index = lista.curselection() # Obtiene el índice del elemento seleccionado en la Listbox.
        if index: # Si se ha seleccionado un elemento.
            selected_index = index[0] # Obtiene el primer índice seleccionado.
            # Pasamos la tarea completa y el callback para refrescar el calendario
            _ver_tarea_desde_calendario(usuario, selected_index, tareas_en_listbox_actual, win, refresh_calendar_tasks_list) # Llama a la función para ver/editar la tarea, pasando los datos necesarios.

    # Vincular el evento de selección del calendario a la función
    cal.bind("<<CalendarSelected>>", mostrar_tareas_fecha) # Vincula el evento de selección de una fecha en el calendario con la función mostrar_tareas_fecha.
    
    # Vincular el evento de clic en la Listbox a la función on_tarea_click
    lista.bind("<<ListboxSelect>>", on_tarea_click) # Vincula el evento de selección de un elemento en la Listbox con la función on_tarea_click.

    # Llamar a la función una vez al inicio para mostrar las tareas de la fecha actual (o por defecto)
    refresh_calendar_tasks_list() # Llama a la función de refresco al inicio para poblar la lista de tareas.

    # Protocolo para liberar el grab si la ventana se cierra con la "X"
    win.protocol("WM_DELETE_WINDOW", lambda: [win.grab_release(), win.destroy()]) # Configura el protocolo de cierre para liberar el grab al cerrar la ventana con la "X".
