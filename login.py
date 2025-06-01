import tkinter as tk # Importa el módulo tkinter, que es la biblioteca estándar de Python para crear interfaces gráficas de usuario (GUI).
from tkinter import messagebox # Importa el submódulo messagebox de tkinter, utilizado para mostrar cuadros de diálogo de mensajes (información, advertencia, error).
import json # Importa el módulo json, que permite trabajar con datos en formato JSON (serializar y deserializar).
import os # Importa el módulo os, que proporciona funciones para interactuar con el sistema operativo, como la gestión de rutas de archivos y directorios.
from menu import MenuPrincipal # Importa la clase MenuPrincipal desde el archivo 'menu.py', que representa la ventana principal del menú de la aplicación.

USUARIOS_FILE = "data/usuarios.json" # Define una constante con la ruta al archivo JSON donde se almacenarán los datos de los usuarios.

class LoginVentana: # Define la clase LoginVentana, que encapsula la lógica y la interfaz de usuario para el inicio de sesión y registro.
    def __init__(self, root): # Define el método constructor de la clase, que se ejecuta al crear una nueva instancia de LoginVentana.
        self.root = root # Almacena la ventana raíz de Tkinter (pasada como argumento) en una variable de instancia.
        self.root.title("Login") # Establece el título de la ventana de login.
        self.root.geometry("300x200") # Establece el tamaño inicial de la ventana de login a 300 píxeles de ancho por 200 de alto.

        tk.Label(root, text="Usuario:").pack(pady=5) # Crea una etiqueta de texto "Usuario:" y la empaqueta en la ventana, con un padding vertical.
        self.usuario_entry = tk.Entry(root) # Crea un campo de entrada de texto para el nombre de usuario y lo almacena en una variable de instancia.
        self.usuario_entry.pack() # Empaqueta el campo de entrada de usuario en la ventana.

        tk.Label(root, text="Contraseña:").pack(pady=5) # Crea una etiqueta de texto "Contraseña:" y la empaqueta en la ventana, con un padding vertical.
        self.password_entry = tk.Entry(root, show="*") # Crea un campo de entrada de texto para la contraseña, mostrando asteriscos para ocultar los caracteres.
        self.password_entry.pack() # Empaqueta el campo de entrada de contraseña en la ventana.

        tk.Button(root, text="Iniciar sesión", command=self.iniciar_sesion).pack(pady=5) # Crea un botón "Iniciar sesión" y lo empaqueta, vinculándolo al método iniciar_sesion.
        tk.Button(root, text="Registrarse", command=self.registrarse).pack() # Crea un botón "Registrarse" y lo empaqueta, vinculándolo al método registrarse.

    def cargar_usuarios(self): # Define un método para cargar los usuarios desde el archivo JSON.
        if not os.path.exists(USUARIOS_FILE): # Comprueba si el archivo de usuarios no existe.
            return {} # Si no existe, devuelve un diccionario vacío.
        with open(USUARIOS_FILE, 'r') as f: # Abre el archivo de usuarios en modo lectura.
            return json.load(f) # Carga y devuelve el contenido JSON del archivo.

    def guardar_usuario(self, usuario, contraseña): # Define un método para guardar un nuevo usuario o actualizar uno existente.
        usuarios = self.cargar_usuarios() # Carga la lista actual de usuarios.
        usuarios[usuario] = contraseña # Añade o actualiza la contraseña del usuario en el diccionario.
        with open(USUARIOS_FILE, 'w') as f: # Abre el archivo de usuarios en modo escritura (sobrescribe).
            json.dump(usuarios, f) # Guarda el diccionario actualizado de usuarios en el archivo JSON.

    def iniciar_sesion(self): # Define el método que maneja la lógica de inicio de sesión.
        usuario = self.usuario_entry.get() # Obtiene el texto ingresado en el campo de usuario.
        contraseña = self.password_entry.get() # Obtiene el texto ingresado en el campo de contraseña.
        usuarios = self.cargar_usuarios() # Carga la lista de usuarios.
        if usuario in usuarios and usuarios[usuario] == contraseña: # Comprueba si el usuario existe y la contraseña coincide.
            messagebox.showinfo("Éxito", "Inicio de sesión exitoso") # Muestra un mensaje de éxito.
            self.root.destroy() # Destruye la ventana de login actual.
            MenuPrincipal(usuario) # Crea una instancia de MenuPrincipal, pasando el nombre de usuario, y muestra la ventana del menú.
        else: # Si las credenciales son incorrectas.
            messagebox.showerror("Error", "Usuario o contraseña incorrectos") # Muestra un mensaje de error.

    def registrarse(self): # Define el método que maneja la lógica de registro de un nuevo usuario.
        usuario = self.usuario_entry.get() # Obtiene el texto ingresado en el campo de usuario.
        contraseña = self.password_entry.get() # Obtiene el texto ingresado en el campo de contraseña.
        usuarios = self.cargar_usuarios() # Carga la lista de usuarios.
        if usuario in usuarios: # Comprueba si el usuario ya existe.
            messagebox.showwarning("Advertencia", "El usuario ya existe") # Muestra una advertencia.
        else: # Si el usuario no existe.
            self.guardar_usuario(usuario, contraseña) # Guarda el nuevo usuario y su contraseña.
            messagebox.showinfo("Éxito", "Usuario registrado con éxito") # Muestra un mensaje de éxito.
