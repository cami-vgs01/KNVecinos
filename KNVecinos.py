from tkinter import filedialog
import tkinter as tk
import pandas as pd
import matplotlib.pyplot as plt
#from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns
import scipy.spatial.distance as dist

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

def calcularKVecinos():
    num_filas, num_columnas = df.shape
    print("Numero de variables: ", num_columnas-1)
    nombres_columnas = list(df.columns)
    indice = int(0.8 * df.shape[0])  # calcula el indice del 80% de las filas
    print("El 80% de datos es: ", indice)
    nombre_ultima_columna = df.columns[-1]  # obtiene el nombre de la ultima columna
    datosEntrenamiento = df.iloc[:indice]    # selecciona solo las filas hasta ese indice
    datosPrueba = df.iloc[indice:]  # selecciona solo las filas desde ese indice
    print("DatosEntrenamiento")
    print(datosEntrenamiento)
    print("DatosPrueba")
    print(datosPrueba)
    palette = sns.color_palette("bright", len(datosEntrenamiento[nombre_ultima_columna].unique()))
    color_dict = dict(zip(datosEntrenamiento[nombre_ultima_columna].unique(), palette))
    frecuencias = df.iloc[:indice, -1].value_counts().reset_index()
    frecuencias.columns = ['Clase', 'Frecuencia']
    if num_columnas-1 <3:
        dibujar2D(nombres_columnas,datosEntrenamiento,color_dict,nombre_ultima_columna)
    elif num_columnas-1 == 3:
        dibujar3D(nombres_columnas,datosEntrenamiento,color_dict,nombre_ultima_columna)
    print(frecuencias)
    distancia = []
    for i in range(indice,df.shape[0]):
        k=1
        for j in range(0,indice):
            distancia.append(dist.euclidean(df.iloc[i, :-1].values,df.iloc[j, :-1].values))
        dfModificado = datosEntrenamiento.copy()
        dfModificado['DistanciasCalculadas'] = distancia
        dfModificado.sort_values(by=['DistanciasCalculadas'], inplace=True)
        print("")
        print(dfModificado)
        #AÑADIR EL MEJOR K
        #
        #
        #
        distancia.clear()
        dfModificado.drop(index=dfModificado.index, columns=dfModificado.columns, inplace=True)

def dibujar2D(nombres_columnas,sub_df,color_dict,nombre_ultima_columna):
    plt.scatter(sub_df.iloc[:,0], sub_df.iloc[:,1], c=sub_df[nombre_ultima_columna].apply(lambda x: color_dict[x]), marker='s')
    plt.xlabel(nombres_columnas[0])
    plt.ylabel(nombres_columnas[1])
    plt.show()

def dibujar3D(nombres_columnas,sub_df,color_dict,nombre_ultima_columna):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(sub_df[nombres_columnas[0]], sub_df[nombres_columnas[1]], sub_df[nombres_columnas[2]],marker='s')
    ax.set_xlabel(nombres_columnas[0])
    ax.set_ylabel(nombres_columnas[1])
    ax.set_zlabel(nombres_columnas[2])
    plt.show()

def menu():
    while True:
        print("*******************Algoritmo de K-Vecinos*******************")
        print("1. Ingresar datos desde archivo .csv")
        print("2. Mostrar Datos")
        print("3. Calcular K-Vecinos")
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
                print(df)
            elif opc == 3:
                calcularKVecinos()
            elif opc == 4:
                print("Finalizando...")
                break
        except ValueError:
            print("Opcion invalida")


menu()