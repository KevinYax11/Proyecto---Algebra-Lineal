import tkinter as tk
import math
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
from numpy import arctan

# Definir variables globales
entry_magnitudes = []
entry_angulos = []
entry_orientaciones = []
label_resultante = None
text_pasos = None

def calcular_componentes(magnitud, angulo, orientacion):
    angulo_rad = math.radians(angulo)
    if orientacion == "N":
        vx = magnitud * math.cos(angulo_rad)
        vy = magnitud * math.sin(angulo_rad)
    elif orientacion == "S":
        vx = -magnitud * math.cos(angulo_rad)
        vy = -magnitud * math.sin(angulo_rad)
    elif orientacion == "E":
        vx = magnitud * math.sin(angulo_rad)
        vy = magnitud * math.cos(angulo_rad)
    elif orientacion == "O":
        vx = -magnitud * math.sin(angulo_rad)
        vy = -magnitud * math.cos(angulo_rad)
    elif orientacion == "NE":
        vx = magnitud * math.cos(angulo_rad)
        vy = magnitud * math.sin(angulo_rad)
    elif orientacion == "NO":
        vx = -magnitud * math.cos(angulo_rad)
        vy = magnitud * math.sin(angulo_rad)
    elif orientacion == "SE":
        vx = magnitud * math.cos(angulo_rad)
        vy = -magnitud * math.sin(angulo_rad)
    elif orientacion == "SO":
        vx = -magnitud * math.cos(angulo_rad)
        vy = -magnitud * math.sin(angulo_rad)
    else:
        raise ValueError("Orientación no válida. Use 'N', 'S', 'E', 'O', 'NE', 'NO', 'SE' o 'SO'.")
    return vx, vy

def sumar_vectores(vx_list, vy_list):
    vx_sum = sum(vx_list)
    vy_sum = sum(vy_list)
    return vx_sum, vy_sum

def calcular_magnitud_angulo(vx_sum, vy_sum):
    magnitud = math.sqrt(vx_sum ** 2 + vy_sum ** 2)
    angulo = math.degrees(math.atan2(vy_sum, vx_sum))
    return magnitud, angulo

def crear_entradas():
    global entry_magnitudes, entry_angulos, entry_orientaciones, label_resultante, text_pasos

    num_vectores = int(entry_num_vectores.get())

    for widget in root.winfo_children():
        if widget.winfo_class() == 'Entry' and widget != entry_num_vectores:
            widget.destroy()
        elif widget.winfo_class() == 'OptionMenu':
            widget.destroy()
        elif isinstance(widget, tk.Text):
            widget.delete("1.0", tk.END)

    entry_magnitudes.clear()
    entry_angulos.clear()
    entry_orientaciones.clear()

    row = 2
    for i in range(num_vectores):
        label_magnitud = tk.Label(root, text=f"Magnitud del vector {chr(65 + i)}:")
        label_magnitud.grid(row=row, column=0, padx=5, pady=5, sticky="w")
        entry_mag = tk.Entry(root)
        entry_mag.grid(row=row, column=1, padx=5, pady=5)
        entry_magnitudes.append(entry_mag)

        label_angulo = tk.Label(root, text=f"Ángulo del vector {chr(65 + i)}:")
        label_angulo.grid(row=row, column=2, padx=5, pady=5, sticky="w")
        entry_ang = tk.Entry(root)
        entry_ang.grid(row=row, column=3, padx=5, pady=5)
        entry_angulos.append(entry_ang)

        label_orientacion = tk.Label(root, text=f"Orientación del vector {chr(65 + i)}:")
        label_orientacion.grid(row=row, column=4, padx=5, pady=5, sticky="w")
        entry_or = tk.Entry(root)
        entry_or.grid(row=row, column=5, padx=5, pady=5)
        entry_orientaciones.append(entry_or)

        row += 1

    button_calcular = tk.Button(root, text="Calcular", command=calcular)
    button_calcular.grid(row=row, column=2, columnspan=2, padx=5, pady=5)

def calcular():
    global label_resultante, text_pasos

    magnitudes = []
    angulos = []
    orientaciones = []

    for entry_mag, entry_ang, entry_or in zip(entry_magnitudes, entry_angulos, entry_orientaciones):
        magnitud = float(entry_mag.get())
        angulo = float(entry_ang.get())
        orientacion = entry_or.get().strip().upper()
        magnitudes.append(magnitud)
        angulos.append(angulo)
        orientaciones.append(orientacion)

    # Calcular componentes de cada vector según la fórmula
    comp_x_list = []
    comp_y_list = []
    for magnitud, angulo, orientacion in zip(magnitudes, angulos, orientaciones):
        comp_x, comp_y = calcular_componentes(magnitud, angulo, orientacion)
        comp_x_list.append(comp_x)
        comp_y_list.append(comp_y)

    # Calcular el componente resultante restando los componentes de los vectores individuales
    comp_x_resultante = comp_x_list[0] - comp_x_list[1]
    comp_y_resultante = comp_y_list[0] - comp_y_list[1]

    # Calcular magnitud y ángulo de la componente resultante
    magnitud_resultante = ((comp_x_resultante)**2 + (comp_y_resultante)**2)**(1/2)
    angulo_resultante = arctan(comp_x_resultante / comp_y_resultante)
    # Actualizar el cuadro de texto con los pasos y el resultado
    text_pasos.delete("1.0", tk.END)
    text_pasos.insert(tk.END, "Pasos:\n\n")
    text_pasos.insert(tk.END, "Vector A:\n")
    text_pasos.insert(tk.END, f"Componente X: {comp_x_list[0]:.2f}\n")
    text_pasos.insert(tk.END, f"Componente Y: {comp_y_list[0]:.2f}\n")
    text_pasos.insert(tk.END, f"Magnitud: {magnitudes[0]:.2f}\n")
    text_pasos.insert(tk.END, f"Ángulo: {angulos[0]:.2f}\n")
    text_pasos.insert(tk.END, f"Orientación: {orientaciones[0]}\n\n")
    text_pasos.insert(tk.END, "Vector B:\n")
    text_pasos.insert(tk.END, f"Componente X: {comp_x_list[1]:.2f}\n")
    text_pasos.insert(tk.END, f"Componente Y: {comp_y_list[1]:.2f}\n")
    text_pasos.insert(tk.END, f"Magnitud: {magnitudes[1]:.2f}\n")
    text_pasos.insert(tk.END, f"Ángulo: {angulos[1]:.2f}\n")
    text_pasos.insert(tk.END, f"Orientación: {orientaciones[1]}\n\n")
    text_pasos.insert(tk.END, "Vector resultante:\n")
    text_pasos.insert(tk.END, f"Componente X: {comp_x_resultante:.2f}\n")
    text_pasos.insert(tk.END, f"Componente Y: {comp_y_resultante:.2f}\n")
    text_pasos.insert(tk.END, f"Magnitud: {magnitud_resultante:.2f}\n")
    text_pasos.insert(tk.END, f"Ángulo: {angulo_resultante:.2f} grados\n")

    # Graficar los vectores
    fig, ax = plt.subplots()
    ax.quiver(0, 0, comp_x_list[0], comp_y_list[0], angles='xy', scale_units='xy', scale=1, label="Vector A")
    ax.quiver(0, 0, comp_x_list[1], comp_y_list[1], angles='xy', scale_units='xy', scale=1, label="Vector B")
    ax.quiver(0, 0, comp_x_resultante, comp_y_resultante, angles='xy', scale_units='xy', scale=1, color='r', label="Resultante")
    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title('Gráfica de vectores')
    ax.legend()
    ax.grid()

    # Mostrar la gráfica en la interfaz
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().grid(row=11, column=0, columnspan=6)

    # Barra de herramientas de la gráfica
    toolbar = NavigationToolbar2Tk(canvas, root)
    toolbar.update()
    canvas.get_tk_widget().grid(row=12, column=0, columnspan=6)

# Crear la ventana principal
root = tk.Tk()
root.title("Suma de vectores con orientación")

# Etiqueta para el número de vectores
label_num_vectores = tk.Label(root, text="Número de vectores:")
label_num_vectores.grid(row=0, column=0, padx=5, pady=5, sticky="w")
entry_num_vectores = tk.Entry(root)
entry_num_vectores.grid(row=0, column=1, padx=5, pady=5, sticky="w")

# Botón para crear las entradas
button_crear_entradas = tk.Button(root, text="Crear entradas", command=crear_entradas)
button_crear_entradas.grid(row=0, column=2, padx=5, pady=5, sticky="w")

# Crear el cuadro de texto para mostrar los pasos
text_pasos = tk.Text(root, height=10, width=50)
text_pasos.grid(row=9, column=0, columnspan=6, padx=5, pady=5)

# Crear la etiqueta para mostrar el resultado
label_resultante = tk.Label(root, text="Resultado de la suma:")
label_resultante.grid(row=10, column=0, columnspan=6, padx=5, pady=5, sticky="w")

# Iniciar el bucle principal de la interfaz gráfica
root.mainloop()
