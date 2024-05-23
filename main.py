import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from modulo1 import ejecutar_modulo1
from modulo2 import ejecutar_modulo2
from modulo3 import ejecutar_modulo3
from modulo4 import ejecutar_modulo4
from modulo5 import ejecutar_modulo5
from modulo6 import ejecutar_modulo6

def mostrar_menu_principal(current_frame=None):
    if current_frame:
        current_frame.destroy()

    # Cargar imágenes para los botones y ajustar el tamaño
    img_modulo1 = ImageTk.PhotoImage(Image.open(r"OP.png").resize((230, 230), Image.LANCZOS))
    img_modulo2 = ImageTk.PhotoImage(Image.open(r"Inversa.png").resize((230, 230), Image.LANCZOS))
    img_modulo3 = ImageTk.PhotoImage(Image.open(r"DET.png").resize((230, 230), Image.LANCZOS))
    img_modulo4 = ImageTk.PhotoImage(Image.open(r"RG.png").resize((230, 230), Image.LANCZOS))
    img_modulo5 = ImageTk.PhotoImage(Image.open(r"Cifrado.png").resize((230, 230), Image.LANCZOS))
    img_modulo6 = ImageTk.PhotoImage(Image.open(r"Cadenas.png").resize((230, 230), Image.LANCZOS))
    img_modulo7 = ImageTk.PhotoImage(Image.open(r"Vectores.png").resize((230, 230), Image.LANCZOS))

    # Crear botones para cada módulo sobre el fondo
    btn_modulo1 = ttk.Button(root, text="Operaciones Matrices", command=lambda: mostrar_modulo(ejecutar_modulo1), image=img_modulo1, compound="top", style='TButton')
    btn_modulo1.grid(row=0, column=0, padx=10, pady=10)

    btn_modulo2 = ttk.Button(root, text="Inversa Matriz", command=lambda: mostrar_modulo(ejecutar_modulo2), image=img_modulo2, compound="top", style='TButton')
    btn_modulo2.grid(row=0, column=1, padx=10, pady=10)

    btn_modulo3 = ttk.Button(root, text="Determinante Matriz", command=lambda: mostrar_modulo(ejecutar_modulo3), image=img_modulo3, compound="top", style='TButton')
    btn_modulo3.grid(row=0, column=2, padx=10, pady=10)

    btn_modulo4 = ttk.Button(root, text="Rango Matriz", command=lambda: mostrar_modulo(ejecutar_modulo4), image=img_modulo4, compound="top", style='TButton')
    btn_modulo4.grid(row=1, column=0, padx=10, pady=10)

    btn_modulo5 = ttk.Button(root, text="Cifrar - Descrifar", command=lambda: mostrar_modulo(ejecutar_modulo5), image=img_modulo5, compound="top", style='TButton')
    btn_modulo5.grid(row=1, column=1, padx=10, pady=10)

    btn_modulo6 = ttk.Button(root, text="Cadenas Markov", command=lambda: mostrar_modulo(ejecutar_modulo6), image=img_modulo6, compound="top", style='TButton')
    btn_modulo6.grid(row=1, column=2, padx=10, pady=10)

    btn_modulo7 = ttk.Button(root, text="Operaciones Vectores", command=lambda: mostrar_modulo(ejecutar_modulo7), image=img_modulo7, compound="top", style='TButton')
    btn_modulo7.grid(row=2, column=0, columnspan=3, padx=10, pady=10)  # Usamos columnspan para que el botón abarque todas las columnas

    # Mantener referencias a las imágenes
    btn_modulo1.image = img_modulo1
    btn_modulo2.image = img_modulo2
    btn_modulo3.image = img_modulo3
    btn_modulo4.image = img_modulo4
    btn_modulo5.image = img_modulo5
    btn_modulo6.image = img_modulo6
    btn_modulo7.image = img_modulo7

def mostrar_modulo(funcion_modulo):
    for widget in root.winfo_children():
        widget.destroy()
    mostrar_fondo()
    funcion_modulo(root, mostrar_menu_principal)

def mostrar_fondo():
    # Cargar la imagen de fondo
    image_path = r"fondito.png"  # Reemplaza esto con la ruta de tu imagen
    image = Image.open(image_path)
    image = image.resize((1500, 1500), Image.LANCZOS)  # Redimensionar la imagen al tamaño de la ventana
    background_image = ImageTk.PhotoImage(image)

    # Configurar la etiqueta de fondo
    background_label = tk.Label(root, image=background_image)
    background_label.image = background_image  # Necesario para evitar que la imagen sea recolectada por el recolector de basura
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

def crear_interfaz_principal():
    global root
    root = tk.Tk()
    root.title("Proyecto Algebra Lineal")

    # Tamaño de la ventana
    root.geometry("820x850")

    # Crear estilo de botón para eliminar el color al pasar por encima
    style = ttk.Style()
    style.map('TButton', foreground=[('active', '!disabled', 'black')], background=[('active', '!disabled', 'white')])

    mostrar_fondo()
    mostrar_menu_principal()

    root.mainloop()

crear_interfaz_principal()
