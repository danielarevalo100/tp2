from os import path
from service_gmail import obtener_servicio_gmail
from gmailUtils import *

def actualizar_entregas(basedir) :
    service = obtener_servicio_gmail()
    ruta_alumnos = path.join(basedir, 'alumnos.csv')
    with open(ruta_alumnos, "r") as alumnos:
        for alumno in alumnos:
            alumno = alumno.rstrip().split(',')
            #obtengo el id del mail del alumno con siendo el asunto su legajo y debe ser enviado desde su correo registrado en el .csv
            informacion = buscarMailPorQuery(service, f'subject:{alumno[1]} from:({alumno[2]})')
            if informacion['resultSizeEstimate'] > 1:
                idMail = informacion['messages'][0]['id']
            else : 
                enviarMail(service, alumno[2], 'No recibimos su entrega', 'ERROR')








