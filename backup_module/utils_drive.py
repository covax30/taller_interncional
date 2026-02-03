import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Permisos para ver y subir archivos en Drive
SCOPES = ['https://www.googleapis.com/auth/drive.file']

def obtener_servicio_drive():
    creds = None
    # El archivo token.json se crea solo la primera vez que inicias sesión
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Aquí busca el archivo que descargaste de Google Cloud
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return build('drive', 'v3', credentials=creds)

def subir_archivo_a_drive(ruta_archivo):
    service = obtener_servicio_drive()
    nombre_archivo = os.path.basename(ruta_archivo)
    
    metadata = {'name': nombre_archivo}
    media = MediaFileUpload(ruta_archivo, resumable=True)
    
    file = service.files().create(body=metadata, media_body=media, fields='id').execute()
    return file.get('id')