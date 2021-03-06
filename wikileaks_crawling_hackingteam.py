#-*- coding: utf-8 -*-

import json
import urllib
import goslate
import os
import HTMLParser

from bs4 import BeautifulSoup

g_main_uri = "https://wikileaks.org"

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
        url_to_extract_mails = g_main_uri+"/hackingteam/emails"+search_url+str(index)
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


def write_mail_contents_in_JSON(url):
    html_doc = urllib.urlopen(url)
    soup = BeautifulSoup(html_doc,
                         'html.parser',
                         from_encoding='utf-8'
                         )

    mail_data = {}

    # Parse e-mail info table.
    table_data = soup.table.find_all('td')

    mail_data["email-id"] =table_data[0].get_text()
    mail_data["date"] = table_data[1].get_text()
    mail_data["from"] = table_data[2].get_text()
    mail_data["to"] = table_data[3].get_text()

    # Get contents in Italian.
    contents = soup.find("div", {"id": "uniquer"}).get_text().encode("ascii", "ignore").replace("\n", ' ')
    contents = contents.replace("."," ").replace(","," ").replace("'"," ").replace("\""," ").replace("\\"," ")

    # Remove mail signature.
    sig1 = "This message is a PRIVATE communication. This message contains privileged and confidential information intended only for the use of the addressee(s)."
    sig2 = "If you are not the intended recipient, you are hereby notified that any dissemination, disclosure, copying, distribution or use of the information contained in this message is strictly prohibited. If you received this email in error or without authorization, please notify the sender of the delivery error by replying to this message, and then delete it from your system."
    sig3 = "The information contained in this e-mail message is confidential and intended only for the use of the individual or entity named above.If you are not the intended recipient, please notify us immediately by telephone or e-mail and destroy this communication. Due to the way of the transmission, we do not undertake any liability with respect to the secrecy and confidentiality of the information contained in this e-mail message"
    sig4="Best regards"

    filted_contents = contents.replace(sig1, " ").replace(sig2, " ").replace(sig3, " ").replace(sig4, " ")

    # Convert unicode to common text.
    h = HTMLParser.HTMLParser()
    mail_data["contents_it"] = h.unescape(filted_contents)


    # Translate in English
    gs = goslate.Goslate()
    mail_data["contents_en"] = gs.translate(mail_data["contents_it"], "en" )

    return mail_data


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

    # Parse e-mails and dump them in folder.
    if not os.path.exists('mails'):
        os.makedirs('mails')

    for elem in email_list:
        email_url = g_main_uri+ elem
        print 'Parsing e-mail:'+ email_url
        contents = write_mail_contents_in_JSON(email_url)

        # Save it as JSON file
        file_name = contents["email-id"]+".json"
        f = open("mails/"+file_name, 'w')
        f.write( json.dumps( contents ) )
        f.close()


if __name__ == "__main__":
    main_proc()
