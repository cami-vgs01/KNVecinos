from collections import Counter
from tkinter import filedialog
import tkinter as tk
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.spatial.distance as dist

df = pd.DataFrame()
def lecturaArchivo():

    global df
    archivo_csv = filedialog.askopenfilename(filetypes=[("Archivo CSV", "*.csv")])
    # Leer el archivo CSV seleccionado
    try:
        df.drop(index=df.index, columns=df.columns, inplace=True)
        datos = pd.read_csv(archivo_csv)
        df = pd.concat([df, datos], ignore_index=True)
        print("Datos ingresados correctamente")
        return df
    except FileNotFoundError:
        print("No se eligió el archivo")

def calcularKVecinos(mejorK):
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
        dibujar3D(nombres_columnas,datosEntrenamiento,nombre_ultima_columna)
    print(frecuencias)
    distancia = []
    listaTabla = []
    for i in range(indice,df.shape[0]):
        for j in range(0,indice):
            distancia.append(dist.euclidean(df.iloc[i, :-1].values,df.iloc[j, :-1].values))
        dfModificado = datosEntrenamiento.copy()
        dfModificado['DistanciasCalculadas'] = distancia
        dfModificado.sort_values(by=['DistanciasCalculadas'], inplace=True)
        print("")
        print(dfModificado)
        listaTabla.append(dfModificado.copy())
        dfModificado.drop(index=dfModificado.index, columns=dfModificado.columns, inplace=True)
        distancia.clear()
    bandera=True
    n=0
    aux=0
    listaClases = []
    dicK = {}
    while True:
        for i in listaTabla:
            k=1
            print("")
            print("Dato de prueba:")
            print(datosPrueba.iloc[aux,:-1].to_frame().T.to_string(index=False))
            print("")
            for j in range(0,listaTabla[0].shape[0]):
                listaClases.append(i.iloc[j,-2])
                if n >= len(listaTabla):
                    bandera=False
                print("K = ",k)
                print(listaClases)
                freq = Counter(listaClases)
                print('{:5s} {:10s}'.format('Clases','Frecuencia'))
                for numero, frecuencia in freq.items():
                    print('{:5d} {:10d}'.format(numero,frecuencia))
                numero_mas_comun = max(freq, key=freq.get)
                print("")
                print("La clase predicha para este dato de prueba es: ",numero_mas_comun)
                dicK.setdefault(f"K = {k}", []).append(numero_mas_comun)
                k+=1
                n+=1
            listaClases.clear()
            aux+=1
        if bandera==False:
            break

    print(dicK)
    contadorDeK =0
    precisionMax =float('-inf')
    for clave, valores in dicK.items():
        cont =0
        var =0
        contadorDeK+=1
        for valor in valores:
            if valor == datosPrueba.iloc[var,-1]:
                cont+=1
            var+=1
        precision = (cont /len(datosPrueba))*100
        if(precisionMax<precision):
            mejorK = contadorDeK
            precisionMax = precision

        print(f"k = {contadorDeK} tiene una ",precision,"%")
    print(f"El mejor k es {mejorK} con un ", precisionMax)
    return mejorK

def dibujar2D(nombres_columnas,sub_df,color_dict,nombre_ultima_columna):
    sns.scatterplot(x=nombres_columnas[0], y=nombres_columnas[1], hue=nombre_ultima_columna, data=sub_df, palette=color_dict)
    plt.scatter(sub_df.iloc[:,0], sub_df.iloc[:,1], c=sub_df[nombre_ultima_columna].apply(lambda x: color_dict[x]), marker='s')
    plt.xlabel(nombres_columnas[0])
    plt.ylabel(nombres_columnas[1])
    plt.show()

def dibujar3D(nombres_columnas, df, nombre_ultima_columna):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    clases = df[nombre_ultima_columna].unique()
    color_dict = {clase: np.random.rand(3,) for clase in clases} # generamos un diccionario con un color aleatorio por cada clase
    for clase, color in color_dict.items():
        temp_df = df[df[nombre_ultima_columna] == clase]
        ax.scatter(temp_df[nombres_columnas[0]], temp_df[nombres_columnas[1]], temp_df[nombres_columnas[2]], color=color, marker='s', label=str(clase))
    ax.set_xlabel(nombres_columnas[0])
    ax.set_ylabel(nombres_columnas[1])
    ax.set_zlabel(nombres_columnas[2])
    plt.legend()
    plt.show()

def predecirClasificacion(k):
    print(k)
    if df.empty:
        print("Primero debe cargar un archivo para entrenar el modelo")
        return
    if k==0:
        print("Primero debe entrenar el modelo")
        return
    dato = input("Ingrese los datos a predecir separados por comas: ")
    dato = dato.split(",")
    dato = [float(x) for x in dato]
    print(dato)
    distancia = []
    for i in range(df.shape[0]):
        distancia.append(dist.euclidean(dato, df.iloc[i,:-1]))
    df_modificado = df.copy()
    df_modificado['DistanciasCalculadas'] = distancia
    print(df_modificado)
    df_modificado.sort_values(by=['DistanciasCalculadas'], inplace=True)
    print(df_modificado)
    clases = df_modificado.iloc[:k,-2].values
    print(clases)
    frecuencia_clases = Counter(clases)
    clase_predicha = max(frecuencia_clases, key=frecuencia_clases.get)
    print(f"La clase predicha es: {clase_predicha}")

def menu():
    mejorK = 0
    while True:
        print("*******************Algoritmo de K-Vecinos*******************")
        print("1. Ingresar datos desde archivo .csv")
        print("2. Mostrar Datos")
        print("3. Calcular K-Vecinos")
        print("4. Predecir nuevo dato")
        print("5. Salir")
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
                mejorK=calcularKVecinos(mejorK)
            elif opc == 4:
                predecirClasificacion(mejorK)
            elif opc == 5:
                print("Finalizando...")
                break
        except ValueError:
            print("Opcion invalida")

menu()