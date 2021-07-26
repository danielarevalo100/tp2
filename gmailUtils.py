from service_gmail import obtener_servicio_gmail
from utils import * 
import base64
import io 
import zipfile
from email.mime.text import MIMEText

def buscarMailPorId(service, id):
    return service.users().messages().get(userId='me', id=id).execute()

def obtenerAsunto(data : dict = {}) -> str:
    headers = data['payload']['headers']
    subject =  find(lambda item, i: item['name'] == 'Subject', headers)
    if subject:
        return subject['value']
    return ''

def obtenerIdsDeAdjuntos(data : dict = {}):
    parts = data['payload']['parts']
    partsWithAttachments = list(filter(lambda item: 'attachmentId' in item['body'], parts))
    return list(map(lambda item: item['body']['attachmentId'] ,partsWithAttachments))

def enviarMail(service, address, text, subject):
    remitente = service.users().getProfile(userId='me').execute()
    message = MIMEText(text)
    message['to'] = address
    message['from'] = remitente['emailAddress']
    message['subject'] = subject
    body = {'raw': base64.urlsafe_b64encode(message.as_string().encode('UTF-8')).decode('ascii')}
    service.users().messages().send(userId='me', body=body).execute()

def buscarMailPorQuery(service, query): 
    return service.users().messages().list(userId='me', q=query).execute()

"""
messageInfo = getMailById(service, '17ab6106a4a03c07')
print(getEmailSubject(messageInfo))
attachments = getAttachmentsIds(messageInfo)

att = service.users().messages().attachments().get(userId='me', messageId='17ab6106a4a03c07', id=attachments[0]).execute()
files = base64.urlsafe_b64decode(att['data'])

z = zipfile.ZipFile(io.BytesIO(files))
z.extractall()
#fi = z.read(z.infolist()[0])
"""

