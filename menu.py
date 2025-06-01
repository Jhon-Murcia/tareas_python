import tkinter as tk # Importa el módulo tkinter, que es la biblioteca estándar de Python para crear interfaces gráficas de usuario (GUI).
from tkinter import PhotoImage # Importa la clase PhotoImage de tkinter, utilizada para trabajar con imágenes en formatos como GIF, PNG.
from PIL import Image, ImageTk # Importa las clases Image y ImageTk del módulo PIL (Pillow), necesarias para trabajar con imágenes (abrir, redimensionar, convertir a formato compatible con Tkinter).
# Asegúrate de que estas rutas sean correctas y que los módulos existan
from notas import crear_nueva_nota, mostrar_notas # Importa las funciones crear_nueva_nota y mostrar_notas desde el módulo 'notas.py'.
from tareas import agregar_tarea, ver_tareas # Importa las funciones agregar_tarea y ver_tareas desde el módulo 'tareas.py'.
from calendario import mostrar_calendario # Importa la función mostrar_calendario desde el módulo 'calendario.py'.

class MenuPrincipal: # Define la clase MenuPrincipal, que representa la ventana principal del menú de la aplicación después del login.
    def __init__(self, usuario): # Define el método constructor de la clase, que se ejecuta al crear una nueva instancia de MenuPrincipal.
        """
        Inicializa la ventana principal del menú.
        
        Args:
            usuario (str): El nombre del usuario logueado.
        """ # Docstring que describe la función y sus argumentos.
        self.usuario = usuario # Almacena el nombre de usuario (pasado como argumento) en una variable de instancia.
        self.root = tk.Tk() # Crea la ventana principal (raíz) de la aplicación Tkinter para el menú.
        self.root.title("Administrador de Tareas") # Establece el título de la ventana del menú.
        self.root.attributes('-fullscreen', True) # Configura la ventana para que se abra en modo de pantalla completa.

        # Fondo de la ventana del menú
        try: # Intenta ejecutar el bloque de código para cargar la imagen de fondo.
            fondo_img = Image.open("img/fondo_menu.jpg") # Abre la imagen de fondo desde la ruta especificada.
            # Redimensionar la imagen para que se ajuste a la pantalla
            fondo_img = fondo_img.resize((self.root.winfo_screenwidth(), self.root.winfo_screenheight()), Image.Resampling.LANCZOS) # Redimensiona la imagen para que coincida con el tamaño de la pantalla, usando un algoritmo de remuestreo de alta calidad.
            fondo_photo = ImageTk.PhotoImage(fondo_img) # Convierte la imagen PIL a un formato compatible con Tkinter (PhotoImage).
            fondo_label = tk.Label(self.root, image=fondo_photo) # Crea un Label para mostrar la imagen de fondo.
            fondo_label.image = fondo_photo # Mantiene una referencia a la imagen para evitar que sea eliminada por el recolector de basura de Python.
            fondo_label.place(x=0, y=0, relwidth=1, relheight=1) # Coloca el Label de fondo para que ocupe toda la ventana.
        except Exception as e: # Captura cualquier excepción que ocurra durante la carga de la imagen.
            print(f"Error al cargar la imagen de fondo del menú: {e}") # Imprime el error en la consola.
            self.root.configure(bg="#f0f4f7") # Si la imagen no carga, establece un color de fondo alternativo para la ventana.

        # Título superior "Bienvenido, [Usuario]" (AHORA MUCHO MÁS GRANDE)
        titulo = tk.Label(self.root, text=f"Bienvenido, {usuario}", font=("Helvetica", 56, "bold"), fg="black", bg="white") # Crea un Label para el título de bienvenida, con una fuente grande y en negrita.
        titulo.pack(pady=50) # Empaqueta el título en la ventana, añadiendo un padding vertical para más espacio.

        # Contenedor con fondo blanco para las tarjetas de opciones
        contenedor = tk.Frame(self.root, bg="white", padx=20, pady=20) # Crea un Frame que servirá como contenedor principal para las tarjetas de opciones, con fondo blanco y padding interno.
        contenedor.place(relx=0.5, rely=0.45, anchor="center") # Coloca el contenedor centrado en la pantalla (50% del ancho, 45% del alto).

        # Frame para las tarjetas dentro del contenedor (para organizar horizontalmente)
        frame_botones = tk.Frame(contenedor, bg="white") # Crea un Frame dentro del contenedor para organizar los botones/tarjetas horizontalmente.
        frame_botones.pack() # Empaqueta este Frame de botones.

        # Opciones del menú
        opciones = [ # Define una lista de diccionarios, donde cada diccionario representa una opción del menú.
            {"texto": "Nueva nota", "icono": "img/icono_nota.jpg", "accion": self.nueva_nota}, # Opción para crear una nueva nota, con su texto, ruta de icono y la función a ejecutar.
            {"texto": "Ver notas", "icono": "img/icono_ver_notas.png", "accion": self.ver_notas}, # Opción para ver notas existentes.
            {"texto": "Agregar tarea", "icono": "img/icono_tarea.png", "accion": self.nueva_tarea}, # Opción para agregar una nueva tarea.
            {"texto": "Ver tareas", "icono": "img/icono_ver_tareas.png", "accion": self.ver_tareas}, # Opción para ver tareas existentes.
            {"texto": "Calendario", "icono": "img/calendario.png", "accion": self.abrir_calendario} # Opción para abrir el calendario.
        ]

        # Crear cada tarjeta de opción
        for opcion in opciones: # Itera sobre cada diccionario en la lista de opciones.
            self.crear_tarjeta_opcion(frame_botones, opcion["texto"], opcion["icono"], opcion["accion"]) # Llama a la función crear_tarjeta_opcion para crear la interfaz visual de cada opción.

        # Botón Salir (Esquina superior izquierda)
        tk.Button( # Crea el botón "Salir".
            self.root, # Se coloca directamente en la ventana principal del menú.
            text="Salir", # Texto del botón.
            font=("Helvetica", 10), # Fuente del texto.
            command=self.root.quit, # Comando que se ejecuta al hacer clic: cierra la aplicación por completo.
            bg="#E74C3C", # Color de fondo del botón (rojo).
            fg="white", # Color del texto del botón.
            activebackground="#C0392B", # Color de fondo cuando el botón está activo (presionado).
            relief="flat" # Estilo de relieve plano.
        ).place(x=10, y=10) # Coloca el botón en la esquina superior izquierda con un pequeño margen.

        self.root.mainloop() # Inicia el bucle principal de eventos de Tkinter para esta ventana. Este método mantiene la ventana abierta y esperando interacciones del usuario.

    def crear_tarjeta_opcion(self, parent, texto, icono_path, comando):
        """
        Crea una tarjeta visual para cada opción del menú con un borde.
        """ # Docstring que describe la función.
        card = tk.Frame( # Crea un Frame que servirá como la "tarjeta" individual para cada opción.
            parent, # El Frame se coloca dentro del 'parent' (frame_botones).
            bg="white", # Color de fondo de la tarjeta.
            width=150, # Ancho fijo de la tarjeta.
            height=170, # Altura fija de la tarjeta.
            highlightbackground="#d9d9d9",  # Color del borde gris claro (usando highlight para simular un borde).
            highlightthickness=2,          # Grosor del borde.
            bd=0                           # Asegura que no haya un borde 3D por defecto.
        )
        card.pack(side="left", padx=10, pady=10) # Empaqueta la tarjeta para que se coloque a la izquierda de la anterior, con padding horizontal y vertical.
        card.pack_propagate(False) # Evita que el Frame de la tarjeta se encoja o expanda automáticamente para ajustarse a su contenido, manteniendo su tamaño fijo.

        # Intenta cargar el icono, si falla, usa un emoji como fallback
        try: # Intenta cargar la imagen del icono.
            icono_img = Image.open(icono_path) # Abre la imagen del icono desde la ruta especificada.
            icono_img = icono_img.resize((60, 60), Image.Resampling.LANCZOS) # Redimensiona la imagen del icono a 60x60 píxeles.
            icono = ImageTk.PhotoImage(icono_img) # Convierte la imagen PIL a un formato compatible con Tkinter.
            lbl_icono = tk.Label(card, image=icono, bg="white") # Crea un Label para mostrar el icono dentro de la tarjeta.
            lbl_icono.image = icono # Mantiene una referencia a la imagen del icono.
            lbl_icono.pack(pady=(15, 10)) # Empaqueta el Label del icono con padding vertical.
        except Exception as e: # Captura cualquier excepción si la imagen del icono no se puede cargar.
            print(f"Error al cargar icono {icono_path}: {e}") # Imprime el error en la consola.
            lbl_icono = tk.Label(card, text="📄", font=("Helvetica", 28), bg="white") # Si falla, usa un emoji de documento como icono de fallback.
            lbl_icono.pack(pady=(15, 10)) # Empaqueta el Label del emoji.

        # Etiqueta de texto para la opción
        tk.Label(card, text=texto, font=("Helvetica", 12, "bold"), bg="white", fg="#333").pack() # Crea un Label para el texto de la opción y lo empaqueta.

        # Asocia el comando a toda la tarjeta y a sus widgets internos para una mejor área de clic
        for widget in [card, lbl_icono] + list(card.winfo_children()): # Itera sobre la tarjeta misma, el Label del icono y todos los demás widgets hijos de la tarjeta.
            widget.bind("<Button-1>", lambda e: comando()) # Vincula el evento de clic izquierdo del ratón a cada uno de estos widgets para ejecutar el comando asociado a la opción.

    # Métodos para las acciones del menú (se mantienen igual)
    def nueva_nota(self): # Define el método que se ejecuta al seleccionar "Nueva nota".
        crear_nueva_nota(self.usuario) # Llama a la función crear_nueva_nota del módulo 'notas.py', pasándole el usuario actual.

    def ver_notas(self): # Define el método que se ejecuta al seleccionar "Ver notas".
        mostrar_notas(self.usuario) # Llama a la función mostrar_notas del módulo 'notas.py', pasándole el usuario actual.

    def nueva_tarea(self): # Define el método que se ejecuta al seleccionar "Agregar tarea".
        agregar_tarea(self.usuario) # Llama a la función agregar_tarea del módulo 'tareas.py', pasándole el usuario actual.

    def ver_tareas(self): # Define el método que se ejecuta al seleccionar "Ver tareas".
        ver_tareas(self.usuario) # Llama a la función ver_tareas del módulo 'tareas.py', pasándole el usuario actual.

    def abrir_calendario(self): # Define el método que se ejecuta al seleccionar "Calendario".
        mostrar_calendario(self.usuario) # Llama a la función mostrar_calendario del módulo 'calendario.py', pasándole el usuario actual.
