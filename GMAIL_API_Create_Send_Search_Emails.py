
# coding: utf-8

# In[26]:


#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from email.mime.text import MIMEText
import base64
from apiclient import errors
import pandas as pd

# Defining the scope, although it should be narrowed down, but I used full access for this task

SCOPES = ['https://mail.google.com/']


def get_creds():
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
            flow =                 InstalledAppFlow.from_client_secrets_file('credentials.json'
                    , SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run

        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    # Bulding the service

    service = build('gmail', 'v1', credentials=creds)
    return service


def create_message(
    sender,
    to,
    subject,
    message_text,
    ):
    """
    Create a message for an email. Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.

  Returns:
    An object containing a base64url encoded email object.
  """

    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    return {'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode()}


def send_message(service, user_id, message):
    """Send an email message.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    message: Message to be sent.

  Returns:
    Sent Message.
  """

    try:
        message = service.users().messages().send(userId=user_id,
                body=message).execute()

        # print('Message Id: %s' % message['id'])

        return message
    except errors.HttpError as error:

    # I would rather log all the errors in staging table or in a file, though it depends on error handling method used

        print('An error occurred: %s' % error)


def ListMessagesMatchingQuery(service, user_id, query=''):
    """List all Messages of the user's mailbox matching the query.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    query: String used to filter messages returned.
    Eg.- 'from:user@some_domain.com' for Messages from a particular sender.

  Returns:
    List of Messages that match the criteria of the query. Note that the
    returned list contains Message IDs, you must use get with the
    appropriate ID to get the details of a Message.
  """

    try:
        response = service.users().messages().list(userId=user_id,
                q=query).execute()
        messages = []
        if 'messages' in response:
            messages.extend(response['messages'])

        while 'nextPageToken' in response:
            page_token = response['nextPageToken']
            response = service.users().messages().list(userId=user_id,
                    q=query, pageToken=page_token).execute()
            messages.extend(response['messages'])

        return messages
    except errors.HttpError as error:

    # Again ,depends on error handling method, its a print command for this task

        print('An error occurred: %s' % error)


def GetMimeMessage(service, user_id, msg_id):
    """Get a Message and use it to create a MIME Message.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    msg_id: The ID of the Message required.

  Returns:
    A MIME Message, consisting of data from Message.
....
....The format can vary there are many as full, 
...."full": Returns the full email message data with body 
....content parsed in the payload field; the raw field is not used. (default)
  """

    try:
        f_m = service.users().messages().get(userId=user_id, id=msg_id,
                format='full').execute()

        # msg_str = base64.urlsafe_b64decode(message['full'].encode('ASCII'))

        # mime_msg = email.message_from_string(msg_str)

        return f_m
    except errors.HttpError as error:

    # Again, depends on error handling method

        print('An error occurred: %s' % error)


if __name__ == '__main__':

    # Calling to connect and authorize GMAIL API

    creds = get_creds()

    # Call to create a message with parameters, parameters can be read from a file also

    the_message = create_message('test.ams102019@gmail.com',
                                 'bhardwaj.priyamvada30@gmail.com',
                                 'final test',
                                 'final test before commenting')

    # Call to send the message created above, again parameters can be read from a file

    send_message(creds, 'test.ams102019@gmail.com', the_message)

    matching_message = ListMessagesMatchingQuery(creds,
            'test.ams102019@gmail.com', query='ams')

df = pd.DataFrame()
for i in matching_message:
    full_m = GetMimeMessage(creds, 'test.ams102019@gmail.com', i['id'])
    dict_new = dict(full_m)
    df = df.append(dict_new, ignore_index=True)

    # Exporting to CSV, File name can be parametrized

df.to_csv('out0910.csv')

