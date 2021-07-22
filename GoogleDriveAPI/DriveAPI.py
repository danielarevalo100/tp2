from  __future__ import print_function

from quickstart import obtener_servicio
import shutil
import os
import io
from googleapiclient.http import MediaIoBaseDownload
import shutil
from os.path import isfile, join, isdir
from oauth2client import file, client, tools

def ingresar_opcion():
    menu = [
        '1)Listar archivos',
        '2)Crear un archivo',
        '3)Crear carpeta',
        '4)Subir un archvo',
        '5)Descargar archivo',
        '6)Salir'
    ]
    print("\n")
    for i in range(len(menu)):
        print(menu[i])
    opcion=input("Ingrese la opcion que desea realizar: ")
    while not (opcion.isnumeric() and int(opcion)> 0 and int(opcion)< 7):
        opcion= input("Debe ingresar un valor posible: ")
    opcion = int(opcion)
    return opcion

def recorrer_el_drive():
    '''
    pre:
    post: Le muestra todos los archivos y carpetas que hay en el drive
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
    # ARCHIVOS_A_SUBIR = ['nro_tramite.txt','photo.jpeg']
    #contenido = os.listdir(ruta_archivos_a_subir) #Te devuelve el contenido de la carpeta

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
            #Crea carpeta
            crear_carpeta()

        if opcion == 4:
            #Subir archivo(3.4)
            # Subir archivos especificos, tengo que hacer que el usuario elija cual quiere subir
            #crear una carpeta y que el usuario guarde los archivos que quiera subir
            subir_archivo()

        if opcion == 5:
            #Descargar archivo(3.5)
            descargar_archivo()

        if opcion == 6:
            corte = True

        opcion_corte = input('Desea volver al menu? (s|n) ')
        if opcion_corte != 's':
            corte = True

main()


# ruta_archivos_a_subir = 'Archivos_a_subir'

# for archivo in os.listdir(ruta_archivos_a_subir):
#     archivo = os.path.join(ruta_archivos_a_subir, archivo)
#     try:
#         if os.path.isfile(archivo):
#             os.unlink(archivo)        
#     except Exception as e:
#         print(e)

# print('Se limpio la carpeta')



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


# mover archivos en el drive

#     file_id = '***'
#     folder_id = '***'

#     # Retrieve the existing parents to remove
#     file = drive_service.files().get(fileId=file_id, fields='parents').execute()
#     previous_parents = ",".join(file.get('parents'))

#     # Move the file to the new folder
#     file = drive_service.files().update(
#         fileId=file_id,
#         addParents=folder_id,
#         removeParents=previous_parents,
#         fields='id, parents'
#     ).execute()