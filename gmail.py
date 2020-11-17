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


def get_emails(user_email):
    service = credentials()
    # Call the Gmail API
    #user_email = input("Enter your email:")

    
    emails = []

    def add_to_emails(request_id, response, exception):
      if exception is not None:
        # Do something with the exception
        pass
      else:
        emailresponse = []
        headers=response["payload"]["headers"]
        for d in headers:
            if d['name'] == 'From':
                emailresponse.append(d['value'])
            if d['name'] == 'Subject':
                emailresponse.append(d['value'])
        emailresponse.append(response.get('labelIds', []))
        emails.append(emailresponse)
        pass

    batch = service.new_batch_http_request()

    results = service.users().messages().list(userId='me', q=user_email).execute()
    messages = results.get('messages', [])

    for message in messages:
        mId = message.get("id")
        if user_email is None:
            batch.add(service.users().messages().get(userId="me", id=mId, format="full", metadataHeaders=None), callback=add_to_emails)
        else:
            batch.add(service.users().messages().get(userId="me", id=mId, format="full", metadataHeaders=None), callback=add_to_emails)
    batch.execute()
    return emails
