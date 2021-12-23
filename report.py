#! /usr/bin/env python

import os
import requests
import requests.packages.urllib3
from  more_itertools import unique_everseen
requests.packages.urllib3.disable_warnings()
import datetime
import math
import argparse
import sys
import time
parser = argparse.ArgumentParser()
parser.add_argument("start", help="The start date in YYYY-MM-DD format")
parser.add_argument("end", help="The end date in YYYY-MM-DD format")
args = parser.parse_args()

start = args.start
end = args.end


class Vividict(dict):
    def __missing__(self, key):
        value = self[key] = type(self)()
        return value

users =   Vividict()
auth = (os.environ['TOGGL_AUTH_KEY'], 'api_token')

headers = {'user-agent': 'report-generator'}
url = 'https://api.track.toggl.com/api/v8/v8/workspaces'
r = requests.get(url, auth=auth, headers=headers)
workspace_id = r.json()[0]['id']

url = 'https://api.track.toggl.com/reports/api/v2/details'

page = 1
total_pages = 1
while page <= total_pages:

    payload = { 'user_agent': 'report-generator', 'workspace_id': workspace_id, 'since': start, 'until': end, 'order_desc': 'off', 'order_field': 'date', 'page': page}
    r = requests.get(url, auth=auth, params=payload)
    details = r.json()

    if details['total_count'] > 50 and page == 1:
        print('Total records:', details['total_count'])
        total_pages =  math.ceil(details['total_count']/float(details['per_page']))
        print('Total pages:', total_pages)

    # print "Gathering data ..."

# put data in user-centric datastructure

    if 'error' in details:
        print('Error:', details['error']['message'])
        sys.exit(1)
    for d in details['data']:
        if len(users[d['user']]['clients'][d['client']]['projects'][d['project']]['tasks']) == 0:
                users[d['user']]['clients'][d['client']]['projects'][d['project']]['tasks'] = []
        users[d['user']]['clients'][d['client']]['projects'][d['project']]['tasks'].append(d)

    page +=1
    if details['total_count'] > 50 and page != total_pages:
        time.sleep(1)  # rate limiting of 1s for each request per toggl API docs

# looping through this whole thing just to sum the client total hours per User
for user in list(users.keys()):
    for client in list(users[user]['clients'].keys()):
        client_total = 0
        for project in list(users[user]['clients'][client]['projects'].keys()):
            project_total = 0
            for task in users[user]['clients'][client]['projects'][project]['tasks']:
                project_total = project_total + task['dur']
            client_total = client_total + project_total
            users[user]['clients'][client]['client_total'] = round(client_total/1000.0/3600.0, 1)

# loop through again to print hours
sorted_users = sorted(users.keys())
print('## Status report from', start, 'to', end)
for user in sorted_users:
    print('\n##',user)
    for client in list(users[user]['clients'].keys()):
        print('\n### Client:', client, '--',  str(users[user]['clients'][client]['client_total']) + 'h')
        for project in list(users[user]['clients'][client]['projects'].keys()):
            print('\n#### Project:', project)
            t_tasks = []
            for task in users[user]['clients'][client]['projects'][project]['tasks']:
                duration = round(task['dur']/1000.0/3600.0, 1)
                t_tasks.append(task['description'] + ' ' + str(duration) + 'h')
                #project_total = project_total + task['dur']
            for task in list(unique_everseen(t_tasks)):
                print('*', task)
