# -*- coding: utf-8 -*-

import urllib
from bs4 import BeautifulSoup
import re
import os

url  = 'http://trenesytiempos.blogspot.com.es/'
html = urllib.request.urlopen(url).read()
sopa = BeautifulSoup(html, "html.parser")

#getting all the 2015 registers
enlaces = sopa.find_all(href=re.compile("/2015"),class_="post-count-link")

#filling the array with its values
dirList = []
enlaceList = []
countImg = 0

for enlace in enlaces:
    path = (enlace.text).strip()
    enlaceList.append(enlace['href'])
    #Formatting and creating all the directoties
    enlacewoHyphen = path.replace("-", " ")
    directory = enlacewoHyphen.replace("/", "-")
    dirList.append(directory)
    if not os.path.exists(directory):
        os.makedirs(directory)
    #scraping all the imgs urls in every enlace
    img = urllib.request.urlopen(enlace['href']).read()
    sopa = BeautifulSoup(img, "html.parser")
    all_images = sopa.find_all("img", border="0")
    #creating the image file in the current Directory 
    countImg = 0
    for imgs in all_images:
        imgFile = open(directory+'/img'+str(countImg)+'.jpg', 'wb')
        imgFile.write(urllib.request.urlopen(imgs['src']).read())
        countImg = countImg + 1
        imgFile.close()
