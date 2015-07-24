#-*- coding: utf-8 -*-

import json
import urllib
import goslate
import os
import wikileaks_crawling_hackingteam as wc

from bs4 import BeautifulSoup

g_main_uri = "https://wikileaks.org"

# Read e-mail list to dump.
f = open("email_list.json", 'r')
email_list_data = json.load(f)
f.close()

email_list = email_list_data['email_list']

print email_list

# Parse e-mails and dump them in folder.
if not os.path.exists('mails'):
    os.makedirs('mails')

for elem in email_list:
    email_url = g_main_uri+ elem
    print 'Parsing e-mail:'+ email_url
    contents = wc.write_mail_contents_in_JSON(email_url)

    # Save it as JSON file
    file_name = contents["email-id"]+".json"
    f = open("mails/"+file_name, 'w')
    f.write( json.dumps( contents ) )
    f.close()
