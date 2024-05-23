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
    combo_operaciones = ttk.Combobox(frame, textvariable=operaciones, values=["Calcular Rango"])
    combo_operaciones.grid(row=filas*2+3, column=1, columnspan=2, padx=5, pady=5, sticky=tk.W+tk.E)

    ttk.Button(frame, text="Calcular", command=lambda: calcular_rango(filas, columnas)).grid(row=filas*2+4, column=1, columnspan=2, padx=5, pady=5)

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
            if valor:
                try:
                    fila.append(float(valor))
                except ValueError:
                    messagebox.showerror("Error", f"Valor inválido en la posición ({i+1}, {j+1}).")
                    return None
            else:
                fila.append(0)
        matriz.append(fila)
    return matriz

def calcular_rango(filas, columnas):
    matriz_a = obtener_matriz(entradas_matriz_a, filas, columnas)

    if matriz_a is None:
        return

    resultado, paso_a_paso = rango_matriz(matriz_a)

    area_resultado.delete("1.0", tk.END)
    area_paso_a_paso.delete("1.0", tk.END)

    area_resultado.insert(tk.END, str(resultado))
    area_paso_a_paso.insert(tk.END, paso_a_paso)

def eliminar_filas_ceros(matriz):
    return [fila for fila in matriz if any(elemento != 0 for elemento in fila)]

def eliminar_columnas_ceros(matriz):
    transpuesta = list(map(list, zip(*matriz)))
    transpuesta_sin_ceros = eliminar_filas_ceros(transpuesta)
    return list(map(list, zip(*transpuesta_sin_ceros)))

def convertir_forma_escalon(matriz):
    filas = len(matriz)
    columnas = len(matriz[0])
    paso_a_paso = ""

    for i in range(filas):
        if all(matriz[i][j] == 0 for j in range(columnas)):
            continue

        # Encontrar el pivote
        pivote = matriz[i][matriz[i].index(next(e for e in matriz[i] if e != 0))]
        paso_a_paso += f"Pivote en la fila {i+1}: {pivote}\n"
        for j in range(i + 1, filas):
            factor = matriz[j][matriz[i].index(pivote)] / pivote
            paso_a_paso += f"Eliminando elemento en la posición ({j+1},{i+1}), factor: {factor}\n"
            for k in range(columnas):
                matriz[j][k] = matriz[j][k] - factor * matriz[i][k]
                paso_a_paso += f"{matriz[j][k]} = {matriz[j][k]} - ({factor} * {matriz[i][k]})\n"
        paso_a_paso += f"Matriz después de eliminar filas por debajo del pivote en la columna {i+1}:\n{np.array(matriz)}\n\n"
    return matriz, paso_a_paso

def rango_matriz(matriz):
    paso_a_paso = ""
    matriz = eliminar_filas_ceros(matriz)
    paso_a_paso += f"Matriz después de eliminar filas con ceros:\n{np.array(matriz)}\n\n"
    matriz = eliminar_columnas_ceros(matriz)
    paso_a_paso += f"Matriz después de eliminar columnas con ceros:\n{np.array(matriz)}\n\n"
    matriz, paso_a_paso_conversion = convertir_forma_escalon(matriz)
    paso_a_paso += paso_a_paso_conversion

    rango = len(matriz)
    for fila in matriz:
        if all(elemento == 0 for elemento in fila):
            rango -= 1
    paso_a_paso += f"El rango de la matriz es: {rango}\n\n"
    return rango, paso_a_paso

def ejecutar_modulo4(parent, mostrar_menu_principal):
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
        except ValueError:messagebox.showerror("Error", "Formato de tamaño de matriz incorrecto. Utilice el formato 'filas x columnas'.")

    ttk.Button(frame, text="Generar Matriz", command=generar_entradas).grid(row=0, column=3, padx=5, pady=5)
    frame.tkraise()