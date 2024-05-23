import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import numpy as np

# Diccionario para mapear letras a números (A = 1, B = 2, ...)
LETRAS_A_NUMEROS = {letra: codigo for codigo, letra in enumerate('ABCDEFGHIJKLMNÑOPQRSTUVWXYZ ', start=1)}
NUMEROS_A_LETRAS = {v: k for k, v in LETRAS_A_NUMEROS.items()}

def convertir_mensaje_a_numeros(mensaje):
    numeros = []
    for letra in mensaje.upper():
        if letra in LETRAS_A_NUMEROS:
            numeros.append(LETRAS_A_NUMEROS[letra])
        else:
            numeros.append(27)  # Reemplazar caracteres desconocidos con un espacio
    return numeros

def convertir_numeros_a_mensaje(numeros):
    mensaje = ''
    for num in numeros:
        if num in NUMEROS_A_LETRAS:
            mensaje += NUMEROS_A_LETRAS[num]
        else:
            mensaje += '?'  # Reemplazar números desconocidos con un signo de interrogación
    return mensaje

def cifrar_mensaje(mensaje, clave):
    numeros_mensaje = convertir_mensaje_a_numeros(mensaje)
    tamano_clave = len(clave)
    mensaje_cifrado = []
    paso_a_paso = "Cifrado Paso a Paso:\n"
    for i in range(0, len(numeros_mensaje), tamano_clave):
        bloque = numeros_mensaje[i:i+tamano_clave]
        if len(bloque) < tamano_clave:
            bloque.extend([27] * (tamano_clave - len(bloque)))
        matriz_bloque = np.array(bloque).reshape(-1, 1)
        matriz_clave = np.array(clave)
        resultado = np.matmul(matriz_clave, matriz_bloque)
        mensaje_cifrado.extend(resultado.flatten().tolist())
        paso_a_paso += f"Bloque {i//tamano_clave + 1}:\n"
        paso_a_paso += f"  - Multiplicación de la matriz clave por el bloque:\n{matriz_clave}\n{matriz_bloque}\nResultado:\n{resultado}\n\n"
    area_paso_a_paso.delete("1.0", tk.END)
    area_paso_a_paso.insert(tk.END, paso_a_paso)
    return mensaje_cifrado

def descifrar_mensaje(mensaje_cifrado, clave):
    bloques = [mensaje_cifrado[i:i+len(clave)] for i in range(0, len(mensaje_cifrado), len(clave))]
    paso_a_paso = "Descifrado Paso a Paso:\n"
    numeros_mensaje = []
    for idx, bloque in enumerate(bloques):
        matriz_bloque = np.array(bloque).reshape(-1, 1)
        matriz_clave = np.linalg.inv(np.array(clave))
        resultado = np.matmul(matriz_clave, matriz_bloque)
        numeros_mensaje.extend(np.round(resultado).flatten().astype(int).tolist())
        paso_a_paso += f"Bloque {idx + 1}:\n"
        paso_a_paso += f"  - Multiplicación de la inversa de la matriz clave por el bloque cifrado:\n{matriz_clave}\n{matriz_bloque}\nResultado:\n{resultado}\n\n"
    area_paso_a_paso.delete("1.0", tk.END)
    area_paso_a_paso.insert(tk.END, paso_a_paso)
    return convertir_numeros_a_mensaje(numeros_mensaje)


def crear_entradas_matriz(frame, filas, columnas):
    for widget in frame.winfo_children():
        widget.destroy()

    ttk.Label(frame, text="Matriz Clave:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
    global entradas_matriz_a
    entradas_matriz_a = []
    for i in range(filas):
        fila = []
        for j in range(columnas):
            entrada = ttk.Entry(frame, width=5)
            entrada.grid(row=i+2, column=j, padx=5, pady=5)
            fila.append(entrada)
        entradas_matriz_a.append(fila)

    ttk.Label(frame, text="Mensaje:").grid(row=filas + 2, column=0, padx=5, pady=5, sticky=tk.W)
    global entrada_mensaje
    entrada_mensaje = scrolledtext.ScrolledText(frame, width=30, height=3)
    entrada_mensaje.grid(row=filas + 2, column=1, columnspan=2, padx=5, pady=5, sticky=tk.W+tk.E)

    ttk.Label(frame, text="Operación:").grid(row=filas*2 + 3, column=0, padx=5, pady=5, sticky=tk.W)
    global operaciones
    operaciones = tk.StringVar()
    combo_operaciones = ttk.Combobox(frame, textvariable=operaciones, values=["Cifrar", "Descifrar"])
    combo_operaciones.grid(row=filas*2 + 3, column=1, columnspan=2, padx=5, pady=5, sticky=tk.W+tk.E)

    ttk.Button(frame, text="Calcular", command=lambda: calcular_operacion(filas, columnas)).grid(row=filas*2 + 4, column=1, columnspan=2, padx=5, pady=5)

    ttk.Label(frame, text="Resultado:").grid(row=filas*2 + 5, column=0, padx=5, pady=5, sticky=tk.W)
    global area_resultado
    area_resultado = scrolledtext.ScrolledText(frame, width=30, height=5)
    area_resultado.grid(row=filas*2 + 5, column=1, columnspan=2, padx=5, pady=5, sticky=tk.W+tk.E)

    ttk.Label(frame, text="Paso a Paso:").grid(row=filas*2 + 6, column=0, padx=5, pady=5, sticky=tk.W)
    global area_paso_a_paso
    area_paso_a_paso = scrolledtext.ScrolledText(frame, width=50, height=10)
    area_paso_a_paso.grid(row=filas*2 + 6, column=1, columnspan=2, padx=5, pady=5, sticky=tk.W+tk.E)

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

def calcular_operacion(filas, columnas):
    matriz_a = obtener_matriz(entradas_matriz_a, filas, columnas)
    if matriz_a is None:
        return

    operacion = operaciones.get()
    mensaje = entrada_mensaje.get("1.0", tk.END).strip()
    resultado = ""
    paso_a_paso = ""

    if operacion == "Cifrar":
        mensaje_cifrado = cifrar_mensaje(mensaje, matriz_a)
        resultado = ' '.join(map(str, mensaje_cifrado))
        paso_a_paso = "Mensaje cifrado paso a paso."
    elif operacion == "Descifrar":
        try:
            mensaje_cifrado = list(map(int, mensaje.split()))
            resultado = descifrar_mensaje(mensaje_cifrado, matriz_a)
            paso_a_paso = "Mensaje descifrado paso a paso."
        except ValueError:
            messagebox.showerror("Error", "Mensaje cifrado inválido. Debe contener solo números separados por espacios.")

    area_resultado.delete("1.0", tk.END)
    area_resultado.insert(tk.END, resultado)
    area_paso_a_paso.delete("1.0", tk.END)
    area_paso_a_paso.insert(tk.END, paso_a_paso)

def ejecutar_modulo5(parent, mostrar_menu_principal):
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

