#-*- coding: utf-8 -*-

import urllib
from bs4 import BeautifulSoup



def get_mail_list_from_wikileak_search_url(search_url):
    html_doc = urllib.urlopen(url)
    soup = BeautifulSoup( html_doc, 'html.parser', from_encoding='utf-8')

    email_list = []
    for link in soup.find_all('a'):
        attribute = link.get('href')
        if None == attribute:
            continue
        if 0 <= attribute.find( "/hackingteam/emails/emailid/" ):
            email_list.append( attribute )

    return list(set(email_list))

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



if __name__ == "__main__":

    # Search URL with Korea and Devilangel
    url = "https://wikileaks.org/hackingteam/emails?q=Korea+%7C+deviangel&mfrom=&mto=&title=&notitle=&date=&nofrom=&noto=&count=1000&sort=0#searchresult"

    # Estimated max result
    max_result = 2000

    # Extract e-mail list.
    search_url = extract_search_result_url(url)
    email_list = []

    f = open("email_list_temp.json", 'w')
    f.write( " { 'email_list' : [ ")

    for index in range(0, max_result+50, 50):
        url_to_extract_mails = "https://wikileaks.org/hackingteam/email"+search_url+str(index)
        print "Processing url: "+ url_to_extract_mails
        data = get_mail_list_from_wikileak_search_url( url_to_extract_mails )

        # To recognize process.
        print "Length of email list: "+str( len(data) )
        print data

        # Write data temporary.
        for elem in data:
            f.write( "'"+elem+"',\n")
            email_list.append(elem)


    f.write( "] }")
    f.close()

    print email_list

