from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly',
          'https://www.googleapis.com/auth/gmail.labels']

#def make_label(name, mlv="show", llv = "labelShow"):
#    label = {
#        "messageListVisibility": mlv,
#        "labelListVisibility": llv,
#        "name": name
#    }

#    return label

def get_labels(service, mId):
    results = service.users().messages().get(userId="me", id=mId).execute()
    labels = results.get('labelIds', [])
    print("Labels:")
    for id in labels:
        print(id)

def find_email(service, user_email, mId):
    messageheader= service.users().messages().get(userId="me", id=mId, format="full", metadataHeaders=None).execute()
    # print(messageheader)
    headers=messageheader["payload"]["headers"]
    subject= [i['value'] for i in headers if i["name"]=="From"]
    to_email = subject[0]
    temp = to_email.find(user_email)
    if temp is not -1:
        return 1
    else:
        return 0





def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.


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

    # Call the Gmail API
    user_email = input("Enter your email:")
    '''
    message = service.users().messages().get(userId='me', id="17539e6a5bde42d8").execute()
    snippet = message.get("snippet")
    print("SNIPPET: " + snippet)
    payload = message.get("payload")
    headers = payload.get("headers", [])
    i = 0
    for h in headers:
        i = i+1
        if i is 8:
            value = h.get("value")
            temp = value.find("ncd2123@columbia.edu")
            if temp is not -1:
                print("FOUND")
            else:
                print("not found")
    '''


    results = service.users().messages().list(userId='me').execute()
    messages = results.get('messages', [])
    mIds = []

    if not messages:
        print('No messages found.')
    else:
        print('Messages:')
        for message in messages:
            mId = message.get("id")
            bool = find_email(service, user_email, mId)
            if bool is 1:
                print("Message:")
                print(message)
                get_labels(service, mId)

            #mIds.append(mId)

'''
    for messageId in mIds:
        results = service.users().messages().get(userId="me", id=messageId).execute()
        labels = results.get('labelIds', [])
        print("Labels:")
        for id in labels:
            print(id)
'''

    #snippet = results.get('snippet')

    #print("Snippet: " + snippet)


    #    print("label created")
    #except Exception as e:
    #    print(f"Error occured: {e}")

if __name__ == '__main__':
    main()
