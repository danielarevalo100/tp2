import os
import csv
from os import listdir
from os.path import isfile, join, isdir
from utils import * 
from gmailUtils import *
import base64
import io 
import zipfile
from service_drive import obtener_servicio
from service_gmail import obtener_servicio_gmail
import shutil
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
import shutil

#Modulos
from listar_archivos import listar_archivos
from crear_carpetas import crear_carpetas
from actualizar_entregas import actualizar_entregas
from accionesDrive import recorrer_el_drive, descargar_archivo, crear_carpeta, subir_archivo, comparar_archivos, diccionarios_archivos

menu = (
    'Listar archivos de la carpeta actual.',
    'Crear un archivo.',
    'Subir un archivo.',
    'Descargar un archivo.',
    'Sincronizar.',
    'Generar carpetas de una evaluaciion.',
    'Actualizar entregas de alumnos viıa mail.',
    'Salir.'
)



def crear_carpeta_local(basedir):
    
    print("ver archivos y carpetas")
    print(os.listdir(basedir))
    opcion = input("selecciona una opcion c - crear carpeta y e - eliminar: ")
    if opcion == "c":
        nombre_carpeta = input("ingrese nombre carpeta: ")
        directorio_carpeta = os.path.join(basedir, nombre_carpeta)
        print(directorio_carpeta)
        os.mkdir(directorio_carpeta)
        if (os.path.isdir(directorio_carpeta)):
            tipo = input("indique el tipo a - archivo y c - carpeta: ")
        if tipo == "a":
            nombre_archivo = input("indique el nombre del archivo con el formato (ej: .txt): ")
            crear_archivo = open(nombre_archivo, "w")
            crear_archivo.close()
            shutil.move(nombre_archivo, directorio_carpeta)
            print("archivo creado satisfactoriamente")
        if tipo == "c":
            carpeta = input("indique el nombre de la carpeta: ")
            os.mkdir(os.path.join(basedir, directorio_carpeta, carpeta))
            print("carpeta", carpeta, "creada con exito")
    elif opcion == "e":
        nombre = input("ingrese nombre: ")
        eliminar = input("indique archivo / carpeta eliminar :")
        if (os.path.isfile(os.path.join(basedir, nombre, eliminar))):
            archivo_a_eliminar = (os.path.join(basedir, nombre, eliminar))
            os.remove(archivo_a_eliminar)
            print("archivo", eliminar, "eliminado con exito")
        elif (os.path.isdir((os.path.join(basedir, nombre, eliminar)))):
            carpeta_a_eliminar = (os.path.join(basedir, nombre, eliminar))
            os.rmdir(carpeta_a_eliminar)
            print("carpeta", eliminar, "eliminado con exito")

def main():
    corte = False
    basedir = os.path.dirname(os.path.abspath(__file__))
  
    while not corte:
        opcion = ingresar_opcion(menu)
        opcion +=1
        if opcion == 1:
            opcion2 = int(input('Si desea hacerlo en local apreta 1, si desea en remoto apreta 2: '))
            if opcion2 == 1:
               listar_archivos(basedir) 
            if opcion2 == 2:
                recorrer_el_drive()

        if opcion == 2:
            opcion2 = int(input('Si desea hacerlo en local apreta 1, si desea en remoto apreta 2: '))
            if opcion2 == 1:
                crear_carpeta_local(basedir)
            if opcion2 == 2:
                opcion3 = int(input('Si desea crear un archivo ingresa 1, si desea crear una/s carpeta/s ingresa 2: '))
                if opcion3 == 1:
                    crear_archivo()
                if opcion3 == 2:
                    crear_carpeta()
        
        if opcion == 3:
            subir_archivo()
        
        if opcion == 4:
            descargar_archivo(basedir)
        
        if opcion == 5:
            dict_archivos_locales, dict_archivos_remoto = diccionarios_archivos(basedir)
            comparar_archivos(dict_archivos_locales, dict_archivos_remoto,basedir)

        if opcion == 6:
            crear_carpetas(basedir)

        if opcion == 7:
            actualizar_entregas(basedir)

        if opcion == 8:
            corte = True

main()
