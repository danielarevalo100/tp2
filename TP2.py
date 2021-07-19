from service_gmail import obtener_servicio
from utils import * 
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
    service = obtener_servicio()

    messageInfo = service.users().messages().get(userId='me', id='17ab6106a4a03c07').execute()
    print(getEmailSubject(messageInfo))
    attachments = getAttachmentsIds(messageInfo['payload']['parts'])
    
    att = service.users().messages().attachments().get(userId='me', messageId='17ab6106a4a03c07', id=attachments[0]).execute()
    files = base64.urlsafe_b64decode(att['data'])
    
    z = zipfile.ZipFile(io.BytesIO(files))
    z.extractall()
    #fi = z.read(z.infolist()[0])
    print(fi)

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

def crear_carpetas():
    evaluacion = "Algebra II"
    os.mkdir(evaluacion)

    #carpeta de los docentes
    with open (r'direccion de docentes.csv', "r") as csv_file:
        for csv_file in csv_file.readlines():
            nombresDocentes = csv_file.split(',')
            os.mkdir((os.path,join(evaluacion,nombres[0])))
    with open(r'direccion de alumnos.csv', "r") as alumnos:
        for alumnos in alumnos.readlines():
        

main()
