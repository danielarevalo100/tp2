

def ingresar_opcion():
    print('\n')
    menu = [
        '1)Listar archivos de la carpeta actual.',
        '2)Crear un archivo.',
        '3)Subir un archivo.',
        '4)Descargar un archivo.',
        '5)Sincronizar.',
        '6)Generar carpetas de una evaluaciion.',
        '7)Actualizar entregas de alumnos viıa mail.',
        '8)Salir.'
    ]
    for i in range(len(menu)):
        print(menu[i])
    opcion = input('Que opcion desea elegir?: ')
    while not opcion.isnumeric() or int(opcion)<1 or int(opcion)>9:
        opcion = input('Eliga una opcion correcta: ')
    opcion = int(opcion)
    return opcion

def main():
    corte = False
    while not corte:
        opcion = ingresar_opcion()

        if opcion == 1:
            pass
        
        if opcion == 2:
            pass

        if opcion == 3:
            pass
        
        if opcion == 4:
            pass

        if opcion == 5:
            pass
        
        if opcion == 6:
            pass

        if opcion == 7:
            pass
        
        if opcion == 8:
            corte = True

    print('Hola')
main()