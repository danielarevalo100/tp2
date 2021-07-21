from  __future__ import print_function

from quickstart import obtener_servicio

import os
import io
from googleapiclient.http import MediaIoBaseDownload

from os.path import isfile, join, isdir

from oauth2client import file, client, tools

def ingresar_opcion():
    menu = [
        '1)Listar archivos',
        '2)Crear un archivo o carpeta',
        '3)Subir un archvo',
        '4)Descargar archivo'
    ]
    print("\n")
    for i in range(len(menu)):
        print(menu[i])
    opcion=input("Ingrese la opcion que desea realizar: ")
    while not (opcion.isnumeric() and int(opcion)> 0 and int(opcion)< 5):
        opcion= input("Debe ingresar un valor posible: ")
    opcion = int(opcion)
    return opcion

def recorrer_el_drive():
    archivos = obtener_servicio().files().list().execute()

    for archivo in archivos:
        if archivo == 'files':
            print('\n')
            for i in range(len(archivos[archivo])):
                print(i+1,')','Nombre: ',archivos[archivo][i]['name'],' - ',archivos[archivo][i]['mimeType'],' - id: ',archivos[archivo][i]['id'] )
            elejir_carpeta = int(input('Si quiere entrar a alguna carpeta ingrese su respectivo numero: '))
            elejir_carpeta -=1
            print(archivos[archivo][elejir_carpeta]['name'])
            print(archivos[archivo][elejir_carpeta][0]['name'])
            for i in range(len(archivos[archivo][elejir_carpeta])):
                print(i+1,')','Nombre: ',archivos[archivo][elejir_carpeta][i]['name'],' - ',archivos[archivo][elejir_carpeta][i]['mimeType'],' - id: ',archivos[archivo][elejir_carpeta][i]['id'] )


def crear_archivo():
    opcionx = int(input('Si desea crear un archivo ingresa 1, si desea crear una carpeta ingresa 2? '))
    if opcionx == 1:
        mimetype = ''
        tipo_de_archivo = [['1) .txt','text/plain'],['2) .jpeg','image/jpeg'],['3) .pdf','application/pdf'],['4) .zip','application/zip']]
        for i in range(len(tipo_de_archivo)):
            print(tipo_de_archivo[i][0])
        tipo_archivo = int(input('Eleji el tipo de archivo que queres para tu nuevo archivo: '))
        tipo_archivo-=1
        mimetype = tipo_de_archivo[tipo_archivo][1]
        print(mimetype)
        nombre_archivo = input('Ingrese el nombre del nuevo archivo: ')
        file_metadata = {
            'name' : nombre_archivo,
            'mimeType' : mimetype
            }
        file = obtener_servicio().files().create(body=file_metadata,
                                    fields='id').execute()
        print('File ID: %s' % file.get('id'))
    
    if opcionx ==2:#Crea la cantidad de carpetas que quiera el usuario
        nombre_de_carpetas = input('Ingrese los nombres de las distintas carpetas que quiere crear, separadas con una coma: ')
        lista_nombre_carpetas = nombre_de_carpetas.split(',')
        for nombre in lista_nombre_carpetas:
            file_metadata = {
                'name': nombre,
                'mimeType': 'application/vnd.google-apps.folder'
            }
            obtener_servicio().files().create(body=file_metadata).execute()

def subir_archivo():
    print('Debe llevar todos los archivos que quiera subir a la carpeta "Archivos_a_subir". ')
    enter = input('Si ya lo hizo apreta enter. ')
    print('\n')
    ruta_archivos_a_subir = r'.\Archivos _a_subir'
    #contenido = os.listdir(ruta_archivos_a_subir) #Te devuelve el contenido de la carpeta
    archivos_a_subir = [nombre for nombre in os.listdir(ruta_archivos_a_subir) if isfile(join(ruta_archivos_a_subir,nombre))]#Devuelve los archivos de la carpeta
    # ARCHIVOS_A_SUBIR = ['nro_tramite.txt','photo.jpeg']
    print(archivos_a_subir)
    for filename in archivos_a_subir:
        metadata = {'name': filename}
        mimeType = None #Pongo = none para que me tome el tipo de archivo como viene, y no me lo cambie a tipo google docs
        if mimeType:
            metadata['mimeType'] = mimeType
        res = obtener_servicio().files().create(body=metadata, media_body=filename).execute()
        if res:
            print('Se subio el archivo: ', filename, res['mimeType'])

def descargar_archivo():
    archivos = obtener_servicio().files().list().execute()#Primero recorro el drive para que el usuario elija cual archivo quiere descargar
    for archivo in archivos:
        if archivo == 'files':
            print('\n')
            for i in range(len(archivos[archivo])):
                print('Nombre: ',archivos[archivo][i]['name'],' - ',archivos[archivo][i]['mimeType'],' - id: ',archivos[archivo][i]['id'] )

    file_id = input('Copie e ingrese aqui el id del archivo que quiere descargar: ') 
    nombre_archivo =input('Ingrese el nombre con el que quiere guardar el archivo: ')
    request = obtener_servicio().files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))

    fh.seek(0)

    with open(os.path.join('./Archivos_descargados', nombre_archivo), 'wb') as f:# Te guarda los archivos que descargas en la carpeta 'Archivos descargados'
        f.write(fh.read())
        f.close()

def main():

    corte = False
    while not corte:
        opcion = ingresar_opcion()

        if opcion == 1:
            #Listado de archivos (3.2)
            #Tengo que listar todas carpetas y hacer que el usuario pueda recorrerlas
            # Para recorrerlas puedo usar el id de la carpeta que el usuario elija y meterme ahi
            recorrer_el_drive()

        if opcion == 2:
            #Crear archvios(3.3), y tambien carpetas
            #Dar una lista de posibles extensiones(.zip, .pdf , .txt)
            crear_archivo()
            
        
        if opcion == 3:
            #Subir archivo(3.4)
            # Subir archivos especificos, tengo que hacer que el usuario elija cual quiere subir
            #crear una carpeta y que el usuario guarde los archivos que quiera subir
            subir_archivo()

        if opcion == 4:
            #Descargar archivo(3.5)
            descargar_archivo()

            
        opcion2 = input('Desea volver al menu? (s|n) ')
        if opcion2 != 's':
            corte = True

main()

# ruta_archivos_a_subir = r'.\Archivos _a_subir'
# print(ruta_archivos_a_subir)
# print('\n')
# contenido = os.listdir(ruta_archivos_a_subir) #Te devuelve el contenido de la carpeta
# print(contenido)
# print('\n')
# archivos = [nombre for nombre in os.listdir(ruta_archivos_a_subir) if isfile(join(ruta_archivos_a_subir,nombre))]
# for i in range(len(archivos)):
#     print(archivos[i])
# for i in range(len(contenido)):
#     print(contenido[i])

# aca tendria que imprimirme todos en pantalla
# print(obtener_servicio().files().list().execute())



##Crear carpetas que quiera el usuario
# nombre_de_carpetas = input('Ingrese los nombres de las distintas carpetas que quiere crear, separadas con una coma: ')
# lista_nombre_carpetas = nombre_de_carpetas.split(',')
# for nombre in lista_nombre_carpetas:
#     file_metadata = {
#         'name': nombre,
#         'mimeType': 'application/vnd.google-apps.folder'
#     }
#     obtener_servicio().files().create(body=file_metadata).execute()


#get('items',[])