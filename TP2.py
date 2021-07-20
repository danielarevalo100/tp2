from utils import * 
from gmailUtils import *
import base64
import io 
import zipfile

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
            pass
        if opcion == 7:
            pass
        
        if opcion == 8:
            corte = True

    print('Hola')




main()
