import tkinter as tk # Importa el módulo tkinter, que es la biblioteca estándar de Python para crear interfaces gráficas de usuario (GUI).
from tkinter import messagebox # Importa el submódulo messagebox de tkinter, utilizado para mostrar cuadros de diálogo de mensajes (información, advertencia, error).
import json # Importa el módulo json, que permite trabajar con datos en formato JSON (serializar y deserializar).
import os # Importa el módulo os, que proporciona funciones para interactuar con el sistema operativo, como la gestión de rutas de archivos y directorios.
from tkcalendar import DateEntry # Importa la clase DateEntry del módulo tkcalendar, que proporciona un widget de calendario para seleccionar fechas.

TAREAS_FILE = "data/tareas.json" # Define una constante con la ruta al archivo JSON donde se almacenarán las tareas.

def cargar_tareas():
    """Carga las tareas desde el archivo JSON.""" # Docstring que describe la función.
    if not os.path.exists(TAREAS_FILE): # Comprueba si el archivo de tareas no existe en la ruta especificada.
        return {} # Si el archivo no existe, devuelve un diccionario vacío, indicando que no hay tareas.
    with open(TAREAS_FILE, 'r') as f: # Abre el archivo de tareas en modo lectura ('r').
        return json.load(f) # Carga (deserializa) el contenido JSON del archivo y lo devuelve como un diccionario de Python.

def guardar_tareas(tareas):
    """Guarda las tareas en el archivo JSON.""" # Docstring que describe la función.
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


def agregar_tarea(usuario):
    """Crea una nueva ventana para añadir una tarea.""" # Docstring que describe la función.
    win = tk.Toplevel() # Crea una nueva ventana de nivel superior (Toplevel), que es una ventana independiente.
    win.title("Nueva Tarea") # Establece el título de la ventana.
    win.configure(bg="#F8F8F8") # Configura el color de fondo de la ventana a un gris muy claro.
    win.transient(win.master) # Hace que la ventana sea transitoria con respecto a su ventana maestra (el menú principal), lo que significa que se minimizará y cerrará con ella.
    win.grab_set() # Captura todos los eventos de entrada del usuario para esta ventana, haciéndola modal (el usuario no puede interactuar con otras ventanas de la aplicación hasta que esta se cierre).

    # Dimensiones para centrar
    window_width = 450 # Define el ancho deseado para la ventana.
    window_height = 500 # Define la altura deseada para la ventana (un poco más alta para la fecha).
    _centrar_ventana(win, window_width, window_height) # Llama a la función auxiliar para centrar la ventana en la pantalla.

    # Encabezado destacado
    header_frame = tk.Frame(win, bg="#E0E0E0", padx=15, pady=10) # Crea un Frame para el encabezado, con un fondo gris claro y padding.
    header_frame.pack(fill="x", pady=(0, 15)) # Empaqueta el Frame del encabezado para que se expanda horizontalmente y añada padding inferior.
    tk.Label(header_frame, text="➕ Agregar Tarea", font=("Helvetica", 16, "bold"), fg="#333333", bg="#E0E0E0").pack(anchor="w") # Crea una etiqueta para el título del encabezado con un ícono y estilo.

    # Frame principal para el contenido (campos y botón)
    content_frame = tk.Frame(win, bg="#F8F8F8", padx=20, pady=10) # Crea un Frame para el contenido principal (campos de entrada y botones), con un fondo claro y padding.
    content_frame.pack(expand=True, fill="both") # Empaqueta el Frame del contenido para que se expanda y rellene todo el espacio disponible.

    # Título de la tarea
    tk.Label(content_frame, text="Título:", font=("Helvetica", 12, "bold"), bg="#F8F8F8", fg="#555555").pack(anchor="w", pady=(5, 2)) # Crea una etiqueta para el campo de título, alineada a la izquierda.
    titulo_entry = tk.Entry(content_frame, font=("Helvetica", 12), bd=1, relief="solid", # Crea un campo de entrada (Entry) para el título de la tarea.
                            highlightbackground="#CCCCCC", highlightthickness=1, width=40) # Añade un borde sutil y un ancho fijo para visibilidad.
    titulo_entry.pack(fill="x", padx=5, pady=(0, 10)) # Empaqueta el campo de título, permitiendo que se expanda horizontalmente y con padding.

    # Contenido de la tarea
    tk.Label(content_frame, text="Contenido:", font=("Helvetica", 12, "bold"), bg="#F8F8F8", fg="#555555").pack(anchor="w", pady=(5, 2)) # Crea una etiqueta para el campo de contenido.
    contenido_text = tk.Text(content_frame, height=10, width=40, bd=1, relief="solid", # Crea un campo de texto multi-línea (Text) para el contenido.
                             highlightbackground="#CCCCCC", highlightthickness=1) # Añade un borde sutil y dimensiones iniciales.
    contenido_text.pack(fill="both", expand=True, padx=5, pady=(0, 15)) # Empaqueta el campo de contenido, permitiendo que se expanda y rellene.

    # Fecha de entrega
    tk.Label(content_frame, text="Fecha de entrega:", font=("Helvetica", 12, "bold"), bg="#F8F8F8", fg="#555555").pack(anchor="w", pady=(5, 2)) # Crea una etiqueta para la fecha de entrega.
    fecha_entry = DateEntry(content_frame, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd', # Crea un widget DateEntry para seleccionar la fecha.
                            font=("Helvetica", 12)) # Establece la fuente para el widget de fecha.
    fecha_entry.pack(padx=5, pady=(0, 15)) # Empaqueta el campo de fecha con padding.

    def guardar():
        """Guarda la nueva tarea.""" # Docstring que describe la función interna.
        titulo = titulo_entry.get().strip() # Obtiene el texto del título y elimina espacios en blanco.
        contenido = contenido_text.get("1.0", tk.END).strip() # Obtiene el texto del contenido y elimina espacios en blanco.
        fecha = fecha_entry.get() # Obtiene la fecha seleccionada.

        if not titulo: # Comprueba si el campo de título está vacío.
            messagebox.showwarning("Advertencia", "El título no puede estar vacío") # Muestra una advertencia.
            return # Sale de la función si el título está vacío.

        tareas = cargar_tareas() # Carga las tareas existentes.
        if usuario not in tareas: # Comprueba si el usuario actual no tiene tareas registradas.
            tareas[usuario] = [] # Si no tiene, inicializa una lista vacía para sus tareas.
        tareas[usuario].append({"titulo": titulo, "contenido": contenido, "fecha": fecha}) # Añade la nueva tarea (como un diccionario) a la lista de tareas del usuario.
        guardar_tareas(tareas) # Guarda la lista actualizada de tareas en el archivo.
        messagebox.showinfo("Éxito", "Tarea guardada con éxito") # Muestra un mensaje de éxito.
        win.destroy() # Cierra la ventana actual de "Nueva Tarea".
        win.grab_release() # Libera el "grab" de la ventana, permitiendo la interacción con otras ventanas.

    # Botón "Guardar tarea" estilizado
    _crear_boton_estilizado(content_frame, "Guardar tarea", guardar, "#4CAF50", "white", icon_char="💾") # Crea el botón "Guardar tarea" con estilo y su comando asociado.
    
    # Protocolo para liberar el grab si la ventana se cierra con la "X"
    win.protocol("WM_DELETE_WINDOW", lambda: [win.grab_release(), win.destroy()]) # Configura un protocolo para que al cerrar la ventana con la "X", se libere el grab y se destruya la ventana.


def ver_tareas(usuario):
    """Muestra una lista de tareas del usuario y permite ver/editar/eliminar.""" # Docstring que describe la función.
    tareas = cargar_tareas().get(usuario, []) # Carga las tareas del usuario actual; si no hay, devuelve una lista vacía.

    win = tk.Toplevel() # Crea una nueva ventana de nivel superior.
    win.title("Mis Tareas") # Establece el título de la ventana.
    win.configure(bg="#F8F8F8") # Configura el color de fondo.
    win.transient(win.master) # Hace la ventana transitoria.
    win.grab_set() # Hace la ventana modal.

    window_width = 550 # Define el ancho de la ventana.
    window_height = 550 # Define la altura de la ventana (un poco más alta para la lista y botones).
    _centrar_ventana(win, window_width, window_height) # Centra la ventana.

    # Encabezado destacado
    header_frame = tk.Frame(win, bg="#E0E0E0", padx=15, pady=10) # Crea un Frame para el encabezado.
    header_frame.pack(fill="x", pady=(0, 15)) # Empaqueta el encabezado.
    tk.Label(header_frame, text="✅ Mis Tareas", font=("Helvetica", 16, "bold"), fg="#333333", bg="#E0E0E0").pack(anchor="w") # Crea la etiqueta del título del encabezado.

    content_frame = tk.Frame(win, bg="#F8F8F8", padx=20, pady=10) # Crea un Frame para el contenido principal.
    content_frame.pack(expand=True, fill="both") # Empaqueta el contenido.

    # Lista de tareas
    tk.Label(content_frame, text="Selecciona una tarea:", font=("Helvetica", 12, "bold"), bg="#F8F8F8", fg="#555555").pack(anchor="w", pady=(5, 2)) # Crea una etiqueta para la lista.
    lista = tk.Listbox(content_frame, width=60, height=15, font=("Helvetica", 11), bd=1, relief="solid", # Crea un widget Listbox para mostrar las tareas.
                       highlightbackground="#CCCCCC", highlightthickness=1, selectbackground="#B0E0E6", selectforeground="black") # Estilo para la Listbox.
    lista.pack(fill="both", expand=True, padx=5, pady=(0, 10)) # Empaqueta la Listbox.

    for tarea in tareas: # Itera sobre cada tarea del usuario.
        lista.insert(tk.END, f"{tarea['titulo']} - {tarea['fecha']}") # Inserta el título y la fecha de la tarea en la Listbox.

    def ver_tarea():
        """Abre una nueva ventana para ver/editar una tarea seleccionada.""" # Docstring que describe la función interna.
        index = lista.curselection() # Obtiene el índice de la tarea seleccionada en la Listbox.
        if not index: # Comprueba si no se ha seleccionado ninguna tarea.
            messagebox.showwarning("Advertencia", "Por favor, selecciona una tarea para ver.") # Muestra una advertencia.
            return # Sale de la función.
        i = index[0] # Obtiene el primer índice seleccionado.
        tarea = tareas[i] # Obtiene el diccionario de la tarea seleccionada de la lista de tareas.

        ver_win = tk.Toplevel() # Crea una nueva ventana para ver/editar la tarea.
        ver_win.title("Ver / Editar Tarea") # Establece el título.
        ver_win.configure(bg="#F8F8F8") # Configura el color de fondo.
        ver_win.transient(ver_win.master) # Hace la ventana transitoria.
        ver_win.grab_set() # Hace la ventana modal.

        ver_window_width = 450 # Define el ancho.
        ver_window_height = 550 # Define la altura.
        _centrar_ventana(ver_win, ver_window_width, ver_window_height) # Centra la ventana.

        # Encabezado destacado
        ver_header_frame = tk.Frame(ver_win, bg="#E0E0E0", padx=15, pady=10) # Crea un Frame para el encabezado.
        ver_header_frame.pack(fill="x", pady=(0, 15)) # Empaqueta el encabezado.
        tk.Label(ver_header_frame, text="✏️ Editar Tarea", font=("Helvetica", 16, "bold"), fg="#333333", bg="#E0E0E0").pack(anchor="w") # Crea la etiqueta del título del encabezado.

        ver_content_frame = tk.Frame(ver_win, bg="#F8F8F8", padx=20, pady=10) # Crea un Frame para el contenido.
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
            tarea["titulo"] = titulo_entry.get().strip() # Actualiza el título de la tarea con el valor del campo.
            tarea["contenido"] = contenido_text.get("1.0", tk.END).strip() # Actualiza el contenido de la tarea.
            tarea["fecha"] = fecha_entry.get() # Actualiza la fecha de la tarea.
            todas = cargar_tareas() # Carga todas las tareas de todos los usuarios.
            todas[usuario] = tareas # Actualiza la lista de tareas del usuario actual con los cambios.
            guardar_tareas(todas) # Guarda todas las tareas de nuevo en el archivo.
            messagebox.showinfo("Éxito", "Tarea actualizada") # Muestra un mensaje de éxito.
            ver_win.destroy() # Cierra la ventana de ver/editar tarea.

        def eliminar_tarea():
            """Elimina la tarea seleccionada.""" # Docstring que describe la función interna.
            if messagebox.askyesno("Confirmar", "¿Eliminar esta tarea?"): # Pide confirmación al usuario antes de eliminar.
                tareas.pop(i) # Elimina la tarea de la lista de tareas del usuario.
                todas = cargar_tareas() # Carga todas las tareas de todos los usuarios.
                todas[usuario] = tareas # Actualiza la lista de tareas del usuario actual.
                guardar_tareas(todas) # Guarda todas las tareas de nuevo en el archivo.
                messagebox.showinfo("Éxito", "Tarea eliminada") # Muestra un mensaje de éxito.
                ver_win.destroy() # Cierra la ventana de ver/editar tarea.
                win.destroy() # Cierra la ventana de la lista de tareas (para forzar una actualización).
                ver_tareas(usuario) # Vuelve a abrir la ventana de la lista de tareas para mostrar los cambios.

        # Botones de guardar cambios y eliminar tarea estilizados
        _crear_boton_estilizado(ver_content_frame, "Guardar cambios", guardar_cambios, "#3498DB", "white", icon_char="💾") # Botón "Guardar cambios" con estilo.
        _crear_boton_estilizado(ver_content_frame, "Eliminar tarea", eliminar_tarea, "#E74C3C", "white", icon_char="🗑️") # Botón "Eliminar tarea" con estilo.

        ver_win.protocol("WM_DELETE_WINDOW", lambda: [ver_win.grab_release(), ver_win.destroy()]) # Configura el protocolo de cierre para liberar el grab.

    # Botón "Ver tarea seleccionada" estilizado
    _crear_boton_estilizado(content_frame, "Ver tarea seleccionada", ver_tarea, "#3498DB", "white", icon_char="👁️") # Botón "Ver tarea seleccionada" con estilo.

    win.protocol("WM_DELETE_WINDOW", lambda: [win.grab_release(), win.destroy()]) # Configura el protocolo de cierre para la ventana principal de tareas.
