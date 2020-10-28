from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly',
          'https://www.googleapis.com/auth/gmail.labels']


def credentials():
    creds = None

    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)
    return service


def get_labels(service, mId, message):
    results = service.users().messages().get(userId="me", id=mId).execute()
    message['labelIds'] = (results.get('labelIds', []))

def find_specific_list(service, mId):
    messageheader= service.users().messages().get(userId="me", id=mId, format="full", metadataHeaders=None).execute()
    return messageheader

def find_email(service, user_email, mId, message):
    hasEmail = False
    messageheader = find_specific_list(service, mId)
    headers=messageheader["payload"]["headers"]
    email_from= [i['value'] for i in headers if i["name"]=="From"]
    sub= [i['value'] for i in headers if i["name"]=="Subject"]
    to_email = email_from[0]
    subject = sub[0]
    date = messageheader.get("internalDate")
    lists = []
    if user_email is not None:
        temp = to_email.find(user_email)
        if temp is not -1:
            hasEmail = True
            message['From'] = to_email
            message['Subject'] = subject
            message['Date'] = date
            get_labels(service, mId, message)

    else:
        message['From'] = to_email
        message['Subject'] = subject
        message['Date'] = date
        get_labels(service, mId, message)

    return hasEmail



def get_emails_all():
    service = credentials()
    results = service.users().messages().list(userId='me').execute()
    messages = results.get('messages', [])
    for message in messages:
        mId = message.get("id")
        find_email(service, None, mId, message)

    return messages


def get_emails_search(user_email):
    service = credentials()
    # Call the Gmail API
    #user_email = input("Enter your email:")

    results = service.users().messages().list(userId='me').execute()
    messages = results.get('messages', [])
    emails = []

    if not messages:
        print('No messages found.')
    else:
        print('Messages:')
        messagedict = []
        for message in messages:
            mId = message.get("id")
            hasEmail = find_email(service, user_email, mId, message)
            if(hasEmail):
                messagedict.append(message)

    return messagedict
