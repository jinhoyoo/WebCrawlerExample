#-*- coding: utf-8 -*-

import json
import urllib
from bs4 import BeautifulSoup

g_main_uri = "https://wikileaks.org/hackingteam/emails"

def get_mail_list_from_wikileak_search_url(search_url):
    soup2 = BeautifulSoup( urllib.urlopen(search_url), 'html.parser', from_encoding='utf-8')

    email_list = []
    for link in soup2.find_all('a'):
        attribute = link.get('href')
        if None == attribute:
            continue
        if 0 <= attribute.find("/hackingteam/emails/emailid/" ):
            email_list.append(attribute )

    # Filter out redundency mail list.
    filtered_email_list = list(set(email_list))
    return email_list


def extract_search_result_url(url):
    html_doc = urllib.urlopen(url)
    soup = BeautifulSoup(html_doc, 'html.parser', from_encoding='utf-8')

    search_url_all=""
    for link in soup.find_all('a'):
        attribute = link.get('href')
        if None == attribute:
            continue
        if 0 <= attribute.find( "&offset=" ):
            search_url_all=attribute
            break

    index = search_url_all.rfind("&offset=")
    index_offset_number = index + len( "&offset=")
    return search_url_all[0:index_offset_number]


def get_mail_list( url, max_result):
    search_url = extract_search_result_url(url)

    f = open("email_list_temp.json", 'w')
    f.write( " { \"email_list\" : [ ")

    email_list = []
    for index in range(0, max_result+50, 50):
        url_to_extract_mails = g_main_uri +search_url+str(index)
        print "Processing url: "+ url_to_extract_mails

        # Crawl e-mail lists.
        data = get_mail_list_from_wikileak_search_url(url_to_extract_mails)

        # To recognize process.
        print "Length of email list: "+str( len(data) )
        print data

        # Write data temporary.
        for elem in data:
            f.write( "\""+elem+"\",\n")
            email_list.append(elem)

    f.write( "] }")
    f.close()

    # Filter out redundancy mail list.
    filtered_email_list = list(set(email_list))

    return filtered_email_list


def main_proc():
    # Search URL with Korea and Devilangel
    search_url = "https://wikileaks.org/hackingteam/emails?q=Korea+%7C+deviangel&mfrom=&mto=&title=&notitle=&date=&nofrom=&noto=&count=1000&sort=0#searchresult"

    # Estimated max result
    max_result = 2000

    # Get mail list from given search URL result.
    email_list = get_mail_list( search_url, max_result )

    # Save it as JSON file
    data = {'email_list':email_list,
            'queried_url':search_url}
    f = open("email_list.json", 'w')
    f.write( json.dumps(data) )
    f.close()

    print email_list


if __name__ == "__main__":
    main_proc()





