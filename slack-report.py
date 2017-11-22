#! /usr/bin/env python

import os
import sys
import requests
import subprocess
from datetime import date, timedelta

url = os.environ['SLACK_WEBHOOK_URL']

yesterday = date.today() - timedelta(1)
date_text = yesterday.strftime('%Y-%m-%d')

report = subprocess.check_output([sys.executable, 'report.py', date_text, date_text], universal_newlines = True)

payload = {
    'text': report,
    'channel': '#reports',
    'username': 'Toggl reports',
    'mrkdwn': True
}

r = requests.post(url, json = payload)
print(r)
print(r.text)
