import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import numpy as np

# Función para crear las entradas de la matriz
def crear_entradas_matriz(frame, filas, columnas):
    # Limpiar el frame antes de crear nuevas entradas
    for widget in frame.winfo_children():
        widget.destroy()

    # Crear etiquetas y entradas para la matriz A
    ttk.Label(frame, text="Matriz A:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
    global entradas_matriz_a
    entradas_matriz_a = []
    for i in range(filas):
        fila = []
        for j in range(columnas):
            entrada = ttk.Entry(frame, width=5)
            entrada.grid(row=i + 2, column=j, padx=5, pady=5)
            fila.append(entrada)
        entradas_matriz_a.append(fila)

    # Operaciones y botón calcular
    ttk.Label(frame, text="Operación:").grid(row=filas + 2, column=0, padx=5, pady=5, sticky=tk.W)
    global operaciones
    operaciones = tk.StringVar()
    combo_operaciones = ttk.Combobox(frame, textvariable=operaciones, values=["Calcular Determinante"])
    combo_operaciones.grid(row=filas + 2, column=1, columnspan=2, padx=5, pady=5, sticky=tk.W + tk.E)

    ttk.Button(frame, text="Calcular", command=lambda: calcular_determinante(filas, columnas)).grid(row=filas + 3, column=1, columnspan=2, padx=5, pady=5)

    # Área de resultado
    ttk.Label(frame, text="Resultado:").grid(row=filas + 4, column=0, padx=5, pady=5, sticky=tk.W)
    global area_resultado
    area_resultado = scrolledtext.ScrolledText(frame, width=30, height=5)
    area_resultado.grid(row=filas + 4, column=1, columnspan=2, padx=5, pady=5, sticky=tk.W + tk.E)

    # Área para mostrar el paso a paso
    ttk.Label(frame, text="Paso a Paso:").grid(row=filas + 5, column=0, padx=5, pady=5, sticky=tk.W)
    global area_paso_a_paso
    area_paso_a_paso = scrolledtext.ScrolledText(frame, width=50, height=10, wrap=tk.NONE)
    area_paso_a_paso.grid(row=filas + 5, column=1, columnspan=2, padx=5, pady=5, sticky=tk.W + tk.E)

    # Barra de desplazamiento horizontal
    scroll_x = tk.Scrollbar(frame, orient=tk.HORIZONTAL, command=area_paso_a_paso.xview)
    scroll_x.grid(row=filas + 6, column=1, columnspan=2, sticky=tk.W + tk.E)
    area_paso_a_paso['xscrollcommand'] = scroll_x.set

# Función para obtener la matriz a partir de las entradas
def obtener_matriz(entradas, filas, columnas):
    matriz = []
    for i in range(filas):
        fila = []
        for j in range(columnas):
            valor = entradas[i][j].get()
            try:
                fila.append(float(valor))
            except ValueError:
                messagebox.showerror("Error", f"Valor inválido en la posición ({i + 1}, {j + 1}).")
                return None
        matriz.append(fila)
    return matriz

# Función para calcular el determinante con pasos detallados
def calcular_determinante(filas, columnas):
    matriz_a = obtener_matriz(entradas_matriz_a, filas, columnas)

    if matriz_a is None:
        return

    if filas != columnas:
        messagebox.showerror("Error", "La matriz debe ser cuadrada.")
        return

    resultado, paso_a_paso = calcular_determinante_matriz(matriz_a)

    area_resultado.delete("1.0", tk.END)
    area_paso_a_paso.delete("1.0", tk.END)

    if isinstance(resultado, (int, float)):
        area_resultado.insert(tk.END, str(resultado))
    else:
        area_resultado.insert(tk.END, str(resultado))

    area_paso_a_paso.insert(tk.END, paso_a_paso)

# Función recursiva para calcular el determinante y registrar los pasos
def calcular_determinante_matriz(matriz):
    pasos = []
    determinante = determinante_con_pasos(matriz, pasos)
    paso_a_paso = "\n".join(pasos)
    return determinante, paso_a_paso

# Función para calcular el determinante y registrar cada paso detallado
def determinante_con_pasos(matriz, pasos, nivel=0):
    n = len(matriz)
    if n == 1:
        pasos.append(f"Nivel {nivel}: det({matriz[0][0]}) = {matriz[0][0]}")
        return matriz[0][0]
    elif n == 2:
        resultado = matriz[0][0] * matriz[1][1] - matriz[0][1] * matriz[1][0]
        pasos.append(f"Nivel {nivel}: det([[{matriz[0][0]}, {matriz[0][1]}], [{matriz[1][0]}, {matriz[1][1]}]]) = "
                     f"({matriz[0][0]} * {matriz[1][1]}) - ({matriz[0][1]} * {matriz[1][0]}) = {resultado}")
        return resultado
    else:
        det = 0
        for j in range(n):
            submatriz = [fila[:j] + fila[j + 1:] for fila in matriz[1:]]
            cofactor = (-1) ** j * matriz[0][j]
            det_submatriz = determinante_con_pasos(submatriz, pasos, nivel + 1)
            pasos.append(
                f"Nivel {nivel}: Cofactor = {cofactor}, subdet = {det_submatriz}, contribución = {cofactor * det_submatriz}")
            det += cofactor * det_submatriz
        pasos.append(f"Nivel {nivel}: Determinante de la matriz en nivel {nivel} es {det}")
        return det

# Función para ejecutar el módulo 3
def ejecutar_modulo3(parent, mostrar_menu_principal):
    frame = ttk.Frame(parent)
    frame.grid(row=0, column=0, sticky="nsew")

    parent.grid_rowconfigure(0, weight=1)
    parent.grid_columnconfigure(0, weight=1)

    btn_regresar = ttk.Button(frame, text="<", command=lambda: mostrar_menu_principal(frame))
    btn_regresar.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

    ttk.Label(frame, text="Tamaño de la matriz (filas x columnas):").grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
    entry_tamano_matriz = ttk.Entry(frame, width=10)
    entry_tamano_matriz.grid(row=0, column=2, padx=5, pady=5)

    def generar_entradas():
        tamano = entry_tamano_matriz.get()
        try:
            filas, columnas = map(int, tamano.split("x"))
            crear_entradas_matriz(frame, filas, columnas)
        except ValueError:
            messagebox.showerror("Error","Formato de tamaño de matriz incorrecto. Utilice el formato 'filas x columnas'.")

    ttk.Button(frame, text="Generar Matriz", command=generar_entradas).grid(row=0, column=3, padx=5, pady=5)

    frame.tkraise()









