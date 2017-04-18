#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  6 19:21:10 2017

@author: jonathan
"""
## Lematizar Analise sematica

import csv
import re
import math
from collections import Counter

WORD = re.compile(r'\w+')

def get_cosine(vec1, vec2):
    '''
    Está funcão calcula a similaridade entre as frases
    '''
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])

    sum1 = sum([vec1[x]**2 for x in vec1.keys()])
    sum2 = sum([vec2[x]**2 for x in vec2.keys()])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator

def text_to_vector(text):
    '''
    Não sei ainda
    '''
    words = WORD.findall(text)
    return Counter(words)


ARCHIVE = csv.reader(open("bd.csv", "r"))
A_SPLIT = []
for row in ARCHIVE:
    #print(row)
    a = [row[0], row[1]]
    A_SPLIT.append(a)

ARCHIVE = csv.reader(open("bd_t.csv", "r"))
B_SPLIT = []
for row in ARCHIVE:
    #print(row)
    b = [row[0], row[1]]
    B_SPLIT.append(b)

#print(a_split)
def processa_pergunta(sentence):
    '''
    testar
    '''
    resposta = 'Não sei'
    value = 0.0
    vector1 = text_to_vector(sentence)

    ## Saudações
    for i in enumerate(B_SPLIT):
        #print(a_split[i][0])
        if sentence.lower() == B_SPLIT[i[0]][0].lower():
            return B_SPLIT[i[0]][1]
    for i in enumerate(A_SPLIT):
        vector2 = text_to_vector(A_SPLIT[i[0]][0])
        cosine = get_cosine(vector1, vector2)
        if cosine > 0.40 and cosine > value:
            value = cosine
            resposta = A_SPLIT[i[0]][1]
    return resposta

while True:
    SENTENCE = input()
    if SENTENCE.lower() == 'tchau':
        break
    print(processa_pergunta(SENTENCE))
print('Bye!!!!')
