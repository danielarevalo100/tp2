from service_drive import obtener_servicio
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
import io 
from os import path, listdir, unlink
from os.path import isfile, join, isdir
import os
import time
from datetime import datetime, timedelta

def recorrer_el_drive(id='root', profundidad=0):
    '''
    pre:
    post: Le muestra todos los archivos y carpetas que hay en el drive
    '''
    driveid = obtener_servicio().files().get(fileId=id).execute()['id']
    query = f"parents = '{driveid}'"
    archivos = obtener_servicio().files().list(q=query).execute()['files']

    for archivo in archivos:
        espacios = ''
        for i in range(profundidad):
            espacios += '   '
        if archivo['mimeType'] == 'application/vnd.google-apps.folder':
            print(espacios, 'carpeta', archivo['name'])
            recorrer_el_drive(archivo['id'], profundidad+1)
        else:
            print(espacios, archivo['name'], 'id: ',archivo['id'])

def descargar_archivo(basedir):
    '''
    pre: debe haber archivos en el drive
    post: descarga el archivo que eliga el usuario del drive
    '''
    recorrer_el_drive()
    print('\n')
    archivos = obtener_servicio().files().list().execute()
    id_archivo = input('Copie y pegue el nro de id del archivo que desea descargar: ')
    for i in range(len(archivos['files'])):
        if archivos['files'][i]['id'] == id_archivo:
                print('here')
                archivo_elejido = archivos['files'][i]
                
    opcionx = input('Desea modificar el nombre del archivo que va a guardar?(s|n): ')
    if opcionx == 's':
        nombre_archivo =input('Ingrese el nombre con el que quiere guardar el archivo: ')
    else:
        nombre_archivo = archivo_elejido['name']

    request = obtener_servicio().files().get_media(fileId=id_archivo)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    opcion = int(input('Si desea guardar el archivo en una subcarpeta aprete 1, si desea que se guarde en la carpeta local aprete 2: '))
    
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))

    fh.seek(0)
    
    if opcion == 1:
        with open(path.join('./Archivos_descargados', nombre_archivo), 'wb') as f:# Te guarda los archivos que descargas en la carpeta 'Archivos descargados'
            f.write(fh.read())
            f.close()
    elif opcion ==2:
        with open(path.join(basedir, nombre_archivo), 'wb') as f:# Te guarda en la carpeta local
            f.write(fh.read())
            f.close()


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
    print('se crearon  las carpetas')


def limpiar_carpeta_archivos_a_subir():
    '''
    luego de que el usuario ingrese archivos a la carpeta "Archivos a subir", esta funcion vacia la carpeta para nuevo uso
    '''
    ruta_archivos_a_subir = 'Archivos_a_subir'
    for archivo in listdir(ruta_archivos_a_subir):
        archivo = path.join(ruta_archivos_a_subir, archivo)
        try:
            if path.isfile(archivo):
                unlink(archivo)        
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
    archivos_a_subir = [nombre for nombre in listdir(ruta_archivos_a_subir) if isfile(join(ruta_archivos_a_subir,nombre))]#Devuelve los archivos de la carpeta

    print(archivos_a_subir)
    for filename in archivos_a_subir:
        ruta_archivo= path.join(ruta_archivos_a_subir, filename)
        metadata = {'name': filename}
        mimeType = None #Pongo = none para que me tome el tipo de archivo como viene, y no me lo cambie a tipo google docs
        if mimeType:
            metadata['mimeType'] = mimeType
        res = obtener_servicio().files().create(body=metadata, media_body=ruta_archivo).execute()
        if res:
            print('Se subio el archivo: ', filename, res['mimeType'])

    limpiar_carpeta_archivos_a_subir()

def ultima_modificacion_local(ruta_archivo):
    '''
    pre: se le manda una ruta de un archivo especifico
    post: devuelve la fecha de ultima modificacion de ese archivo
    ''' 
    estado = os.stat(ruta_archivo)
    fecha = time.localtime(estado.st_mtime)
    fecha = datetime(fecha[0], fecha[1], fecha[2], fecha[3], fecha[4], fecha[5])
    return fecha

def diccionarios_archivos(basedir):
    '''
    genera diccionarios con los archivos/carpetas locales y remotos
    '''
    archivos_remotos = obtener_servicio().files().list(fields='files(name,modifiedTime,id,mimeType)').execute()
    dict_archivos_remoto = dict()
    for archivo_remoto in archivos_remotos['files']:
        lista_fecha = archivo_remoto['modifiedTime'].split('.')
        lista_fecha.pop(1)
        ultima_modificacion_remoto = (''.join(lista_fecha))
        desfase_horario = timedelta(hours = 3)
        ultima_modificacion_remoto = datetime.strptime(ultima_modificacion_remoto, '%Y-%m-%dT%H:%M:%S') - desfase_horario
        dict_archivos_remoto[archivo_remoto['name']] = [ultima_modificacion_remoto, archivo_remoto['id'], archivo_remoto['mimeType']]

    with os.scandir(basedir) as ficheros:
        archivos_locales = list()
        for i in ficheros:
            archivos_locales.append(i.name)
    dict_archivos_locales = dict()
    for archivo_local in archivos_locales:
        dict_archivos_locales[archivo_local] = ultima_modificacion_local(archivo_local)

    return dict_archivos_locales, dict_archivos_remoto

def comparar_fechas(dict_archivos_locales,dict_archivos_remoto,archivo):
    '''
    pre: un archivo debe estar en la carpeta local como en la de remoto
    post: compara las fechas de modificacion y remplaza el archivo mas viejo
    '''
    modificacion_local = dict_archivos_locales[archivo]
    modificacion_remoto = dict_archivos_remoto[archivo][0]

    if modificacion_local > modificacion_remoto:#Modifica el archivo que esta en el drive por el que esta en local
        contenido_archivo = MediaFileUpload(archivo, mimetype= dict_archivos_remoto[archivo][2])
        obtener_servicio().files().update(fileId=dict_archivos_remoto[archivo][1], media_body=contenido_archivo).execute()
        print('Se modifico el archivo', archivo)

    elif modificacion_local < modificacion_remoto:
        if (os.path.isfile(archivo)): # elimina el archivo
            os.remove(archivo)
            request = obtener_servicio().files().get_media(fileId=dict_archivos_remoto[archivo][1])#Descarga archivo
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)
            fh.seek(0)
            with open(os.path.join(basedir, archivo), 'wb') as f:# Te guarda los archivos que descargas en la carpeta 'Archivos descargados'
                f.write(fh.read())
                f.close()
    
    
    elif modificacion_local == modificacion_remoto:
        print('No se modifico el archivo ', archivo)

def comparar_archivos(dict_archivos_locales, dict_archivos_remoto, basedir):
    cosas_quenoquiero_subir = ['__pycache__','Archivos_a_subir','Archivos_descargados','.gitignore','actualizar_entregas.py','client_secret.json','crear_carpetas.py','gmailUtils.py','listar_archivos.py','README.md','service_drive.py','service_gmail.py','TP2.py','utils.py','token_drive.json','token.json']#Por si hay archivos en la carpeta principal que no queres subir
    list_remoto = list() #Se usa para ver los archivos que estan en el remoto pero no en el drive

    for claves, valores in dict_archivos_locales.items():
        if claves in dict_archivos_remoto:
            #LLamo a la funcion que analiza las fechas de modificacion
            comparar_fechas(dict_archivos_locales, dict_archivos_remoto,claves)
        elif claves not in cosas_quenoquiero_subir:
            #Debe subir el archivo al remoto
            metadata = {'name': claves}
            contenido = MediaFileUpload(claves)
            obtener_servicio().files().create(body=metadata,media_body=contenido).execute()
            print('Se subio el archivo: ', claves)

    for claves, valores in dict_archivos_remoto.items():
        if claves not in dict_archivos_locales:
            print(claves)
            print(valores)
            request = obtener_servicio().files().get_media(fileId=valores[1])
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                print("Download %d%%." % int(status.progress() * 100))
            fh.seek(0)
            with open(os.path.join(basedir, claves), 'wb') as f:# Te guarda en la carpeta local
                f.write(fh.read())
                f.close()

