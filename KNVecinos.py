from tkinter import filedialog
import tkinter as tk
import pandas as pd

df = pd.DataFrame()
def lecturaArchivo():

    global df
    archivo_csv = filedialog.askopenfilename(filetypes=[("Archivo CSV", "*.csv")])
    # Leer el archivo CSV seleccionado
    try:
        datos = pd.read_csv(archivo_csv)
        df = pd.concat([df, datos], ignore_index=True)
        print("Datos ingresados correctamente")
        return df
    except FileNotFoundError:
        print("No se eligió el archivo")

def menu():
    while True:
        print("*******************Algoritmo de K-Vecinos*******************")
        print("1. Ingresar datos desde archivo .csv")
        print("2. Ingresar datos desde consola")
        print("3. Mostrar datos")
        print("4. Salir")
        try:
            opc = int(input("Opcion: "))
            if opc == 1:
                try:
                    df.drop(index=df.index, columns=df.columns, inplace=True)
                    # Crear la ventana principal
                    root = tk.Tk()

                    # Agregar un botón para abrir el cuadro de diálogo de selección de archivos

                    boton_abrir = tk.Button(root, text="Abrir archivo CSV", command=lecturaArchivo)
                    boton_abrir.pack()

                    # Mostrar la ventana principal
                    root.mainloop()
                except:
                    print("No se eligió el archivo")
            elif opc == 2:
                print("Ingresar datos desde consola")
                print("Ingrese cantidad de variables")

            elif opc == 3:
                print(df)
            elif opc == 4:
                print("Finalizando...")
                break
        except ValueError:
            print("Opcion invalida")
menu()