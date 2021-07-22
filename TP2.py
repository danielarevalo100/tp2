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
    alumnos = []
    docentes = []
    docentes_alumnos = []
    evaluacion = "AlgebraII"
    basedir = os.path.dirname(os.path.abspath(__file__))

    print(basedir)
    ruta_ev = os.path.join(basedir, evaluacion)
    os.mkdir(ruta_ev)
    if os.path.isdir(ruta_ev):
        print("La carpeta ya existe")
    ruta_docentes = os.path.join(basedir, 'docentes.csv')
    ruta_alum_docentes = os.path.join(basedir,'docalum.csv')
    ruta_alumnos = os.path.join(basedir, 'alumnos.csv')


    with open(ruta_docentes, "r") as csv_file:
        for linea in csv_file.readlines():
            linea = linea.rstrip()
            nombresDocentes = linea.split(',')
            os.mkdir((os.path.join(ruta_ev, nombresDocentes[0])))
            docentes.append(nombresDocentes)

    with open(ruta_alumnos, 'r') as csv_file:
        for linea in csv_file.readlines():
            linea = linea.rstrip()
            list_alumnos = linea.split(',')
            alumnos.append(list_alumnos)

    with open(ruta_alum_docentes, "r") as csv_file1:
        for linea2 in csv_file1.readlines():
            linea2 = linea2.rstrip()
            list_alumdoc = linea2.split(',')
            docentes_alumnos.append(list_alumdoc)
        for docente in docentes:
            for docentes_alumno in docentes_alumnos:
                for alumno in alumnos:
                    if docentes_alumno[0] == docente[0] and docentes_alumno[1] == alumno[0]:
                        os.mkdir((os.path.join(ruta_ev, docente[0], alumno[0]+" "+alumno[1])))

main()
>>>>>>> 3b6b11407bc5a7910fad9c33d181cddadd2d3874
