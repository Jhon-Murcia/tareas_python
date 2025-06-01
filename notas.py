import tkinter as tk # Importa el módulo tkinter, que es la biblioteca estándar de Python para crear interfaces gráficas de usuario (GUI).
from tkinter import messagebox, simpledialog # Importa los submódulos messagebox (para cuadros de diálogo) y simpledialog (para diálogos de entrada simple) de tkinter.
import json # Importa el módulo json, que permite trabajar con datos en formato JSON (serializar y deserializar).
import os # Importa el módulo os, que proporciona funciones para interactuar con el sistema operativo, como la gestión de rutas de archivos y directorios.
from PIL import Image, ImageTk # Importa las clases Image y ImageTk del módulo PIL (Pillow), necesarias para trabajar con imágenes (abrir, redimensionar, convertir a formato compatible con Tkinter).

NOTAS_FILE = "data/notas.json" # Define una constante con la ruta al archivo JSON donde se almacenarán las notas.

def cargar_notas():
    """Carga las notas desde el archivo JSON.""" # Docstring que describe la función.
    if not os.path.exists(NOTAS_FILE): # Comprueba si el archivo de notas no existe en la ruta especificada.
        return {} # Si el archivo no existe, devuelve un diccionario vacío, indicando que no hay notas.
    with open(NOTAS_FILE, 'r') as f: # Abre el archivo de notas en modo lectura ('r').
        return json.load(f) # Carga (deserializa) el contenido JSON del archivo y lo devuelve como un diccionario de Python.

def guardar_notas(notas):
    """Guarda las notas en el archivo JSON.""" # Docstring que describe la función.
    # Asegurarse de que el directorio 'data' exista
    os.makedirs(os.path.dirname(NOTAS_FILE), exist_ok=True) # Crea el directorio 'data' si no existe; 'exist_ok=True' evita un error si ya existe.
    with open(NOTAS_FILE, 'w') as f: # Abre el archivo de notas en modo escritura ('w'). Si no existe, lo crea; si existe, sobrescribe su contenido.
        json.dump(notas, f, indent=4) # Guarda (serializa) el diccionario de notas en el archivo JSON, con una indentación de 4 espacios para legibilidad.

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


def crear_nueva_nota(usuario):
    """Crea una nueva ventana para añadir una nota.""" # Docstring que describe la función.
    win = tk.Toplevel() # Crea una nueva ventana de nivel superior (Toplevel), que es una ventana independiente.
    win.title("Nueva Nota") # Establece el título de la ventana.
    win.configure(bg="#F8F8F8") # Configura el color de fondo de la ventana a un gris muy claro.
    win.transient(win.master) # Hace que la ventana sea transitoria con respecto a su ventana maestra (el menú principal), lo que significa que se minimizará y cerrará con ella.
    win.grab_set() # Captura todos los eventos de entrada del usuario para esta ventana, haciéndola modal (el usuario no puede interactuar con otras ventanas de la aplicación hasta que esta se cierre).

    # Dimensiones para centrar
    window_width = 450 # Define el ancho deseado para la ventana.
    window_height = 450 # Define la altura deseada para la ventana.
    _centrar_ventana(win, window_width, window_height) # Llama a la función auxiliar para centrar la ventana en la pantalla.

    # Encabezado destacado
    header_frame = tk.Frame(win, bg="#E0E0E0", padx=15, pady=10) # Crea un Frame para el encabezado, con un fondo gris claro y padding.
    header_frame.pack(fill="x", pady=(0, 15)) # Empaqueta el Frame del encabezado para que se expanda horizontalmente y añada padding inferior.
    tk.Label(header_frame, text="📝 Agregar Nota", font=("Helvetica", 16, "bold"), fg="#333333", bg="#E0E0E0").pack(anchor="w") # Crea una etiqueta para el título del encabezado con un ícono y estilo.

    # Frame principal para el contenido (campos y botón)
    content_frame = tk.Frame(win, bg="#F8F8F8", padx=20, pady=10) # Crea un Frame para el contenido principal (campos de entrada y botones), con un fondo claro y padding.
    content_frame.pack(expand=True, fill="both") # Empaqueta el Frame del contenido para que se expanda y rellene todo el espacio disponible.

    # Título de la nota
    tk.Label(content_frame, text="Título:", font=("Helvetica", 12, "bold"), bg="#F8F8F8", fg="#555555").pack(anchor="w", pady=(5, 2)) # Crea una etiqueta para el campo de título, alineada a la izquierda.
    titulo_entry = tk.Entry(content_frame, font=("Helvetica", 12), bd=1, relief="solid", # Crea un campo de entrada (Entry) para el título de la nota.
                            highlightbackground="#CCCCCC", highlightthickness=1, width=40) # Añade un borde sutil y un ancho fijo para visibilidad.
    titulo_entry.pack(fill="x", padx=5, pady=(0, 10)) # Empaqueta el campo de título, permitiendo que se expanda horizontalmente y con padding.

    # Contenido de la nota
    tk.Label(content_frame, text="Contenido:", font=("Helvetica", 12, "bold"), bg="#F8F8F8", fg="#555555").pack(anchor="w", pady=(5, 2)) # Crea una etiqueta para el campo de contenido.
    contenido_text = tk.Text(content_frame, height=10, width=40, bd=1, relief="solid", # Crea un campo de texto multi-línea (Text) para el contenido.
                             highlightbackground="#CCCCCC", highlightthickness=1) # Añade un borde sutil y dimensiones iniciales.
    contenido_text.pack(fill="both", expand=True, padx=5, pady=(0, 15)) # Empaqueta el campo de contenido, permitiendo que se expanda y rellene.

    def guardar():
        """Guarda la nueva nota.""" # Docstring que describe la función interna.
        titulo = titulo_entry.get().strip() # Obtiene el texto del título y elimina espacios en blanco al inicio/final.
        contenido = contenido_text.get("1.0", tk.END).strip() # Obtiene el texto del contenido (desde la primera línea, primer carácter hasta el final) y elimina espacios en blanco.
        if not titulo: # Comprueba si el campo de título está vacío.
            messagebox.showwarning("Advertencia", "El título no puede estar vacío") # Muestra una advertencia.
            return # Sale de la función si el título está vacío.

        notas = cargar_notas() # Carga las notas existentes desde el archivo JSON.
        if usuario not in notas: # Comprueba si el usuario actual no tiene notas registradas.
            notas[usuario] = [] # Si no tiene, inicializa una lista vacía para sus notas.
        notas[usuario].append({"titulo": titulo, "contenido": contenido}) # Añade la nueva nota (como un diccionario) a la lista de notas del usuario.
        guardar_notas(notas) # Guarda la lista actualizada de notas en el archivo.
        messagebox.showinfo("Éxito", "Nota guardada con éxito") # Muestra un mensaje de éxito.
        win.destroy() # Cierra la ventana actual de "Nueva Nota".
        win.grab_release() # Libera el "grab" de la ventana, permitiendo la interacción con otras ventanas de la aplicación.

    # Botón "Guardar nota" estilizado
    _crear_boton_estilizado(content_frame, "Guardar nota", guardar, "#4CAF50", "white", icon_char="💾") # Crea el botón "Guardar nota" con un estilo predefinido (verde, texto blanco, icono de disquete).
    
    # Protocolo para liberar el grab si la ventana se cierra con la "X"
    win.protocol("WM_DELETE_WINDOW", lambda: [win.grab_release(), win.destroy()]) # Configura un protocolo para que al cerrar la ventana con la "X", se libere el grab y se destruya la ventana.


def mostrar_notas(usuario):
    """Muestra una lista de notas del usuario y permite ver/editar/eliminar.""" # Docstring que describe la función.
    notas = cargar_notas().get(usuario, []) # Carga las notas del usuario actual; si no hay, devuelve una lista vacía.

    win = tk.Toplevel() # Crea una nueva ventana de nivel superior.
    win.title("Mis Notas") # Establece el título de la ventana.
    win.configure(bg="#F8F8F8") # Configura el color de fondo.
    win.transient(win.master) # Hace la ventana transitoria con respecto a su ventana maestra.
    win.grab_set() # Hace la ventana modal.

    window_width = 550 # Define el ancho de la ventana.
    window_height = 500 # Define la altura de la ventana.
    _centrar_ventana(win, window_width, window_height) # Centra la ventana en la pantalla.

    # Encabezado destacado
    header_frame = tk.Frame(win, bg="#E0E0E0", padx=15, pady=10) # Crea un Frame para el encabezado.
    header_frame.pack(fill="x", pady=(0, 15)) # Empaqueta el encabezado.
    tk.Label(header_frame, text="📚 Mis Notas", font=("Helvetica", 16, "bold"), fg="#333333", bg="#E0E0E0").pack(anchor="w") # Crea la etiqueta del título del encabezado.

    content_frame = tk.Frame(win, bg="#F8F8F8", padx=20, pady=10) # Crea un Frame para el contenido principal.
    content_frame.pack(expand=True, fill="both") # Empaqueta el contenido.

    # Lista de notas
    tk.Label(content_frame, text="Selecciona una nota:", font=("Helvetica", 12, "bold"), bg="#F8F8F8", fg="#555555").pack(anchor="w", pady=(5, 2)) # Etiqueta para la lista de notas.
    lista = tk.Listbox(content_frame, width=60, height=15, font=("Helvetica", 11), bd=1, relief="solid", # Crea un widget Listbox para mostrar las notas.
                       highlightbackground="#CCCCCC", highlightthickness=1, selectbackground="#B0E0E6", selectforeground="black") # Estilo para la Listbox.
    lista.pack(fill="both", expand=True, padx=5, pady=(0, 10)) # Empaqueta la Listbox.

    for nota in notas: # Itera sobre cada nota del usuario.
        lista.insert(tk.END, nota["titulo"]) # Inserta el título de cada nota en la Listbox.

    def ver_nota():
        """Abre una nueva ventana para ver/editar una nota seleccionada.""" # Docstring que describe la función interna.
        index = lista.curselection() # Obtiene el índice de la nota seleccionada en la Listbox.
        if not index: # Comprueba si no se ha seleccionado ninguna nota.
            messagebox.showwarning("Advertencia", "Por favor, selecciona una nota para ver.") # Muestra una advertencia.
            return # Sale de la función.
        i = index[0] # Obtiene el primer índice seleccionado.
        nota = notas[i] # Obtiene el diccionario de la nota seleccionada de la lista de notas.

        ver_win = tk.Toplevel() # Crea una nueva ventana para ver/editar la nota.
        ver_win.title("Ver / Editar Nota") # Establece el título.
        ver_win.configure(bg="#F8F8F8") # Configura el color de fondo.
        ver_win.transient(ver_win.master) # Hace la ventana transitoria.
        ver_win.grab_set() # Hace la ventana modal.

        ver_window_width = 450 # Define el ancho.
        ver_window_height = 500 # Define la altura.
        _centrar_ventana(ver_win, ver_window_width, ver_window_height) # Centra la ventana.

        # Encabezado destacado
        ver_header_frame = tk.Frame(ver_win, bg="#E0E0E0", padx=15, pady=10) # Crea un Frame para el encabezado.
        ver_header_frame.pack(fill="x", pady=(0, 15)) # Empaqueta el encabezado.
        tk.Label(ver_header_frame, text="✏️ Editar Nota", font=("Helvetica", 16, "bold"), fg="#333333", bg="#E0E0E0").pack(anchor="w") # Crea la etiqueta del título del encabezado.

        ver_content_frame = tk.Frame(ver_win, bg="#F8F8F8", padx=20, pady=10) # Crea un Frame para el contenido.
        ver_content_frame.pack(expand=True, fill="both") # Empaqueta el contenido.

        tk.Label(ver_content_frame, text="Título:", font=("Helvetica", 12, "bold"), bg="#F8F8F8", fg="#555555").pack(anchor="w", pady=(5, 2)) # Etiqueta para el título.
        titulo_entry = tk.Entry(ver_content_frame, font=("Helvetica", 12), bd=1, relief="solid", # Campo de entrada para el título.
                                highlightbackground="#CCCCCC", highlightthickness=1, width=40)
        titulo_entry.insert(0, nota["titulo"]) # Inserta el título actual de la nota en el campo.
        titulo_entry.pack(fill="x", padx=5, pady=(0, 10)) # Empaqueta el campo de título.

        tk.Label(ver_content_frame, text="Contenido:", font=("Helvetica", 12, "bold"), bg="#F8F8F8", fg="#555555").pack(anchor="w", pady=(5, 2)) # Etiqueta para el contenido.
        contenido_text = tk.Text(ver_content_frame, height=10, width=40, bd=1, relief="solid", # Campo de texto para el contenido.
                                 highlightbackground="#CCCCCC", highlightthickness=1)
        contenido_text.insert("1.0", nota["contenido"]) # Inserta el contenido actual de la nota en el campo.
        contenido_text.pack(fill="both", expand=True, padx=5, pady=(0, 15)) # Empaqueta el campo de contenido.

        def guardar_cambios():
            """Guarda los cambios en una nota existente.""" # Docstring que describe la función interna.
            notas[i]["titulo"] = titulo_entry.get().strip() # Actualiza el título de la nota con el valor del campo.
            notas[i]["contenido"] = contenido_text.get("1.0", tk.END).strip() # Actualiza el contenido de la nota.
            todas = cargar_notas() # Carga todas las notas de todos los usuarios.
            todas[usuario] = notas # Actualiza la lista de notas del usuario actual con los cambios.
            guardar_notas(todas) # Guarda todas las notas de nuevo en el archivo.
            messagebox.showinfo("Éxito", "Nota actualizada") # Muestra un mensaje de éxito.
            ver_win.destroy() # Cierra la ventana de ver/editar nota.
            ver_win.grab_release() # Libera el grab de la ventana.
            win.destroy() # Cierra la ventana de la lista de notas (para forzar una actualización).
            mostrar_notas(usuario) # Vuelve a abrir la ventana de la lista de notas para mostrar los cambios.

        def eliminar_nota():
            """Elimina la nota seleccionada.""" # Docstring que describe la función interna.
            if messagebox.askyesno("Confirmar", "¿Eliminar esta nota?"): # Pide confirmación al usuario antes de eliminar.
                notas.pop(i) # Elimina la nota de la lista de notas del usuario.
                todas = cargar_notas() # Carga todas las notas de todos los usuarios.
                todas[usuario] = notas # Actualiza la lista de notas del usuario actual.
                guardar_notas(todas) # Guarda todas las notas de nuevo en el archivo.
                messagebox.showinfo("Éxito", "Nota eliminada") # Muestra un mensaje de éxito.
                ver_win.destroy() # Cierra la ventana de ver/editar nota.
                ver_win.grab_release() # Libera el grab de la ventana.
                win.destroy() # Cierra la ventana de la lista de notas (para forzar una actualización).
                mostrar_notas(usuario) # Vuelve a abrir la ventana de la lista de notas para mostrar los cambios.

        # Botones de guardar cambios y eliminar nota estilizados
        _crear_boton_estilizado(ver_content_frame, "Guardar cambios", guardar_cambios, "#3498DB", "white", icon_char="💾") # Botón "Guardar cambios" con estilo.
        _crear_boton_estilizado(ver_content_frame, "Eliminar nota", eliminar_nota, "#E74C3C", "white", icon_char="🗑️") # Botón "Eliminar nota" con estilo.

        ver_win.protocol("WM_DELETE_WINDOW", lambda: [ver_win.grab_release(), ver_win.destroy()]) # Configura el protocolo de cierre para liberar el grab.

    # Botón "Ver nota seleccionada" estilizado
    _crear_boton_estilizado(content_frame, "Ver nota seleccionada", ver_nota, "#3498DB", "white", icon_char="👁️") # Botón "Ver nota seleccionada" con estilo.

    win.protocol("WM_DELETE_WINDOW", lambda: [win.grab_release(), win.destroy()]) # Configura el protocolo de cierre para la ventana principal de notas.
