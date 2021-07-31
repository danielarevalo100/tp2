from service_gmail import obtener_servicio_gmail
from gmailUtils import *
from utils import ingresar_opcion
import os
import zipfile


def obtener_y_descomprimir():
    # retornara el asunto del mail y descomprimira el archivo zip
    listamails = list()
    listaids = list()
    service = obtener_servicio_gmail()
    mails = service.users().messages().list(userId='me').execute()
    for mailid in mails['messages']:
        infomail = buscarMailPorId(service, mailid['id'])
        asunto = obtenerAsunto(infomail)
        listamails.append(asunto)
        listaids.append(mailid['id'])
    opcion = ingresar_opcion(listamails)
    mailid = listaids[opcion]

    # por ahora lo se hizo con el ID del mail que tiene el comprimido, luego se implementara una busqueda con el nombre de la evaluacion
    messageInfo = buscarMailPorId(service, mailid)
    attachments = obtenerIdsDeAdjuntos(messageInfo)

    att = service.users().messages().attachments().get(userId='me', messageId=mailid, id=attachments[0]).execute()
    files = base64.urlsafe_b64decode(att['data'])

    z = zipfile.ZipFile(io.BytesIO(files))
    z.extractall()
    return obtenerAsunto(messageInfo)

def list_doc(basedir):
    docentes = []
    ruta_docentes = os.path.join(basedir, 'docentes.csv')
    with open(ruta_docentes, "r") as csv_file:
        for linea in csv_file.readlines():
            linea = linea.rstrip()
            nombresDocentes = linea.split(',')
            docentes.append(nombresDocentes)

    return docentes

def list_alum(basedir):
    alumnos = []
    ruta_alumnos = os.path.join(basedir, 'alumnos.csv')
    with open(ruta_alumnos, 'r') as csv_file:
        for linea in csv_file.readlines():
            linea = linea.rstrip()
            list_alumnos = linea.split(',')
            alumnos.append(list_alumnos)
    return alumnos

def list_docalum(basedir):
    ruta_alum_docentes = os.path.join(basedir, 'docente-alumnos.csv')
    docentes_alumnos = []
    with open(ruta_alum_docentes, "r") as csv_file1:
        for linea2 in csv_file1.readlines():
            linea2 = linea2.rstrip()
            list_alumdoc = linea2.split(',')
            docentes_alumnos.append(list_alumdoc)
    return docentes_alumnos

def crear_carpetas(basedir):
    asunto = obtener_y_descomprimir()
    print(basedir)
    ruta_ev = os.path.join(basedir, asunto)
    os.mkdir(ruta_ev)
    if os.path.isdir(ruta_ev):
        print("La carpeta ya existe")

    for i in range(len(list_doc(basedir))):
        os.mkdir((os.path.join(ruta_ev, list_doc(basedir)[i][0])))
        for k in range (len(list_docalum(basedir))):
            for j in range(len(list_alum(basedir))):
                if list_docalum(basedir)[k][0] == list_doc(basedir)[i][0] and list_docalum(basedir)[k][1] == list_alum(basedir)[j][0]:
                    os.mkdir((os.path.join(ruta_ev, list_doc(basedir)[i][0], list_alum(basedir)[j][0] + " " + list_alum(basedir)[j][1])))
