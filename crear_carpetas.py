from service_gmail import obtener_servicio_gmail
from gmailUtils import *
import os
import zipfile

def obtener_y_descomprimir():
    # retornara el asunto del mail y descomprimira el archivo zip

    service = obtener_servicio_gmail()

    # por ahora lo se hizo con el ID del mail que tiene el comprimido, luego se implementara una busqueda con el nombre de la evaluacion
    messageInfo = buscarMailPorId(service, '17ae03031b9e0a12')
    attachments = obtenerIdsDeAdjuntos(messageInfo)

    att = service.users().messages().attachments().get(userId='me', messageId='17ab6106a4a03c07', id=attachments[0]).execute()
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

def list_alum(basedir):
    alumnos = []
    ruta_alumnos = os.path.join(basedir, 'alumnos.csv')
    with open(ruta_alumnos, 'r') as csv_file:
        for linea in csv_file.readlines():
            linea = linea.rstrip()
            list_alumnos = linea.split(',')
            alumnos.append(list_alumnos)


def list_alumdoc(basedir):
    ruta_alum_docentes = os.path.join(basedir, 'docalum.csv')
    docentes_alumnos = []
    with open(ruta_alum_docentes, "r") as csv_file1:
        for linea2 in csv_file1.readlines():
            linea2 = linea2.rstrip()
            list_alumdoc = linea2.split(',')
            docentes_alumnos.append(list_alumdoc)

def crear_carpetas():
    basedir = os.path.dirname(os.path.abspath(__file__))
    print(basedir)
    evaluacion= "Algebra"
    ruta_ev = os.path.join(basedir, evaluacion)
    os.mkdir(ruta_ev)
    if os.path.isdir(ruta_ev):
        print("La carpeta ya existe")
    for docente in docentes:
        os.mkdir((os.path.join(ruta_ev, docente[0])))
    for docentes_alumno in docentes_alumnos:
        for alumno in alumnos:
            if docentes_alumno[0] == docente[0] and docentes_alumno[1] == alumno[0]:
                os.mkdir((os.path.join(ruta_ev, docente[0], alumno[0]+" "+alumno[1])))

crear_carpetas()
