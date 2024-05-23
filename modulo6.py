import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import numpy as np

def crear_entradas_matriz(frame, filas, columnas):
    # Limpiar el frame antes de crear nuevas entradas
    for widget in frame.winfo_children():
        widget.destroy()

    # Crear etiquetas y entradas para la matriz de transición
    ttk.Label(frame, text="Matriz de Transición:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
    global entradas_matriz
    entradas_matriz = []
    for i in range(filas):
        fila = []
        for j in range(columnas):
            entrada = ttk.Entry(frame, width=5)
            entrada.grid(row=i+2, column=j, padx=5, pady=5)
            fila.append(entrada)
        entradas_matriz.append(fila)

    # Crear entradas para el estado actual
    ttk.Label(frame, text="Estado Actual:").grid(row=filas+2, column=0, padx=5, pady=5, sticky=tk.W)
    global entradas_estado_actual
    entradas_estado_actual = []
    for i in range(filas):
        entrada = ttk.Entry(frame, width=5)
        entrada.grid(row=filas+2, column=i+1, padx=5, pady=5)
        entradas_estado_actual.append(entrada)

    # Crear entrada para los pasos
    ttk.Label(frame, text="Número de Pasos:").grid(row=filas+3, column=0, padx=5, pady=5, sticky=tk.W)
    global entrada_pasos
    entrada_pasos = ttk.Entry(frame, width=5)
    entrada_pasos.grid(row=filas+3, column=1, padx=5, pady=5)

    # Botón calcular
    ttk.Button(frame, text="Calcular", command=lambda: calcular_estado_futuro(filas, columnas)).grid(row=filas+4, column=1, columnspan=2, padx=5, pady=5)

    # Área de resultado
    ttk.Label(frame, text="Resultado:").grid(row=filas+5, column=0, padx=5, pady=5, sticky=tk.W)
    global area_resultado
    area_resultado = scrolledtext.ScrolledText(frame, width=30, height=5)
    area_resultado.grid(row=filas+5, column=1, columnspan=2, padx=5, pady=5, sticky=tk.W+tk.E)

    # Área para mostrar el paso a paso
    ttk.Label(frame, text="Paso a Paso:").grid(row=filas+6, column=0, padx=5, pady=5, sticky=tk.W)
    global area_paso_a_paso
    area_paso_a_paso = scrolledtext.ScrolledText(frame, width=50, height=10)
    area_paso_a_paso.grid(row=filas+6, column=1, columnspan=2, padx=5, pady=5, sticky=tk.W+tk.E)

def obtener_matriz(entradas, filas, columnas):
    matriz = []
    for i in range(filas):
        fila = []
        for j in range(columnas):
            valor = entradas[i][j].get()
            try:
                fila.append(float(valor))
            except ValueError:
                messagebox.showerror("Error", f"Valor inválido en la posición ({i+1}, {j+1}).")
                return None
        matriz.append(fila)
    return matriz

def obtener_estado_actual(entradas, filas):
    estado = []
    for i in range(filas):
        valor = entradas[i].get()
        try:
            estado.append(float(valor))
        except ValueError:
            messagebox.showerror("Error", f"Valor inválido en el estado actual en la posición {i+1}.")
            return None
    return estado

def calcular_estado_futuro(filas, columnas):
    matriz = obtener_matriz(entradas_matriz, filas, columnas)
    estado_actual = obtener_estado_actual(entradas_estado_actual, filas)
    try:
        pasos = int(entrada_pasos.get())
    except ValueError:
        messagebox.showerror("Error", "Número de pasos inválido.")
        return

    if matriz is None or estado_actual is None:
        return

    estado_futuro, paso_a_paso = calcular_estado_futuro_logica(matriz, estado_actual, pasos)

    area_resultado.delete("1.0", tk.END)
    area_paso_a_paso.delete("1.0", tk.END)

    area_resultado.insert(tk.END, "Estado futuro:\n")
    for i, valor in enumerate(estado_futuro):
        area_resultado.insert(tk.END, f"Estado {i+1}: {valor:.4f}\n")

    area_paso_a_paso.insert(tk.END, paso_a_paso)

def calcular_estado_futuro_logica(matriz, estado_actual, pasos):
    estado = estado_actual
    paso_a_paso = "Paso a Paso:\n"
    for paso in range(1, pasos + 1):
        nuevo_estado = []
        paso_a_paso += f"Paso {paso}:\n"
        for j in range(len(matriz[0])):
            valor = sum(estado[i] * matriz[i][j] for i in range(len(matriz)))
            nuevo_estado.append(valor)
            paso_a_paso += f"Estado {j+1}: {valor:.4f}\n"
        estado = nuevo_estado
        paso_a_paso += "\n"
    return estado, paso_a_paso

def ejecutar_modulo6(parent, mostrar_menu_principal):
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

# Iniciar la interfaz gráfica
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Cadenas de Markov")
    root.geometry("600x400")

    # Crear la ventana principal
    main_frame = ttk.Frame(root)
    main_frame.grid(row=0, column=0, sticky="nsew")

    def mostrar_menu_principal(frame):
        frame.tkraise()

    ejecutar_modulo6(main_frame, mostrar_menu_principal)

    root.mainloop()


