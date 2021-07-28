from os import path, listdir
from service_gmail import obtener_servicio_gmail
from gmailUtils import *
from utils import ingresar_opcion

def actualizar_entregas(basedir) :
    service = obtener_servicio_gmail()
    ruta_alumnos = path.join(basedir, 'alumnos.csv')

    #seleccion de que evaluacion se va a recibir
    directiorios = obtener_directorios(basedir)
    indiceEvaluacion = ingresar_opcion(directiorios)
    evaluacion = directiorios[indiceEvaluacion]
    rutaEvaluacion = path.join(basedir, evaluacion)

    with open(ruta_alumnos, "r") as alumnos:
        for alumno in alumnos:
            alumno = alumno.rstrip().split(',')
            print(alumno)
            #obtengo el id del mail del alumno con siendo el asunto su legajo y debe ser enviado desde su correo registrado en el .csv
            informacion = buscarMailPorQuery(service, f'subject:{alumno[1]} from:({alumno[2]})')
            if informacion['resultSizeEstimate'] > 0:
                idMail = informacion['messages'][0]['id']
                mail = buscarMailPorId(service, idMail)
                adjuntos = obtenerIdsDeAdjuntos(mail)
                if len(adjuntos) > 0:
                    att = service.users().messages().attachments().get(userId='me', messageId=idMail, id=adjuntos[0]).execute()
                    files = base64.urlsafe_b64decode(att['data'])
                    z = zipfile.ZipFile(io.BytesIO(files))
                    # el estudiante debe poner los archivos  {legajo} - nombre
                    nombresDeArchivos = z.namelist()
                    aux = f"{alumno[1]} - {alumno[0]}"
                    
                    error = False
                    for nombre in nombresDeArchivos:
                        if not aux in nombre:
                            error = True
                    if error:
                        enviarMail(service, alumno[2], 'Su entrega no tiene los nombres de archivos correctos', 'ERROR')
                    else:
                        print('todo buenisimo')


            else : 
                #enviarMail(service, alumno[2], 'No recibimos su entrega', 'ERROR')
                pass

def obtener_directorios(ruta):
    return [a for a in listdir(ruta) if path.isdir(path.join(ruta, a))]






