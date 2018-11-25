from django.shortcuts import render


import requests
import urllib2
# import http.client

from datetime import datetime

import urllib, urllib2
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

from emails import send_reset_link_html

# Mobilnext
sender_1 = "MSG91"
sender1_authkey = "ClkakoPSzQHhq1AqwwjNdQfxtEcMjI"
sender_id = "PTAAPP"

# SMTP Server - 1
server_1_hostname = "relay12.splitmx.com"
server_1_username = "splitmx12/ipac2"
server_1_password = "CS1B7AkRjNy1IKsMaXdpHeaM"
server_1_port = 25





def send_sms(number,message,sender = sender_1,promotional = False):
    if sender == sender_1:
        message = message.replace(" ", "+")
        if promotional:
            url = "https://mobilnxt.in/api/push?accesskey="+sender1_authkey+"&to="+number+"&text="+message+"&from="+ sender_id
        else:
            url = "https://mobilnxt.in/api/push?accesskey="+sender1_authkey+"&to="+number+"&text="+message+"&from="+ sender_id

        urllib2.urlopen(url)


# def send_email(from_mail,to_mail,server=server1,content=""):
#     return content


def send_mail(server="server2", subject=None,to_email=None,from_email=None,content=None,attachment1 = None,filename1 = "Attachment 1", attachment2= None, filename2 = "Attachment 2"):
        # toaddr = to_email
        msg = MIMEMultipart('mixed')
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject

        if attachment1:
            part1 = MIMEApplication(open(attachment1, 'rb').read())
            part1.add_header('Content-Disposition', 'attachment', filename=filename1)
            msg.attach(part1)

        if attachment2:
            part2 = MIMEApplication(open(attachment2, 'rb').read())
            part2.add_header('Content-Disposition', 'attachment', filename=filename2)
            msg.attach(part2)

        script = MIMEText(content, 'html')
        msg.attach(script)

        if server == "server1":
            server = smtplib.SMTP(server_1_hostname, server_1_port)
            server.starttls()
            server.login(server_1_username, server_1_password)
            text = msg.as_string()
            server.sendmail(server_1_username, to_email, text)
            server.quit()

def send_password_reset_email(name,email,secret_string):
    link = "https://www.careeranna.com/adminpanel/password/create/" + secret_string
    html_email = send_reset_link_html(name,link)
    send_mail(subject="Password Reset | CareerAnna TestEngine",to_email=email,from_email="reset@careeranna.com",content=html_email)    
