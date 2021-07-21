import os
import csv

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
            crear_carpetas()

        if opcion == 7:
            pass
        
        if opcion == 8:
            corte = True

    print('Hola')


def ingresarEntero(mensaje: str) -> int:
    '''
    Pre:  Recibe un input
    Post: Retorna el valor solo si es validado por la condicion Is Numeric
    '''

    valor = input(mensaje)
    while not (valor.isnumeric()):
        valor = input("Error, ingrese el valor nuevamente: ")
    valor = int(valor)

    return valor

def crear_carpetas():
    docentes = []
    alumnos = []
    evaluacion = "AlgebraII"
    os.mkdir(evaluacion)
    i = 0

    # carpeta de los docentes
    with open(r"C:\COSAS MUY IMPORTANTES\Facultad\python\docentes.csv", "r") as csv_file:
        for csv_file in csv_file.readlines():
            nombresDocentes = csv_file.split(',')
            os.mkdir((os.path.join(evaluacion, nombresDocentes[0])))
            docentes.append(nombresDocentes)
    with open(r"C:\COSAS MUY IMPORTANTES\Facultad\python\docalum.csv", "r") as csv_file1:
        for csv_file1 in csv_file1.readlines():
            list_alumdoc = csv_file1.split(',')
            alumnos.append(list_alumdoc)
        print(alumnos)
        for i in range(len(docentes)):
            for k in range(len(alumnos)):
                print(evaluacion, docentes[i][0], alumnos[k][1])
                if alumnos[k][0] == docentes[i][0]:
                    os.mkdir((os.path.join(evaluacion, docentes[i][0], alumnos[k][1])))
                print(os.path.join(evaluacion, docentes[i][0], alumnos[k][1]))
