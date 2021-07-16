

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

def crear_carpetas():
    docentes = []
    #no esta completo pero para ya ahcer el push pq no se si estoy el finde :D
    # crear carpeta inicial
    materia = input("Ingrese las materia: ")
    os.mkdir(materia)
    cant_docentes = int(input("Ingrese la cantidad de docentes en la materia: "))
    for j in range(cant_docentes):
        docente = input(("Ingrese los datos del docente con el siguiente formato, nombre y apellido  mail :"))
        os.mkdir((os.path.join(materia, docente)))
        docentes.append(docente)

    for k in range(len(docentes)):
        print(docentes)
        cant_alum_prof = int(input("Ingrese la cantidad de alumnos de ese profesor"))
        for i in range(cant_alum_prof):
            alumno = input("Ingrese los datos del alumno: \n Formato: nombre del alumno, padron, mail")
            os.mkdir((os.path.join(materia, docente, alumno)))
main()