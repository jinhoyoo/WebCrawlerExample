#-*- coding: utf-8 -*-

import urllib
from bs4 import BeautifulSoup


def get_mail_list_from_wikileak_search_url(search_url):
    soup2 = BeautifulSoup( urllib.urlopen(search_url), 'html.parser', from_encoding='utf-8')

    email_list = []
    for link in soup2.find_all('a'):
        attribute = link.get('href')
        if None == attribute:
            continue
        if 0 <= attribute.find("/hackingteam/emails/emailid/" ):
            email_list.append(attribute )

    email_list = get_mail_list( url, max_result )
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
    f.write( " { 'email_list' : [ ")


    email_list = []
    for index in range(0, max_result+50, 50):
        url_to_extract_mails = "https://wikileaks.org/hackingteam/emails"+search_url+str(index)
        print "Processing url: "+ url_to_extract_mails

        # Crawl e-mail lists.
        data = get_mail_list_from_wikileak_search_url(url_to_extract_mails)

        # To recognize process.
        print "Length of email list: "+str( len(data) )
        print data

        # Write data temporary.
        for elem in data:
            f.write( "'"+elem+"',\n")
            email_list.append(elem)

    f.write( "] }")
    f.close()

    # Filter out redundency mail list.
    filtered_email_list = list(set(email_list))

    #Save it in the file.
    f = open("email_list.json", 'w')
    f.write( " { 'email_list' : [ ")
    for elem in filtered_email_list:
        f.write( "'"+elem+"',\n")
    f.write( "] }")
    f.close()

    return filtered_email_list


if __name__ == "__main__":

    # Search URL with Korea and Devilangel
    url = "https://wikileaks.org/hackingteam/emails?q=Korea+%7C+deviangel&mfrom=&mto=&title=&notitle=&date=&nofrom=&noto=&count=1000&sort=0#searchresult"

    # Estimated max result
    max_result = 2000

    # get mail list from given search URL result.
    email_list = get_mail_list( url, max_result )

    print email_list


    """
    url_to_extract_mails = "https://wikileaks.org/hackingteam/emails?q=Korea+%7C+deviangel&relid=0&title=&notitle=&date=&mailboxid=0&mailbox=&domainid=0&domain=&minrecipient=0&maxrecipient=0&file=&mto=&mfrom=&nofrom=&noto=&offset=50"
    data = get_mail_list_from_wikileak_search_url(url_to_extract_mails)
    print data
    """
