# AMS-Task

# Task Description-

    •	setup a test gmail account and enable the APIs for it
    
    •	cover the following features:
      
        o	send emails
        
        o	search for specific messages in the mailbox, e.g. for keywords in subject or body text
    
    •	a brief documentation of your steps in terms what is needed to setup this API connection, PLEASE in your words not just copy &           paste from google

# Solution-

#### 1. Set up Test Gmail account – 
  
    Created a New Gmail account, Email – ‘test.ams102019@gmail.com’

#### 2.	Enable API for it-


      a.	After creating and logging into test account, went to  GMAIL- API, and followed the steps given here- 
  
      https://developers.google.com/gmail/api/quickstart/python?authuser=4
  
      b.	As per 1st step, clicked on “Enable the GMAIL API”, it downloads “credentials.json file”, which has client id and key and all       other necessary configuration. It should be kept in the working directory.
  
      c.	As of 2nd step install google client library-
  
      pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

      d.	Now, there is already a sample code available to connect to gmail to test the connection and it prints labels of the mailbox.       
      For the first run, it asks for authentication, opening a new tab in browser and after confirmation it saves the details for next         runs.

##### 3.	Sending mails -  

Google provides 2 kinds of approach to send emails,

 	a ) create a message and then send it . 
	b ) send it from drafts.
	
	Reference link - https://developers.google.com/gmail/api/guides/sending?authuser=4
	
For the task I used method A, creating a message and then sending it.
	
    •	Creating a message- 

    While creating message it has option to create message with attachment and without it, for the task I created without attachment.       For attachment it’s just requires additional step of uploading the attachment, which includes creating multi-part MIME message. 

    One can also create Drafts and save it rather than creating message and sending it.

For creating message with attachment and sending it-
https://developers.google.com/gmail/api/guides/sending

For drafts-
https://developers.google.com/gmail/api/guides/drafts



#### 4.	Search an email -

For searching a message in mail box, there are methods, message. List and thread. List. The message. List method accept parameter ‘q’ which supports advanced searches, searching based on subject, keyword, date ranges etc. 

 https://support.google.com/mail/answer/7190?authuser=4

For getting the messages matching the search criteria, list method is used for the task. This gives the id and threadID of the message.

response = service.users().messages().list(userId=user_id,q=query).execute()


To get more properties I passed the ID to another method “get” to get the message body,    which  supports various formats.

message = service.users().messages().get(userId=user_id,id=msg_id,format='raw').execute()

#### 5.	Exported the response to csv file 








