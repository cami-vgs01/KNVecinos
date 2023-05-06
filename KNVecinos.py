import csv
from tkinter import filedialog
import tkinter as tk


def lecturaArchivo(lista):

    archivo_csv = filedialog.askopenfilename(filetypes=[("Archivo CSV", "*.csv")])
    # Leer el archivo CSV seleccionado
    try:
        with open(archivo_csv) as archivo:
            lector_csv = csv.reader(archivo)
            next(lector_csv)
            for fila in lector_csv:
                lista.append(fila)
            print("Datos ingresados correctamente")
    except FileNotFoundError:
        print("No se eligió el archivo")

def menu():
    lista = []
    while True:
        print("1. Ingresar datos desde archivo .csv")
        print("2. Ingresar datos desde consola")
        print("3. Mostrar datos")
        print("4. Salir")
        try:
            opc = int(input("Opcion: "))
            if opc == 1:
                try:
                    # Crear la ventana principal
                    root = tk.Tk()

                    # Agregar un botón para abrir el cuadro de diálogo de selección de archivos
                    boton_abrir = tk.Button(root, text="Abrir archivo CSV", command=lambda: lecturaArchivo(lista))
                    boton_abrir.pack()

                    # Mostrar la ventana principal
                    root.mainloop()
                except:
                    print("No se eligió el archivo")
            elif opc == 2:
                print("Ingresar datos desde consola")
            elif opc == 3:
                if len(lista) == 0:
                    print("No hay datos para mostrar")
                else:
                    print("Mostrar datos: ")
                    for i in range(len(lista)):
                        print(lista[i])
                    print("Cantidad de datos: ", len(lista))

            elif opc == 4:
                print("Finalizando...")
                break
        except ValueError:
            print("Opcion invalida")
menu()