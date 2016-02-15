# -*- coding: utf-8 -*-
import json

def freq_termino():
    data=[]
    count=1
    occurencesTotal=[]
    allChar = []
    #Opening and retrieving json data
    with open('tweets.txt') as f:
        for line in f:
            data.append(json.loads(line))    
    #Retrieving only 'text' data
    for items in data:
        try:
            words = items['text']
            occurencesTotal.append(words.encode('utf-8'))
            count+=1
        except:
            pass

    #Separating words    
    new_occurence="" 
    for items in occurencesTotal:
        for word in items:
            if word!=" " and word!="":
                new_occurence+=word
            else:
                if(new_occurence!=" ") and (new_occurence!=""):
                    allChar.append(new_occurence)
                    new_occurence=""
    #Creating and setting the Matrix
    item_index=0
    matrix = []
    matrix.append([])
    matrix.append([])
    #Inserting unique word and incrementing its frequency
    for item in allChar:
        if not(item) in matrix[0]:
            matrix[0].append((item))
            matrix[1].append(1.0)
        else:
            for item_m in matrix[0]:
                if item_m == item:
                    matrix[1][item_index]+=1.0
                    break
                else:
                    item_index+=1
        item_index=0
    #Calculating freq
    index=0   
    for item in matrix[1]:
        matrix[1][index]=round(matrix[1][index] / float(len(allChar)), 8)
        index+=1
    #Creating terminos.txt file and enabling write action    
    terminos = open("terminos.txt", "w")
    index=0
    for item in matrix[0]:
        try:
            terminos.write("%s : %s" % (str(item), matrix[1][index]))
            terminos.write("\n")
            index+=1
        except:
            pass
    print "Words and their frequency added to the terminos.txt file! [OK]"
    terminos.close()
    return ""
freq_termino()