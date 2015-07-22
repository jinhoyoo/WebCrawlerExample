#-*- coding: utf-8 -*-

import urllib
from bs4 import BeautifulSoup



def getMailListFromWikiLeaksSearchURL( url ):
    html_doc = urllib.urlopen( url )

    soup = BeautifulSoup( html_doc, 'html.parser', from_encoding='utf-8')

    email_list = []
    for link in soup.find_all('a'):
        attribute = link.get('href')
        if None == attribute:
            continue
        if 0 <= attribute.find( "/hackingteam/emails/emailid/" ):
            email_list.append( attribute )

    return list(set(email_list))

if __name__ == "__main__":
    #Search URL with Korea and Devilangel
    #url = "https://wikileaks.org/hackingteam/emails?q=Korea+%7C+deviangel&mfrom=&mto=&title=&notitle=&date=&nofrom=&noto=&count=1000&sort=0#searchresult"

    url = "https://wikileaks.org/hackingteam/emails?q=Korea+%7C+deviangel&relid=0&title=&notitle=&date=&mailboxid=0&mailbox=&domainid=0&domain=&minrecipient=0&maxrecipient=0&file=&mto=&mfrom=&nofrom=&noto=&offset=2400"
    #      "https://wikileaks.org/hackingteam/emails?q=Korea+%7C+deviangel&relid=0&title=&notitle=&date=&mailboxid=0&mailbox=&domainid=0&domain=&minrecipient=0&maxrecipient=0&file=&mto=&mfrom=&nofrom=&noto=&offset=50"
    #      "https://wikileaks.org/hackingteam/emails?q=Korea+%7C+deviangel&relid=0&title=&notitle=&date=&mailboxid=0&mailbox=&domainid=0&domain=&minrecipient=0&maxrecipient=0&file=&mto=&mfrom=&nofrom=&noto=&offset=100"

    #email_list = getMailListFromWikiLeaksSearchURL(url)
    #print email_list
    #print len( email_list )

