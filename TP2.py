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

    BASEDIR = os.path.dirname(os.path.abspath(__file__))

    print(BASEDIR)
    RUTA = os.path.join(BASEDIR, evaluacion)
    os.mkdir(RUTA)
    print(RUTA)
    RUTADOC = os.path.join(BASEDIR, 'docentes.csv')
    with open(RUTADOC, "r") as csv_file:
        for linea in csv_file.readlines():
            linea = linea.rstrip()
            nombresDocentes = linea.split(',')
            os.mkdir((os.path.join(RUTA, nombresDocentes[0])))
            docentes.append(nombresDocentes)
    with open(r"C:\COSAS MUY IMPORTANTES\Facultad\python\docalum.csv", "r") as csv_file1:
        for linea2 in csv_file1.readlines():
            linea2 = linea2.rstrip()
            list_alumdoc = linea2.split(',')
            alumnos.append(list_alumdoc)
        print(alumnos)
        for docente in docentes:
            for alumno in alumnos:
                print(evaluacion, docente[0], alumno[1])
                if alumno[0] == docente[0]:
                    os.mkdir((os.path.join(RUTA, docente[0], alumno[1])))


main()
>>>>>>> 3b6b11407bc5a7910fad9c33d181cddadd2d3874
