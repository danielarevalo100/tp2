<<<<<<< HEAD
import os
import csv
from os import listdir
from os.path import isfile, join
=======
from utils import * 
from gmailUtils import *
import base64
import io 
import zipfile
DIRECTORIO_BASE = os.path.dirname(os.path.abspath(__file__))
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

def listar_directorio(ruta):
    archivos = [a for a in listdir(ruta) if isfile(join(ruta, a))]
    return archivos

def init():
    print("ver archivos y carpetas")
    opcion = input("selecciona una opcion c - crear carpeta y e - eliminar: ")
    if opcion == "c":
        nombre_carpeta = input("ingrese nombre carpeta: ")
        directorio_carpeta = os.path.join(DIRECTORIO_BASE, nombre_carpeta)
        if (os.path.isdir(directorio_carpeta)):
            tipo = input("indique el tipo a - archivo y c - carpeta: ")
        if tipo == "a":
            archivo = input("indique el nombre del archivo: ")
            manejador = open(DIRECTORIO_BASE + archivo, "w")
            manejador.close()
            print("ARCHIVO CREADO CON EXITO")
        elif tipo == "c":
            carpeta = input("indique el nombre de la carpeta: ")
            carpeta = carpeta.strip()
            os.mkdir(DIRECTORIO_BASE + carpeta)
            print("carpeta", carpeta, "creado con exito")
    elif opcion == "e":
        nombre = input("ingrese nombre: ")
        eliminar = input("indique archivo / carpeta eliminar :")
        print(nombre+eliminar)
        if (os.path.isfile(nombre+eliminar)):
            os.remove(nombre+eliminar)
            print("archivo", eliminar, "eliminar con exito")
        elif (os.path.isdir(DIRECTORIO_BASE+eliminar)):
            os.rmdir(nombre+eliminar)
            print("carpeta", eliminar, "eliminar con exito")

def getEmailSubject(data : dict = {}) -> str:
    headers = data['payload']['headers']
    subject =  find(lambda item, i: item['name'] == 'Subject', headers)
    if subject:
        return subject['value']
    return ''

def getAttachmentsIds(parts : dict = {}):
    partsWithAttachments = list(filter(lambda item: 'attachmentId' in item['body'], parts))
    return list(map(lambda item: item['body']['attachmentId'] ,partsWithAttachments))


def crear_carpetas():
    alumnos = []
    docentes = []
    docentes_alumnos = []
    basedir = os.path.dirname(os.path.abspath(__file__))
    print(basedir)
    ruta_ev = os.path.join(basedir, 'Evaluacion')
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

def main():
    corte = False
    #service = obtener_servicio()
  
    while not corte:
        opcion = ingresar_opcion()

        if opcion == 1:
            listar_directorio(ruta)
            listado_archivos = listar_directorio(ruta)
            print(listado_archivos)
            print(len(listado_archivos))
        
        if opcion == 2:
            init()
            

        if opcion == 3:
            pass
        
        if opcion == 4:
            pass

        if opcion == 5:
            pass
        
        if opcion == 6:
            crear_carpetas()

            pass
>>>>>>> 3b6b11407bc5a7910fad9c33d181cddadd2d3874
        if opcion == 7:
            pass
        
        if opcion == 8:
            corte = True

    print('Hola')




main()
>>>>>>> 3b6b11407bc5a7910fad9c33d181cddadd2d3874
