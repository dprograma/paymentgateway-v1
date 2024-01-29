import smtplib
import random
import string
import jwt
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.http import JsonResponse

def mailHTMLTemplate(name, code):
    return f'''
    # Your HTML content here (same as your Node.js code)
    # Replace {name} and {code} with {name} and {code}
    '''

def sendMail(email, subject, body, name, code):
    try:
        # Create the SMTP object
        server = smtplib.SMTP('mail.hollajobs.com', 465)
        server.starttls()

        # Login Credentials
        server.login('no-reply@hollajobs.com', 'mypass#@12holla')

        msg = MIMEMultipart()
        msg['From'] = 'no-reply@hollajobs.com'
        msg['To'] = email
        msg['Subject'] = subject

        msg.attach(MIMEText(mailHTMLTemplate(name, code), 'html'))

        server.sendmail('no-reply@hollajobs.com', email, msg.as_string())
        server.quit()

        return {"info": "Mail sent"}
    except Exception as e:
        return {"error": str(e)}

def generateToken(len):
    chars = string.ascii_letters + string.digits + '-'
    return ''.join(random.choice(chars) for _ in range(len))

def getInputValueString(inputObj, field):
    return inputObj.get(field, '').strip() if isinstance(inputObj, dict) else ''

def getInputValueObject(inputObj, field):
    return inputObj.get(field, '') if isinstance(inputObj, dict) and isinstance(inputObj.get(field), dict) else {}

def getInputValueArray(inputObj, field):
    return inputObj.get(field, []) if isinstance(inputObj, dict) and isinstance(inputObj.get(field), list) else []

def calculateQueryStartIndex(page):
    page = int(page) if page and int(page) > 1 else 1
    return (page - 1) * 50  # pagination

signInJWTSecret = "HOLLA@2021#Increase@made#this.secret"


def outputError(response, code, message):
    data = {}
    data['code'] = code if code else 200
    data['error'] = message if message else 'Unknown error'
    
    return JsonResponse(data, status=code)
