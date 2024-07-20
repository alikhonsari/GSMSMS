#!/usr/bin/env python3

import os
import sys
import requests

def send_to_telegram(message):
    
    apiToken = 'TELEGRAM_API_TOKEN'
    chatID = 'TELEGRAM_CHAT_ID'
    apiURL = f'https://api.telegram.org/bot{apiToken}/sendMessage'

    try:
        response = requests.post(apiURL, json={'chat_id': chatID, 'text': message})
        print(response.text)
    except Exception as e:
        print(e)

numparts = int(os.environ["DECODED_PARTS"])
phone = "phone-number" #"replace it with the phone number of simcard"
sender = str(os.environ["SMS_1_NUMBER"])

sms_text = ""

if numparts == 0:
    sms_text = os.environ["SMS_1_TEXT"]
else:
    for i in range(1, numparts + 1):
        varname = "DECODED_%d_TEXT" % i
        if varname in os.environ:
            sms_text = sms_text + os.environ[varname]

sms_text = """from: {2}

{1}

(line: {0})
""".format(phone, sms_text, sender)
send_to_telegram(sms_text)
