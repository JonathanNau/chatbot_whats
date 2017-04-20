#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  6 19:21:10 2017

@author: jonathan
"""
import csv
import re
import math
from collections import Counter
from nltk.stem.snowball import SnowballStemmer

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
    Cria vetor de palavras
    '''
    words = WORD.findall(text)
    return Counter(words)


ARCHIVE = csv.reader(open("bd.csv", "r"), delimiter=';')
A_SPLIT = []
STEMMER = SnowballStemmer("portuguese")
for row in ARCHIVE:
    #print(row)
    a = [' '.join([STEMMER.stem(i) for i in row[0].split()]), row[1], row[2], row[3]]
    A_SPLIT.append(a)

def processa_pergunta(sentence, APARELHO):
    '''
    testar
    '''
    sentence = ' '.join([STEMMER.stem(i) for i in sentence.split()])
    resposta = 'Não sei'
    value_cosine = 0.0
    value_feedback = 0
    categoria = 'geral'
    vector1 = text_to_vector(sentence)
    cat = ['geral', 'conversa']+APARELHO
    for i in enumerate(A_SPLIT):
        if int(A_SPLIT[i[0]][3]) < 0 or A_SPLIT[i[0]][1].lower() not in cat:
            continue
        vector2 = text_to_vector(A_SPLIT[i[0]][0].lower())
        cosine = get_cosine(vector1, vector2)
        if cosine > 0.30 and cosine > value_cosine:
            value_cosine = cosine
            value_feedback = int(A_SPLIT[i[0]][3])
            resposta = A_SPLIT[i[0]][2]
            categoria = A_SPLIT[i[0]][1].lower()
        elif cosine > 0.0 and cosine == value_cosine and value_feedback < int(A_SPLIT[i[0]][3]):
            value_cosine = cosine
            value_feedback = int(A_SPLIT[i[0]][3])
            resposta = A_SPLIT[i[0]][2]
            categoria = A_SPLIT[i[0]][1].lower()
    if len(APARELHO) > 1 and categoria not in ['geral', 'conversa']:
        print('Encontramos uma resposta, mas precisamos confirmar seu aparelho')
        print('Por acaso seu aparelho é ' + categoria + '?')
        answer = input('User: ')
        if answer.lower() in ['s', 'sim', 'yes', 'y']:
            APARELHO.clear()
            APARELHO.append(categoria)
            return resposta
        else:
            APARELHO.remove(categoria)
            print(APARELHO)
            return processa_pergunta(sentence, APARELHO)
    else:
        return resposta

SENTENCES = []
APARELHO = ['android', 'iphone']
while True:
    SENTENCE = input('User: ')
    SENTENCES.append(SENTENCE)
    if SENTENCE.lower() == 'tchau':
        break
    elif SENTENCE.lower() == '*0':
        for i in enumerate(A_SPLIT):
            if A_SPLIT[i[0]][2] == SENTENCES[len(SENTENCES) - 2]:
                A_SPLIT[i[0]][3] = int(A_SPLIT[i[0]][3]) - 1
        print('Obrigado pelo Feedback!')
    elif SENTENCE.lower() == '*1':
        for i in enumerate(A_SPLIT):
            if A_SPLIT[i[0]][2] == SENTENCES[len(SENTENCES) - 2]:
                A_SPLIT[i[0]][3] = int(A_SPLIT[i[0]][3]) + 1
        print('Obrigado pelo Feedback!')
    elif SENTENCE.lower() in ['ajuda', 'versão']:
        print('Execução de comando')
    else:
        PROCESS = processa_pergunta(SENTENCE.lower(), APARELHO)
        SENTENCES.append(PROCESS)
        print(PROCESS)
print('Bye!!!!')
with open('bd.csv', 'w', newline='') as csvfile:
    WRITER = csv.writer(csvfile, delimiter=';')
    for j in enumerate(A_SPLIT):
        WRITER.writerow(A_SPLIT[j[0]])
