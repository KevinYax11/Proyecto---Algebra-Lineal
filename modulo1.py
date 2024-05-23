import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox

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

    # Crear etiquetas y entradas para la matriz B
    ttk.Label(frame, text="Matriz B:").grid(row=filas+3, column=0, padx=5, pady=5, sticky=tk.W)
    global entradas_matriz_b
    entradas_matriz_b = []
    for i in range(filas):
        fila = []
        for j in range(columnas):
            entrada = ttk.Entry(frame, width=5)
            entrada.grid(row=i+filas+4, column=j, padx=5, pady=5)
            fila.append(entrada)
        entradas_matriz_b.append(fila)

    # Operaciones y botón calcular
    ttk.Label(frame, text="Operación:").grid(row=filas*2+5, column=0, padx=5, pady=5, sticky=tk.W)
    global operaciones
    operaciones = tk.StringVar()
    combo_operaciones = ttk.Combobox(frame, textvariable=operaciones, values=["Suma", "Resta", "Multiplicación", "Producto punto"])
    combo_operaciones.grid(row=filas*2+5, column=1, columnspan=2, padx=5, pady=5, sticky=tk.W+tk.E)

    ttk.Button(frame, text="Calcular", command=lambda: realizar_operacion(filas, columnas)).grid(row=filas*2+6, column=1, columnspan=2, padx=5, pady=5)

    # Área de resultado
    ttk.Label(frame, text="Resultado:").grid(row=filas*2+7, column=0, padx=5, pady=5, sticky=tk.W)
    global area_resultado
    area_resultado = scrolledtext.ScrolledText(frame, width=30, height=5)
    area_resultado.grid(row=filas*2+7, column=1, columnspan=2, padx=5, pady=5, sticky=tk.W+tk.E)

    # Área de historial de pasos
    ttk.Label(frame, text="Historial de pasos:").grid(row=filas*2+8, column=0, padx=5, pady=5, sticky=tk.W)
    global area_historial
    area_historial = scrolledtext.ScrolledText(frame, width=50, height=10)
    area_historial.grid(row=filas*2+8, column=1, columnspan=2, padx=5, pady=5, sticky=tk.W+tk.E)

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

def realizar_operacion(filas, columnas):
    operacion = operaciones.get()
    matriz_a = obtener_matriz(entradas_matriz_a, filas, columnas)
    matriz_b = obtener_matriz(entradas_matriz_b, filas, columnas)

    if matriz_a is None or matriz_b is None:
        return

    if operacion == "Suma":
        resultado = sumar_matrices(matriz_a, matriz_b)
    elif operacion == "Resta":
        resultado = restar_matrices(matriz_a, matriz_b)
    elif operacion == "Multiplicación":
        resultado = multiplicar_matrices(matriz_a, matriz_b)
    elif operacion == "Producto punto":
        resultado = producto_punto(matriz_a, matriz_b)
    else:
        resultado = "Operación inválida"

    area_resultado.delete("1.0", tk.END)
    if isinstance(resultado, list):
        for fila in resultado:
            fila_formateada = ','.join(map(str, fila))
            area_resultado.insert(tk.END, fila_formateada + '\n')
    else:
        area_resultado.insert(tk.END, str(resultado))

def ejecutar_modulo1(parent, mostrar_menu_principal):
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

    ttk.Button(frame, text="Generar Matrices", command=generar_entradas).grid(row=0, column=3, padx=5, pady=5)

    frame.tkraise()

def sumar_matrices(A, B):
    filas_A, columnas_A = obtener_dimensiones(A)
    filas_B, columnas_B = obtener_dimensiones(B)
    if filas_A != filas_B or columnas_A != columnas_B:
        return "Las matrices no tienen las mismas dimensiones"
    C = []
    area_historial.insert(tk.END, "\nPaso a paso de la Suma:\n")
    for i in range(filas_A):
        fila = []
        for j in range(columnas_A):
            suma = A[i][j] + B[i][j]
            fila.append(suma)
            area_historial.insert(tk.END, f"A[{i}][{j}] + B[{i}][{j}] = {A[i][j]} + {B[i][j]} = {suma}\n")
        C.append(fila)
    return C

def restar_matrices(A, B):
    filas_A, columnas_A = obtener_dimensiones(A)
    filas_B, columnas_B = obtener_dimensiones(B)
    if filas_A != filas_B or columnas_A != columnas_B:
        return "Las matrices no tienen las mismas dimensiones"
    C = []
    area_historial.insert(tk.END, "\nPaso a paso de la Resta:\n")
    for i in range(filas_A):
        fila = []
        for j in range(columnas_A):
            resta = A[i][j] - B[i][j]
            fila.append(resta)
            area_historial.insert(tk.END, f"A[{i}][{j}] - B[{i}][{j}] = {A[i][j]} - {B[i][j]} = {resta}\n")
        C.append(fila)
    return C

def multiplicar_matrices(A, B):
    filas_A, columnas_A = obtener_dimensiones(A)
    filas_B, columnas_B = obtener_dimensiones(B)
    if columnas_A != filas_B:
        return "Las dimensiones de las matrices no son compatibles para la multiplicación"
    C = []
    area_historial.insert(tk.END, "\nPaso a paso de la Multiplicación:\n")
    for i in range(filas_A):
        fila = []
        for j in range(columnas_B):
            suma = 0
            for k in range(columnas_A):
                multiplicacion = A[i][k] * B[k][j]
                suma += multiplicacion
                area_historial.insert(tk.END, f"A[{i}][{k}] * B[{k}][{j}] = {A[i][k]} * {B[k][j]} = {multiplicacion}\n")
            fila.append(suma)
            area_historial.insert(tk.END, f"Suma de productos para C[{i}][{j}] = {suma}\n")
        C.append(fila)
    return C

def producto_punto(A, B):
    filas_A, columnas_A = obtener_dimensiones(A)
    filas_B, columnas_B = obtener_dimensiones(B)
    if filas_A != filas_B or columnas_A != columnas_B:
        return "Las matrices no tienen las mismas dimensiones"
    suma = 0
    area_historial.insert(tk.END, "\nPaso a paso del Producto punto:\n")
    for i in range(filas_A):
        for j in range(columnas_A):
            producto = A[i][j] * B[i][j]
            suma += producto
            area_historial.insert(tk.END, f"A[{i}][{j}] * B[{i}][{j}] = {A[i][j]} * {B[i][j]} = {producto}\n")
    area_historial.insert(tk.END, f"Suma total de productos punto = {suma}\n")
    return suma


def obtener_dimensiones(matriz):
    filas = len(matriz)
    columnas = len(matriz[0]) if filas > 0 else 0
    return filas, columnas


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



