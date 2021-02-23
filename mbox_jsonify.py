import requests
import os
import sys
import mailbox
import email
import quopri
import json


MBOX = sys.argv[1]
OUT_FILE = sys.argv[2]

def jsonifyMessage(msg):
    json_msg = {'parts': []}
    for (k, v) in msg.items():
        if type(v) != str:
            continue
        else:
            json_msg[k] = ""
    for (k, v) in msg.items():
        if type(v) != str:
            continue
        else:
            json_msg[k] += v

    for k in ['To', 'Cc', 'Bcc','Received']:
        if not json_msg.get(k):
            continue
        json_msg[k] = json_msg[k].replace('\n', '').replace('\t', '').replace('\r', '').replace(' ', '').split(',')

    try:
        for part in msg.walk():
            if part.get_content_type() == 'text/plain':
                content =part.get_payload()
                json_msg['text']=content
    except:
        sys.stderr.write('Skipping message - error encountered\n')
    finally:
        return json_msg

def gen_json_msgs(mb):
    li = []
    for msg in mbox:
        if msg is None:
            break
        li.append(jsonifyMessage(msg))
    return li
        
mbox = mailbox.mbox(MBOX)
with open(OUT_FILE, 'w') as f:
    json.dump(gen_json_msgs(mbox),f, indent=4)

