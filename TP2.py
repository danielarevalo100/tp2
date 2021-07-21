<<<<<<< HEAD
import os
import csv
=======
from utils import * 
from gmailUtils import *
import base64
import io 
import zipfile
>>>>>>> 3b6b11407bc5a7910fad9c33d181cddadd2d3874

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



def crear_carpetas():
    evaluacion = "Algebra II" #es para probar. aca iria el directorio de la ev
    os.mkdir(evaluacion)

    #carpeta de los docentes
    with open (r':C\COSAS MUY IMPORTANTES\Facultad\python\docentes.csv', "r") as csv_file: #mismo q arriba pero para el csv de docentes
        for csv_file in csv_file.readlines():
            nombresDocentes = csv_file.split(',')
            os.mkdir((os.path.join(evaluacion,nombresDocentes[0])))

    with open(r'C:\COSAS MUY IMPORTANTES\Facultad\python\docalum.csv', "r") as csv_file1: #idem carpeta doc-alum
        for csv_file1 in csv_file1.readlines():
            list_alumdoc = csv_file1.split(',')
            if list_alumdoc[0] == nombresDocentes[0]:
                os.mkdir((os.path.join(evaluacion,nombresDocentes[0],list_alumdoc[1])))

def getEmailSubject(data : dict = {}) -> str:
    headers = data['payload']['headers']
    subject =  find(lambda item, i: item['name'] == 'Subject', headers)
    if subject:
        return subject['value']
    return ''

def getAttachmentsIds(parts : dict = {}):
    partsWithAttachments = list(filter(lambda item: 'attachmentId' in item['body'], parts))
    return list(map(lambda item: item['body']['attachmentId'] ,partsWithAttachments))


def main():
    corte = False
    #service = obtener_servicio()
  
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
<<<<<<< HEAD
            crear_carpetas()

=======
            pass
>>>>>>> 3b6b11407bc5a7910fad9c33d181cddadd2d3874
        if opcion == 7:
            pass
        
        if opcion == 8:
            corte = True

    print('Hola')


<<<<<<< HEAD
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
=======


main()
>>>>>>> 3b6b11407bc5a7910fad9c33d181cddadd2d3874
