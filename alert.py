import smtplib
from email.message import EmailMessage



def email_alert(body):
    
    user = 'tradevolatile@gmail.com'
    passcode = 'vlebpunrpspnnysj'
    subject = 'Trade volatile Account Details'
    reciever = 'nwaspecialg@gmail.com'
    
    msg = EmailMessage()
    msg.set_content(body)
    msg['subject'] = subject
    msg['to'] = reciever
    msg['from'] = user
    
        
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(user, passcode)
    server.send_message(msg)
    
    server.quit()
    

if "__name__ " == "__main__":
    email_alert('Testing New Mail')