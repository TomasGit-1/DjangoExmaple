from __future__ import print_function
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import base64
from email.message import EmailMessage
import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from email.mime.text import MIMEText
import json
class Gmail_API:
    path ="/home/tomy/Documentos/programming_excercises/DjangoExmaple/mysite/web/config/"
    credentials = 'key.json'
    token = "token.json"
    SCOPES = [  'https://www.googleapis.com/auth/gmail.readonly',
                'https://www.googleapis.com/auth/gmail.labels',
                'https://www.googleapis.com/auth/gmail.send',
                'https://www.googleapis.com/auth/gmail.compose',
                'https://www.googleapis.com/auth/gmail.insert',
                'https://www.googleapis.com/auth/gmail.modify',
                'https://www.googleapis.com/auth/gmail.metadata',
                'https://www.googleapis.com/auth/gmail.settings.basic',
                'https://www.googleapis.com/auth/gmail.settings.sharing',
                'https://mail.google.com/'
        ]
    creds = None

    def __init__(self):
        print("Inicia la carga del api")
        self.main()
        print("Finaliza la carga del api")
    
    def main(self):
        try:
            '''
            Creacion del token , talvez funcione para todos los servicios de google
            '''
            if os.path.exists(self.path + self.token):
                self.creds = Credentials.from_authorized_user_file(self.path + self.token ,  self.SCOPES)
            # If there are no (valid) credentials available, let the user log in.
            if not self.creds or not self.creds.valid:
                if self.creds and self.creds.expired and self.creds.refresh_token:
                    self.creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(self.path + self.credentials, self.SCOPES)
                    self.creds = flow.run_local_server()
                # Save the credentials for the next run
                with open(self.path + self.token, 'w') as token:
                    token.write(self.creds.to_json())
            '''
                Revisar igual y solo cambiar gmail , v1 por el servicio que necesitemos
            '''
            try:
                service = build('gmail', 'v1', credentials=self.creds)
                results = service.users().labels().list(userId='me').execute()
                labels = results.get('labels', [])
                if not labels:
                    print('No labels found.')
                    return
                print('Labels:')
                for label in labels:
                    print(label['name'])

            except HttpError as error:
                # TODO(developer) - Handle errors from gmail API.
                print(f'An error occurred: {error}')
            except Exception as e:
                print(str(e))
        except  Exception as e:
            return e


    def gmail_create_draft(self , data = []):
        try:
            # creds, _ = google.auth.default()
            try:
                # create gmail api client
                service = build('gmail', 'v1', credentials=self.creds)

                message = EmailMessage()
                # message = MIMEText('Hola Mund')

                message.set_content('This is automated draft mail')

                message['To'] = 'devtom19@gmail.com'
                message['From'] = 'tomaslopezperez107@gmail.com'
                message['Subject'] = 'Automated draft'

                encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
                
                create_message = {
                        'raw': encoded_message
                }
                # pylint: disable=E1101
                draft = service.users().drafts().create(userId="me",body=create_message).execute()

                print(F'Draft id: {draft["id"]}\nDraft message: {draft["message"]}')

            except HttpError as error:
                print(F'An error occurred: {error}')
                draft = None
            except Exception as e:
                return None
            return draft
        except Exception as e:
            return None

    
    def gmail_send_message(self):
        try:
            service = build('gmail', 'v1', credentials=self.creds)
            message = EmailMessage()
            message.set_content('This is automated draft mail')
            message['To'] = 'devtom19@gmail.com'
            message['From'] = 'tomaslopezperez107@gmail.com'
            message['Subject'] = 'Automated draft'
            # encoded message
            encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
            create_message = {
                'raw': encoded_message
            }
            # pylint: disable=E1101
            send_message = (service.users().messages().send(userId="me", body=create_message).execute())
            print(F'Message Id: {send_message["id"]}')
        except HttpError as error:
            print(F'An error occurred: {error}')
            send_message = None
        except Exception as e:
            return None
        return send_message
