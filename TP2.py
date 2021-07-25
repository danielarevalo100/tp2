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
    archivos = obtener_servicio().files().list().execute()#Primero recorro el drive para que el usuario elija cual archivo quiere descargar
    for archivo in archivos:
        if archivo == 'files':
            print('\n')
            for i in range(len(archivos[archivo])):
                print(i+1,')  Nombre: ',archivos[archivo][i]['name'],' - ',archivos[archivo][i]['mimeType'],' - id: ',archivos[archivo][i]['id'] )
    archivo_a_descargar = int(input('Ingrese el nro del archivo que quiere descargar: '))
    archivo_a_descargar-=1
    file_id = archivos[archivo][archivo_a_descargar]['id']
    opcionx = input('Desea modificar el nombre del archivo que va a guardar?(s|n): ')
    if opcionx == 's':
        nombre_archivo =input('Ingrese el nombre con el que quiere guardar el archivo: ')
    else:
        nombre_archivo = archivos[archivo][archivo_a_descargar]['name']
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
    service = obtener_servicio_gmail()

    # por ahora lo se hizo con el ID del mail que tiene el comprimido, luego se implementara una busqueda con el nombre de la evaluacion
    messageInfo = getMailById(service, '17ab6106a4a03c07')
    print(getEmailSubject(messageInfo))
    attachments = getAttachmentsIds(messageInfo)

    att = service.users().messages().attachments().get(userId='me', messageId='17ab6106a4a03c07', id=attachments[0]).execute()
    files = base64.urlsafe_b64decode(att['data'])

    z = zipfile.ZipFile(io.BytesIO(files))
    z.extractall()
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
            opcion2 = int(input('Si desea hacerlo en local apreta 1, si desea en remoto apreta 2: '))
            if opcion2 == 1:
               listar_archivos() 

                #print(listado_archivos)

            if opcion2 == 2:
                recorrer_el_drive()

        if opcion == 2:
            opcion2 = int(input('Si desea hacerlo en local apreta 1, si desea en remoto apreta 2: '))
            if opcion2 == 1:
                init()
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
            pass
        
        if opcion == 6:
            #crear_carpetas()
            service = obtener_servicio_gmail()
            print(service.users().getProfile(userId='me').execute())
        
            pass
        if opcion == 7:
            pass

        if opcion == 8:
            corte = True




main()
