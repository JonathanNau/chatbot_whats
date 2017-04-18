#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  6 19:21:10 2017

@author: jonathan
"""
## Lematizar Analise sematica

import csv
import re, math
from collections import Counter

WORD = re.compile(r'\w+')

def get_cosine(vec1, vec2):
     intersection = set(vec1.keys()) & set(vec2.keys())
     numerator = sum([vec1[x] * vec2[x] for x in intersection])

     sum1 = sum([vec1[x]**2 for x in vec1.keys()])
     sum2 = sum([vec2[x]**2 for x in vec2.keys()])
     denominator = math.sqrt(sum1) * math.sqrt(sum2)

     if not denominator:
        return 0.0
     else:
        return (float(numerator) / denominator)

def text_to_vector(text):
     words = WORD.findall(text)
     return (Counter(words))


read = csv.reader(open("bd.csv","r"))
a_split = []
for row in read :
    #print(row)
    a=[row[0],row[1]]
    a_split.append(a)

read = csv.reader(open("bd_t.csv","r"))
b_split = []
for row in read :
    #print(row)
    b=[row[0],row[1]]
    b_split.append(b)

#print(a_split)
def processa_pergunta(s):
    resposta='Não sei'
    value=0.0
    #similaridade    
    vector1 = text_to_vector(s)

    ## Saudações
    for i in range(len(b_split)):
        #print(a_split[i][0])
        if s.lower() == b_split[i][0].lower():
            return b_split[i][1]
    
    for i in range(len(a_split)):
        vector2 = text_to_vector(a_split[i][0])
        cosine = get_cosine(vector1, vector2)
        if cosine > 0.40 and cosine > value:
            value = cosine
            resposta = a_split[i][1]
            
    return resposta


s=''
while (s.lower() != 'tchau'):
    s = input()
    if s.lower() == 'tchau':
        break
    print(processa_pergunta(s))
print('Bye!!!!')