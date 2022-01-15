import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText



def send_annonces(receiver_email ,mail_content):
    #The mail addresses and password
    sender_address = '159mera@gmail.com'
    sender_pass = 'ne9la100'
    receiver_address =receiver_email
    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'les annones  de  votre ville .'   #The subject line
    #The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'plain'))
    #Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
    session.starttls() #enable security
    session.login(sender_address, sender_pass) #login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    print('Mail Sent')