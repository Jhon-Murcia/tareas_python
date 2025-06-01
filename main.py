import tkinter as tk # Importa el módulo tkinter, que es la biblioteca estándar de Python para crear interfaces gráficas de usuario (GUI).
from tkinter import messagebox # Importa el submódulo messagebox de tkinter, utilizado para mostrar cuadros de diálogo de mensajes (información, advertencia, error).
from PIL import Image, ImageTk # Importa las clases Image y ImageTk del módulo PIL (Pillow), necesarias para trabajar con imágenes (abrir, redimensionar, convertir a formato compatible con Tkinter).
import json # Importa el módulo json, que permite trabajar con datos en formato JSON (serializar y deserializar).
import os # Importa el módulo os, que proporciona funciones para interactuar con el sistema operativo, como la gestión de rutas de archivos y directorios.
from menu import MenuPrincipal # Importa la clase MenuPrincipal desde el archivo 'menu.py', que representa la ventana principal del menú de la aplicación.

# Ruta al archivo de usuarios
USUARIOS_FILE = "data/usuarios.json" # Define una constante con la ruta al archivo JSON donde se almacenarán los datos de los usuarios.

def cargar_usuarios():
    """Carga los usuarios desde el archivo JSON.""" # Docstring que describe la función.
    if not os.path.exists(USUARIOS_FILE): # Comprueba si el archivo de usuarios no existe en la ruta especificada.
        return {} # Si el archivo no existe, devuelve un diccionario vacío, indicando que no hay usuarios registrados.
    with open(USUARIOS_FILE, 'r') as f: # Abre el archivo de usuarios en modo lectura ('r').
        return json.load(f) # Carga (deserializa) el contenido JSON del archivo y lo devuelve como un diccionario de Python.

def guardar_usuarios(usuarios):
    """Guarda los usuarios en el archivo JSON.""" # Docstring que describe la función.
    os.makedirs(os.path.dirname(USUARIOS_FILE), exist_ok=True) # Crea el directorio 'data' si no existe; 'exist_ok=True' evita un error si ya existe.
    with open(USUARIOS_FILE, 'w') as f: # Abre el archivo de usuarios en modo escritura ('w'). Si no existe, lo crea; si existe, sobrescribe su contenido.
        json.dump(usuarios, f, indent=4) # Guarda (serializa) el diccionario de usuarios en el archivo JSON, con una indentación de 4 espacios para legibilidad.

# --- Funciones auxiliares para el estilo (copiadas de notas.py/tareas.py para consistencia) ---
def _centrar_ventana(win, width, height):
    """Centra una ventana Toplevel o Tk en la pantalla.""" # Docstring que describe la función.
    win.update_idletasks() # Fuerza a Tkinter a procesar todos los eventos pendientes y actualizar la geometría de la ventana, asegurando que win.winfo_width() y win.winfo_height() devuelvan valores correctos.
    
    # Obtener las dimensiones de la pantalla
    screen_width = win.winfo_screenwidth() # Obtiene el ancho de la pantalla del usuario en píxeles.
    screen_height = win.winfo_screenheight() # Obtiene la altura de la pantalla del usuario en píxeles.

    # Calcular la posición para centrar
    x = (screen_width // 2) - (width // 2) # Calcula la coordenada X para que la ventana quede centrada horizontalmente.
    y = (screen_height // 2) - (height // 2) # Calcula la coordenada Y para que la ventana quede centrada verticalmente.

    win.geometry(f'{width}x{height}+{x}+{y}') # Establece el tamaño y la posición de la ventana usando el formato "Ancho x Alto + X + Y".
    # No deshabilitamos resizable para la ventana principal si es fullscreen
    # win.resizable(False, False) # Línea comentada: si estuviera activa, evitaría que la ventana se pueda redimensionar.

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


# Función para configurar la interfaz de usuario de login
def setup_login_ui(parent_root):
    """
    Configura y muestra la interfaz de usuario de inicio de sesión en la ventana principal.
    Esta función es llamada inicialmente y también cuando el usuario cierra sesión.
    """ # Docstring que describe la función.
    # Limpiar widgets existentes si los hay (importante al re-inicializar)
    for widget in parent_root.winfo_children(): # Itera sobre todos los widgets hijos de la ventana principal.
        widget.destroy() # Destruye cada widget hijo, limpiando la ventana.

    parent_root.title("EduPlanner - Inicio de Sesión") # Establece el título de la ventana principal.
    parent_root.attributes('-fullscreen', True) # Configura la ventana para que se abra en modo de pantalla completa.

    # Fondo de la ventana de login
    try: # Intenta ejecutar el bloque de código para cargar la imagen de fondo.
        fondo_img = Image.open("img/fondo_login.jpg") # Abre la imagen de fondo desde la ruta especificada.
        # Redimensionar la imagen para que se ajuste a la pantalla
        fondo_img = fondo_img.resize((parent_root.winfo_screenwidth(), parent_root.winfo_screenheight()), Image.Resampling.LANCZOS) # Redimensiona la imagen para que coincida con el tamaño de la pantalla, usando un algoritmo de remuestreo de alta calidad.
        fondo_photo = ImageTk.PhotoImage(fondo_img) # Convierte la imagen PIL a un formato compatible con Tkinter (PhotoImage).
        fondo_label = tk.Label(parent_root, image=fondo_photo) # Crea un Label para mostrar la imagen de fondo.
        fondo_label.image = fondo_photo # Mantiene una referencia a la imagen para evitar que sea eliminada por el recolector de basura de Python.
        fondo_label.place(x=0, y=0, relwidth=1, relheight=1) # Coloca el Label de fondo para que ocupe toda la ventana.
    except Exception as e: # Captura cualquier excepción que ocurra durante la carga de la imagen.
        print(f"Error al cargar la imagen de fondo del login: {e}") # Imprime el error en la consola.
        parent_root.configure(bg="#e0e0e0") # Si la imagen no carga, establece un color de fondo alternativo para la ventana.

    # Título "EduPlanner" (AHORA MÁS GRANDE)
    titulo = tk.Label(parent_root, text="EduPlanner", font=("Helvetica", 56, "bold"), fg="black", bg=parent_root["bg"]) # Crea un Label para el título principal, con una fuente grande y en negrita.
    titulo.place(relx=0.5, y=40, anchor="n") # Coloca el título centrado horizontalmente en la parte superior de la ventana.

    # --- NUEVO: Frame principal del login con estilo de tarjeta ---
    login_card_width = 500 # Define el ancho de la "tarjeta" de login.
    login_card_height = 450 # Define la altura de la "tarjeta" de login.
    login_card_frame = tk.Frame(parent_root, bg="#F8F8F8", bd=0, relief="flat", # Crea un Frame para contener los elementos del login, con un fondo claro y sin relieve.
                                highlightbackground="#d9d9d9", highlightthickness=2) # Añade un borde sutil a la "tarjeta" de login.
    login_card_frame.place(relx=0.5, rely=0.5, anchor="center", width=login_card_width, height=login_card_height) # Coloca la "tarjeta" de login centrada en la ventana, con el tamaño definido.

    # Encabezado para la tarjeta de login
    login_header_frame = tk.Frame(login_card_frame, bg="#E0E0E0", padx=15, pady=10) # Crea un Frame para el encabezado de la tarjeta de login, con un fondo gris claro.
    login_header_frame.pack(fill="x", pady=(0, 15)) # Empaqueta el encabezado para que se expanda horizontalmente y añada padding inferior.
    tk.Label(login_header_frame, text="🔑 Iniciar Sesión", font=("Helvetica", 16, "bold"), fg="#333333", bg="#E0E0E0").pack(anchor="w") # Crea un Label para el texto del encabezado del login, con un ícono y estilo.

    # Frame para el contenido interno (campos y botones)
    login_content_frame = tk.Frame(login_card_frame, bg="#F8F8F8", padx=20, pady=10) # Crea un Frame para los campos de entrada y botones, con un fondo claro y padding interno.
    login_content_frame.pack(expand=True, fill="both") # Empaqueta el Frame para que se expanda y rellene el espacio restante dentro de la tarjeta.

    # Función auxiliar para crear etiquetas y campos de entrada con estilo
    def crear_entry_con_etiqueta(parent_frame, texto): # Define una función para crear un par de Label y Entry.
        label = tk.Label(parent_frame, text=texto, font=("Helvetica", 12, "bold"), bg=parent_frame["bg"], fg="#555555") # Crea un Label para la etiqueta del campo.
        label.pack(anchor="w", pady=(5, 2)) # Empaqueta la etiqueta alineada a la izquierda con padding.
        entry = tk.Entry(parent_frame, font=("Helvetica", 12), bd=1, relief="solid", justify="center", # Crea un campo de entrada (Entry) con estilo de borde y fuente.
                         highlightthickness=1, highlightbackground="#CCCCCC", highlightcolor="#3498DB", width=40) # Añade un borde de resaltado y un ancho fijo.
        entry.pack(pady=(0, 15), ipadx=5, ipady=5, fill="x", padx=5) # Empaqueta el campo de entrada, con padding, relleno horizontal y padding interno.
        return entry # Devuelve el widget Entry creado.

    # Variables globales para los campos de entrada (necesarias para las funciones iniciar_sesion y registrar_usuario)
    global usuario_entry, contrasena_entry # Declara estas variables como globales para que puedan ser accedidas y modificadas por las funciones iniciar_sesion y registrar_usuario.
    usuario_entry = crear_entry_con_etiqueta(login_content_frame, "Usuario") # Crea el campo de entrada para el nombre de usuario.
    contrasena_entry = crear_entry_con_etiqueta(login_content_frame, "Contraseña") # Crea el campo de entrada para la contraseña.
    contrasena_entry.config(show="*") # Configura el campo de contraseña para que muestre asteriscos en lugar de los caracteres ingresados.

    # Botones personalizados (usando la nueva función de estilo)
    _crear_boton_estilizado(login_content_frame, "Iniciar Sesión", lambda: iniciar_sesion(parent_root), "#3498DB", "white", icon_char="➡️") # Crea el botón "Iniciar Sesión" con estilo y su comando asociado.
    _crear_boton_estilizado(login_content_frame, "Registrar Usuario", registrar_usuario, "#2ECC71", "white", icon_char="➕") # Crea el botón "Registrar Usuario" con estilo y su comando asociado.

    # Botón Salir (en la esquina superior izquierda de la ventana principal)
    tk.Button( # Crea el botón "Salir".
        parent_root, # Se coloca directamente en la ventana principal.
        text="Salir", # Texto del botón.
        font=("Helvetica", 10), # Fuente del texto.
        command=parent_root.destroy, # Comando que se ejecuta al hacer clic: cierra la ventana principal y termina la aplicación.
        bg="#E74C3C", # Color de fondo del botón (rojo).
        fg="white", # Color del texto del botón.
        activebackground="#C0392B", # Color de fondo cuando el botón está activo (presionado).
        relief="flat" # Estilo de relieve plano.
    ).place(x=10, y=10) # Coloca el botón en la esquina superior izquierda con un pequeño margen.

# Función para iniciar sesión
def iniciar_sesion(current_root):
    """Maneja la lógica de inicio de sesión.""" # Docstring que describe la función.
    usuario = usuario_entry.get().strip() # Obtiene el texto del campo de usuario y elimina espacios en blanco al inicio/final.
    contrasena = contrasena_entry.get().strip() # Obtiene el texto del campo de contraseña y elimina espacios en blanco.
    usuarios = cargar_usuarios() # Carga la lista de usuarios registrados desde el archivo.

    if usuario in usuarios and usuarios[usuario] == contrasena: # Comprueba si el usuario existe y la contraseña coincide.
        messagebox.showinfo("Éxito", "Inicio de sesión correcto") # Muestra un mensaje de éxito.
        current_root.destroy() # Destruye la ventana de login actual.
        # Inicia el menú principal, pasando el usuario y la función para volver al login
        MenuPrincipal(usuario) # Crea una instancia de MenuPrincipal, pasando el nombre de usuario.
    else: # Si el usuario o la contraseña son incorrectos.
        messagebox.showerror("Error", "Usuario o contraseña incorrectos") # Muestra un mensaje de error.

# Función para registrar un nuevo usuario
def registrar_usuario():
    """Maneja la lógica de registro de un nuevo usuario.""" # Docstring que describe la función.
    usuario = usuario_entry.get().strip() # Obtiene el texto del campo de usuario y elimina espacios en blanco.
    contrasena = contrasena_entry.get().strip() # Obtiene el texto del campo de contraseña y elimina espacios en blanco.

    if not usuario or not contrasena: # Comprueba si alguno de los campos está vacío.
        messagebox.showwarning("Advertencia", "Rellena todos los campos") # Muestra una advertencia.
        return # Sale de la función.

    usuarios = cargar_usuarios() # Carga la lista de usuarios registrados.
    if usuario in usuarios: # Comprueba si el usuario ya existe.
        messagebox.showwarning("Advertencia", "El usuario ya existe") # Muestra una advertencia.
    else: # Si el usuario no existe.
        usuarios[usuario] = contrasena # Añade el nuevo usuario y su contraseña al diccionario de usuarios.
        guardar_usuarios(usuarios) # Guarda la lista actualizada de usuarios en el archivo.
        messagebox.showinfo("Éxito", "Usuario registrado correctamente") # Muestra un mensaje de éxito.
        # Opcional: Limpiar campos después del registro exitoso
        usuario_entry.delete(0, tk.END) # Borra el contenido del campo de usuario.
        contrasena_entry.delete(0, tk.END) # Borra el contenido del campo de contraseña.

# --- Bloque de ejecución principal ---
if __name__ == "__main__": # Este bloque se ejecuta solo cuando el script se corre directamente (no cuando se importa como módulo).
    # Crea la ventana raíz principal de Tkinter
    root = tk.Tk() # Crea la ventana principal (raíz) de la aplicación Tkinter.
    # Configura la interfaz de usuario de login en esta ventana raíz
    setup_login_ui(root) # Llama a la función para configurar y mostrar la interfaz de usuario de login en la ventana raíz.
    # Inicia el bucle principal de eventos de Tkinter
    root.mainloop() # Inicia el bucle de eventos de Tkinter. Este método mantiene la ventana abierta y esperando interacciones del usuario.
