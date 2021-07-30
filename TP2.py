import os
import csv
from os import listdir
from os.path import isfile, join, isdir
from utils import * 
from gmailUtils import *
import base64
import io 
import zipfile
from quickstart import obtener_servicio
from service_gmail import obtener_servicio_gmail
import shutil
from googleapiclient.http import MediaIoBaseDownload
import shutil
#from oauth2client import file, client, tools


#Modulos
from listar_archivos import listar_archivos
from crear_carpetas import crear_carpetas
from actualizar_entregas import actualizar_entregas

menu = (
    '1)Listar archivos de la carpeta actual.',
    '2)Crear un archivo.',
    '3)Subir un archivo.',
    '4)Descargar un archivo.',
    '5)Sincronizar.',
    '6)Generar carpetas de una evaluaciion.',
    '7)Actualizar entregas de alumnos viıa mail.',
    '8)Salir.'
)

def crear_archivo():
    '''
    pre:
    post: Crea un archivo vacio, segun la extension que elija el usuario
    '''
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

def crear_carpeta():
    '''
    pre:
    post: crea la cantidad de carpetas que quiera el usuario con sus nombres
    '''
    nombre_de_carpetas = input('Ingrese los nombres de las distintas carpetas que quiere crear, separadas con una coma: ')
    lista_nombre_carpetas = nombre_de_carpetas.split(',')
    for nombre in lista_nombre_carpetas:
        file_metadata = {
            'name': nombre,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        obtener_servicio().files().create(body=file_metadata).execute()

def recorrer_el_drive():
    '''
    pre:
    post: Le muestra todos los archivos y carpetas que hay en el drive
    '''
    print('Listado de archivos en remoto: ')
    nombre_archivos = list()
    archivos = obtener_servicio().files().list().execute()
    print('\n')
    for archivo in archivos:
        if archivo == 'files':
            print('\n')
            for i in range(len(archivos[archivo])):

                if archivos[archivo][i]['mimeType'] == 'application/vnd.google-apps.folder':
                    print(i+1,') Carpeta = ','Nombre: ',archivos[archivo][i]['name'],' - ',archivos[archivo][i]['mimeType'],' - id: ',archivos[archivo][i]['id'] )
                    query = f"parents = '{archivos[archivo][i]['id']}'"
                    archivos_de_carpeta = obtener_servicio().files().list(q=query).execute()
                    for archivo_carpeta in archivos_de_carpeta:
                        if archivo_carpeta == 'files':
                            for x in range(len(archivos_de_carpeta[archivo_carpeta])):
                                print(' --- ',i+1,'.',x+1,')Archivo_de_carpeta:','Nombre: ',archivos_de_carpeta[archivo_carpeta][x]['name'],' - ',archivos_de_carpeta[archivo_carpeta][x]['mimeType'],' - id: ',archivos_de_carpeta[archivo_carpeta][x]['id'])
                                nombre_archivos.append(archivos_de_carpeta[archivo_carpeta][x]['name'])

                elif archivos[archivo][i]['name'] not in nombre_archivos:
                    print(i+1,') Archivo =','Nombre: ',archivos[archivo][i]['name'],' - ',archivos[archivo][i]['mimeType'],' - id: ',archivos[archivo][i]['id'])
    print('\n')

def limpiar_carpeta_archivos_a_subir():
    '''
    luego de que el usuario ingrese archivos a la carpeta "Archivos a subir", esta funcion vacia la carpeta para nuevo uso
    '''
    ruta_archivos_a_subir = 'Archivos_a_subir'
    for archivo in os.listdir(ruta_archivos_a_subir):
        archivo = os.path.join(ruta_archivos_a_subir, archivo)
        try:
            if os.path.isfile(archivo):
                os.unlink(archivo)        
        except Exception as e:
            print(e)

    print('Se limpio la carpeta')

def subir_archivo():
    '''
    pre:
    post: sube archivos al drive
    '''
    print('Debe llevar todos los archivos que quiera subir a la carpeta "Archivos_a_subir". ')
    enter = input('Si ya lo hizo apreta enter. ')
    print('\n')

    ruta_archivos_a_subir = 'Archivos_a_subir'
    archivos_a_subir = [nombre for nombre in os.listdir(ruta_archivos_a_subir) if isfile(join(ruta_archivos_a_subir,nombre))]#Devuelve los archivos de la carpeta

    print(archivos_a_subir)
    for filename in archivos_a_subir:
        ruta_archivo= os.path.join(ruta_archivos_a_subir, filename)
        metadata = {'name': filename}
        mimeType = None #Pongo = none para que me tome el tipo de archivo como viene, y no me lo cambie a tipo google docs
        if mimeType:
            metadata['mimeType'] = mimeType
        res = obtener_servicio().files().create(body=metadata, media_body=ruta_archivo).execute()
        if res:
            print('Se subio el archivo: ', filename, res['mimeType'])

    limpiar_carpeta_archivos_a_subir()

def descargar_archivo():
    '''
    pre: debe haber archivos en el drive
    post: descarga el archivo que eliga el usuario del drive
    '''
    nombre_archivos = list()
    archivos = obtener_servicio().files().list().execute()
    print('\n')
    for archivo in archivos:
        if archivo == 'files':
            print('\n')
            for i in range(len(archivos[archivo])):
                if archivos[archivo][i]['mimeType'] == 'application/vnd.google-apps.folder':
                    print(i+1,') Carpeta = ','Nombre: ',archivos[archivo][i]['name'],' - ',archivos[archivo][i]['mimeType'],' - id: ',archivos[archivo][i]['id'] )
                    query = f"parents = '{archivos[archivo][i]['id']}'"
                    archivos_de_carpeta = obtener_servicio().files().list(q=query).execute()
                    for archivo_carpeta in archivos_de_carpeta:
                        if archivo_carpeta == 'files':
                            for x in range(len(archivos_de_carpeta[archivo_carpeta])):
                                print(' --- ',i+1,'.',x+1,')Archivo_de_carpeta:','Nombre: ',archivos_de_carpeta[archivo_carpeta][x]['name'],' - ',archivos_de_carpeta[archivo_carpeta][x]['mimeType'],' - id: ',archivos_de_carpeta[archivo_carpeta][x]['id'])
                                nombre_archivos.append(archivos_de_carpeta[archivo_carpeta][x]['name'])
                elif archivos[archivo][i]['name'] not in nombre_archivos:
                    print(i+1,') Archivo =','Nombre: ',archivos[archivo][i]['name'],' - ',archivos[archivo][i]['mimeType'],' - id: ',archivos[archivo][i]['id'])

    id_correcto = False
    while not id_correcto:#Analizo que el id sea de un archivo y no una carpeta
        id_archivo = input('Copie y pegue el nro de id del archivo que desea descargar(no carpeta): ')
        for i in range(len(archivos['files'])):
            if archivos['files'][i]['id'] == id_archivo:
                if archivos[archivo][i]['mimeType'] == 'application/vnd.google-apps.folder':
                    print('El id que pego corresponde a una carpeta, copie el de un archivo')
                    id_archivo = input('Copie y pegue el nro de id del archivo que desea descargar(no carpeta): ')
                else:
                    archivo_elejido = archivos['files'][i]
                    id_correcto = True
    opcionx = input('Desea modificar el nombre del archivo que va a guardar?(s|n): ')
    if opcionx == 's':
        nombre_archivo =input('Ingrese el nombre con el que quiere guardar el archivo: ')
    else:
        nombre_archivo = archivo_elejido['name']

    request = obtener_servicio().files().get_media(fileId=id_archivo)
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

def ultima_modificacion_local(ruta_archivo):
    '''
    pre: se le manda una ruta de un archivo especifico
    post: devuelve la fecha de ultima modificacion de ese archivo
    ''' 
    estado = os.stat(ruta_archivo)
    fecha = time.localtime(estado.st_mtime)
    fecha = datetime(fecha[0], fecha[1], fecha[2], fecha[3], fecha[4], fecha[5])
    return fecha

def sincronizacion(ruta):
    archivos_remotos = obtener_servicio().files().list(fields='files(name,modifiedTime,id,mimeType)').execute()
    archivos_locales = [a for a in listdir(ruta) if isfile(join(ruta, a))]
    for archivo_local in archivos_locales:
        for archivo_remoto in archivos_remotos:
            if archivo_remoto == 'files':
                for i in range(len(archivos_remotos[archivo_remoto])):
                    if archivo_local == archivos_remotos[archivo_remoto][i]['name']:
                        lista_fecha = archivos_remotos[archivo_remoto][i]['modifiedTime'].split('.')
                        lista_fecha.pop(1)
                        ultima_modificacion_remoto = (''.join(lista_fecha))
                        #arregar_huso = timedelta(hours = 2)
                        #ultima_modificacion_remoto = datetime.strptime(ultima_modificacion_remoto, '%Y-%m-%dT%H:%M:%S') - arregar_huso
                        
                        if ultima_modificacion_local(archivo_local) > ultima_modificacion_remoto:
                            contenido_archivo = MediaFileUpload(archivo_local, mimetype=archivos_remotos[archivo_remoto][i]['mimeType'])
                            obtener_servicio().files().update(fileId=archivos_remotos[archivo_remoto][i]['modifiedTime'], media_body=contenido_archivo)
                            print('hola')

                        elif ultima_modificacion_local(archivo_local) < ultima_modificacion_remoto:
                            print('chau')
                            if (os.path.isfile(archivo_local)): # elimina el archivo
                                os.remove(archivo_local)

                                request = obtener_servicio().files().get_media(fileId=id_archivo)#Descarga archivo
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
                        elif ultima_modificacion_local(archivo_local) == archivos_remotos[archivo_remoto][i]['modifiedTime']:
                            print('No se modificaron')

                    else:
                        #Debe subir el archivo al remoto
                        metadata = {'name': archivo_local} 
                        mimeType = None #Pongo = none para que me tome el tipo de archivo como viene, y no me lo cambie a tipo google docs
                        if mimeType:
                            metadata['mimeType'] = mimeType
                        res = obtener_servicio().files().create(body=metadata, media_body=archivo_local).execute()
                        if res:
                            print('Se subio el archivo: ', archivo_local, res['mimeType'])
    
def crear_carpeta_local(basedir):
    
    print("ver archivos y carpetas")
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
            print("ARCHIVO CREADO CON EXITO")
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
    basedir = os.path.dirname(os.path.abspath(__file__))
  
    while not corte:
        opcion = ingresar_opcion(menu)

        if opcion == 1:
            opcion2 = int(input('Si desea hacerlo en local apreta 1, si desea en remoto apreta 2: '))
            if opcion2 == 1:
               listar_archivos() 

                #print(listado_archivos)

            if opcion2 == 2:
                recorrer_el_drive()

        if opcion == 2:
            opcion2 = int(input('Si desea hacerlo en local apreta 1, si desea en remoto apreta 2: '))
            if opcion2 == 1:
                crear_carpeta_local()
            if opcion2 == 2:
                opcion3 = int(input('Si desea crear un archivo ingresa 1, si desea crear una/s carpeta/s ingresa 2: '))
                if opcion3 == 1:
                    crear_archivo()
                if opcion3 == 2:
                    crear_carpeta()
        
        if opcion == 3:
            subir_archivo()
        
        if opcion == 4:
            descargar_archivo()
        
        if opcion == 5:
            sincronizacion(basedir)

        if opcion == 6:
            crear_carpetas(basedir)

        if opcion == 7:
            actualizar_entregas(basedir)

        if opcion == 8:
            corte = True


main()
