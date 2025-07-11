import sys
import subprocess

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import re

#Get the result from scraper.py
#This assumes that scraper.py is in the same directory as this script
def getData():
    result = subprocess.check_output([sys.executable, 'scraper.py'], text=True)
    print(f"Scraped Price: {result}")  #Debugging line to see the raw output
    #Remove words before and around, just need the price i.e. From £50 becomes "50"
    match = re.search(r'(\d+)', result)
    if match:
        price = int(match.group(1))  #Convert the matched string to an integer

        if price < 200:
            #If the price is less than 200, add the £ back on and return it
            result = f'£{price}'
            return result
        else:
            #If the price is more than 200, return a message
            return 'null'

result = getData()

msg = MIMEText(result)

sender = 'scriptspython31@gmail.com'
recipient = 'josephe456@gmail.com'
password = 'cqot onil sjuc qjvd' #App Password for the sender email

def email_new(msg):
    message = MIMEMultipart()
    message['Subject'] = 'Tixel Ticket Price Update'
    message['From'] = sender
    message['To'] = recipient

    #Turn the message into HTML format
    html = MIMEText(f"<p><strong>Scraped Price:</strong> {msg}</p>", 'html')
    message.attach(html)

    #Send email
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender, password)
            server.send_message(message)
            print("Email sent successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")

#Check if the result is not 'null' before sending the email
if result != 'null':
    email_new(result)
else:
    print("Price is too high, no email sent.")






