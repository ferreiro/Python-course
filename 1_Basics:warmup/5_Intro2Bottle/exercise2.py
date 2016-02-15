import urllib.request
from bs4 import BeautifulSoup
import re

url = 'http://trenesytiempos.blogspot.com.es/'
html = urllib.request.urlopen(url).read()
sopa = BeautifulSoup(html, "html.parser")

keywords = []

while True:
    keywords.append(input("Enter the keywords you're searching for.\
     Enter 0 when you already entered all the search keywords\n"))
    if (keywords[-1]=="0"):
        del keywords[-1]
        break
    
#getting all the content urls
enlaces =sopa.find_all(href=re.compile("/201"),class_="post-count-link")
enlaceList= []
contentList = []

#saving all their contents
for enlace in enlaces:
    enlaceList.append(enlace['href'])
    content = urllib.request.urlopen(enlace['href']).read()
    sopa = BeautifulSoup(content, "html.parser")
    contentText = sopa.find("div", {"class":"post-body entry-content"})
    contentList.append(contentText.text.strip())
    
#Looking for the search keywords ocurrences in all blog articles
#List to store temp urls
occurrenceUrl = []

#going through all the keywords array, cleaning the occurrenceUrl list, 
#storing all the articles urls and displaying them
for kw in keywords:
    print (kw+ " : ")
    count = 0
    del occurrenceUrl[:]
    for text in contentList:
        if kw in text:
            occurrenceUrl.append(enlaceList[count])
        count = count + 1
    for url in occurrenceUrl:
        print (url)