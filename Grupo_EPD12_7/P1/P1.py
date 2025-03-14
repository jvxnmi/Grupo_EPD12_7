import csv #necesario para leer el dataset

diccionario = dict()  # Diccionario vacío para almacenar registros
encabezados = () #Encabezados del diccionario

def data_extractor():
    global encabezados # Llamamos a la variable global porque vamos a modificarla

    try:
        with open("EPD12_7_happyscore_income.csv", "r",encoding="utf-8") as archivo:  # Abrimos el dataset en modo lectura
            contenido = csv.reader(archivo, delimiter=",")
            encabezados = next(contenido)  # Asignamos la primera línea para los encabezados

            for linea in contenido:  # Construimos el diccionario con el primer campo como clave
                if len(linea) == len(encabezados):  # Verificamos que la línea tenga el número correcto de columnas
                    clave = linea[0].strip()
                    if clave:  # Evitamos claves vacías
                        diccionario[clave] = tuple(linea)
    except FileNotFoundError:
        print("Error: No se encontró el archivo CSV.")
    except Exception as e:
        print(f"Error al procesar el archivo: {e}")


def agregar_registro(): #Esta función te permite añadir un registro mientras va pidiendo los datos segun los encabezadso del dataset, la clave en este caso es el nombre del pais, la tupla country
    if not encabezados:
        print("Error: Primero debe cargar los datos con data_extractor().")
        return

    n_registro = []
    for i, campo in enumerate(encabezados):
        n_elemento = input(f"Ingrese {campo}: ").strip()
        n_registro.append(n_elemento)

    if len(n_registro) == len(encabezados):  # Verificar que se ingresen todos los datos
        n_tupla = tuple(n_registro)
        if n_tupla[0] not in diccionario:
            diccionario[n_tupla[0]] = n_tupla
            print("\nEl registro ha sido agregado correctamente!\n")
        else:
            print("El registro ya existe :(")
            return None
    else:
        print("Error: La cantidad de datos ingresados no es correcta.")
        return None

def buscar_registro(): # Esta funcion permite buscar un registro introduciendo su clave y lo muestra por pantalla, la clave en este caso es el nombre del pais, la tupla country
    clave = input("Ingrese la clave del registro: ").strip()
    if clave in diccionario:
        print(" ".join(encabezados))
        print(" ".join(diccionario[clave]))
        return clave
    else:
        print("La clave introducida no existe")
        return None

def editar_registro(): #Esta funcion permite modificar un registro introduciendo su clave primero para encontrarlo, la clave en este caso es el nombre del pais, la tupla country
    clave = (buscar_registro())  # Llamada a la función que busca y muestra el registro si lo encuentra.

    if clave and clave in diccionario:
        print("Desea editar el registro? [S para confirmar]")
        if input().upper() == "S":
            n_registro = [input(f"Ingrese {campo}: ").strip() for campo in encabezados]
            if len(n_registro) == len(encabezados):
                diccionario[clave] = tuple(n_registro)
                print("Registro modificado con éxito.")
            else:
                print("Error: La cantidad de datos ingresados no es correcta.")
                return None

def borrar_registro(): #Esta función permite eliminar un registro introduciendo su clave primero para encontrarlo, la clave en este caso es el nombre del pais, la tupla country
    clave = str(input("Ingrese la clave del registro que desea borrar: "))

    while clave not in diccionario.keys(): #Bucle que comprueba si la clave esta o no en el diccionario y pide confirmacion para ejecutar la acción
        print("La clave introducida no existe!")
        clave = str(input("Ingrese la clave del registro que desea borrar: "))
    print("¿Desea eliminar el registro: " + clave + " ?") #Confirmacion
    conf = str.upper(input("[S] para confirmar: "))
    if clave in diccionario.keys() and conf == "S": #Si la clave introducida esta en el diccionario y se ha confirmado, entonces se elimina el registro
        diccionario.pop(clave)
        print("Registro eliminado con éxito\n")
    else:
        print("Operación cancelada")


def listar(): #Esta función permite mostrar todos los registros por pantalla
    if not diccionario: #Primero comprueba si hay elementos a mostrar o no
        print("No hay registros para mostrar.")
        return

    print(" ".join(encabezados)) #Si los hay los lista
    for valores in diccionario.values():
        print(" ".join(valores))

def menu(): #Menu con las opciones que se piden en el enunciado
    print("\n **** Menu del programa **** ")
    print("1. Agregar un nuevo registro")
    print("2. Buscar un registro por clave")
    print("3. Editar un registro")
    print("4. Borrar un registro")
    print("5. Listar todos los registros")
    print("6. Salir")



def principal():
    s = True
    while s:
        menu()
        opcion = input("Elija una opción: ")  # Según la opcion que se introduzca se ejecuta la función correspondiente

        match opcion:
            case "1":
                agregar_registro()
            case "2":
                buscar_registro()
            case "3":
                editar_registro()
            case"4":
                borrar_registro()
            case "5":
                listar()
            case "6":
                s = False
                print("Saliendo :(")
            case _: #También se tiene en cuenta el caso de que se meta una opción fuera del límite
                print("Opción no válida, seleccione de 1 a 6, por favor.")
        if s is True:
            input("Pulsa [Enter] para volver al menu principal ")

if __name__ == "__main__":
    data_extractor()
    principal()