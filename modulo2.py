import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import numpy as np

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
            entrada.grid(row=i+2, column=j, padx=5, pady=5)
            fila.append(entrada)
        entradas_matriz_a.append(fila)

    # Operaciones y botón calcular
    ttk.Label(frame, text="Operación:").grid(row=filas*2+3, column=0, padx=5, pady=5, sticky=tk.W)
    global operaciones
    operaciones = tk.StringVar()
    combo_operaciones = ttk.Combobox(frame, textvariable=operaciones, values=["Calcular Inversa"])
    combo_operaciones.grid(row=filas*2+3, column=1, columnspan=2, padx=5, pady=5, sticky=tk.W+tk.E)

    ttk.Button(frame, text="Calcular", command=lambda: calcular_inversa(filas, columnas)).grid(row=filas*2+4, column=1, columnspan=2, padx=5, pady=5)

    # Área de resultado
    ttk.Label(frame, text="Resultado:").grid(row=filas*2+5, column=0, padx=5, pady=5, sticky=tk.W)
    global area_resultado
    area_resultado = scrolledtext.ScrolledText(frame, width=30, height=5)
    area_resultado.grid(row=filas*2+5, column=1, columnspan=2, padx=5, pady=5, sticky=tk.W+tk.E)

    # Área para mostrar el paso a paso
    ttk.Label(frame, text="Paso a Paso:").grid(row=filas*2+6, column=0, padx=5, pady=5, sticky=tk.W)
    global area_paso_a_paso
    area_paso_a_paso = scrolledtext.ScrolledText(frame, width=50, height=10)
    area_paso_a_paso.grid(row=filas*2+6, column=1, columnspan=2, padx=5, pady=5, sticky=tk.W+tk.E)

def obtener_matriz(entradas, filas, columnas):
    matriz = []
    for i in range(filas):
        fila = []
        for j in range(columnas):
            valor = entradas[i][j].get()
            if valor.isdigit():
                fila.append(int(valor))
            else:
                messagebox.showerror("Error", f"Valor inválido en la posición ({i+1}, {j+1}).")
                return None
        matriz.append(fila)
    return matriz

def calcular_inversa(filas, columnas):
    matriz_a = obtener_matriz(entradas_matriz_a, filas, columnas)

    if matriz_a is None:
        return

    resultado, paso_a_paso = matriz_inversa(matriz_a)

    area_resultado.delete("1.0", tk.END)
    area_paso_a_paso.delete("1.0", tk.END)

    if isinstance(resultado, list):
        for fila in resultado:
            fila_formateada = ','.join(map(str, fila))
            area_resultado.insert(tk.END, fila_formateada + '\n')
    else:
        area_resultado.insert(tk.END, str(resultado))

    area_paso_a_paso.insert(tk.END, paso_a_paso)

def matriz_inversa(matriz):
    try:
        matriz_numpy = np.array(matriz, dtype=float)
        inversa = np.linalg.inv(matriz_numpy)
        paso_a_paso = f"Paso 1: Calcular el determinante de la matriz.\n\nDeterminante = {np.linalg.det(matriz_numpy)}\n\nPaso 2: Calcular la matriz adjunta.\n\nMatriz Adjunta:\n{np.linalg.inv(matriz_numpy) * np.linalg.det(matriz_numpy)}\n\nPaso 3: Calcular la inversa dividiendo la matriz adjunta por el determinante.\n\nInversa = Matriz Adjunta / Determinante\n\n"
        return inversa.tolist(), paso_a_paso
    except np.linalg.LinAlgError:
        return "La matriz no es inversible.", "La matriz no es inversible."

def ejecutar_modulo2(parent, mostrar_menu_principal):
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
            messagebox.showerror("Error", "Formato de tamaño de matriz incorrecto. Utilice el formato 'filas x columnas'.")

    ttk.Button(frame, text="Generar Matriz", command=generar_entradas).grid(row=0, column=3, padx=5, pady=5)

    frame.tkraise()

def mostrar_menu_principal(frame):
    frame.grid_forget()

    # Eliminar todos los widgets del frame menu_principal
    for widget in menu_principal.winfo_children():
        widget.destroy()

    menu_principal.grid(row=0, column=0, sticky="nsew")
    menu_principal.tkraise()

    ttk.Label(menu_principal, text="Seleccione un módulo:").grid(row=0, column=0, padx=5, pady=5)

    ttk.Button(menu_principal, text="Módulo 1", command=lambda: ejecutar_modulo1(root, mostrar_menu_principal)).grid(
        row=1, column=0, padx=5, pady=5)

    ttk.Button(menu_principal, text="Módulo 2", command=lambda: ejecutar_modulo2(root, mostrar_menu_principal)).grid(
        row=2, column=0, padx=5, pady=5)
    btn_regresar = ttk.Button(frame, text="<", command=lambda: mostrar_menu_principal(parent))


