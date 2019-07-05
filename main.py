#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  6 19:21:10 2017

@author: jonathan
"""
import csv
import re
import math
from respostasModel import respostasModel
from collections import Counter
from nltk.stem.snowball import SnowballStemmer
from subprocess import check_output

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
grupoDeRespostas = []
STEMMER = SnowballStemmer("portuguese")

for row in ARCHIVE:
    #print(row)
    resposta = respostasModel(' '.join([STEMMER.stem(i) for i in row[0].split()]), row[1], row[2], row[3])
    grupoDeRespostas.append(resposta)

def processa_pergunta(sentence, APARELHO):
    '''
    '''
    sentence = ' '.join([STEMMER.stem(i) for i in sentence.split()])
    respostaParaUsuario = 'Não sei'
    value_cosine = 0.0
    maiorValorDeFeedback = 0
    categoria = 'geral'
    vector1 = text_to_vector(sentence)
    categorias = ['geral', 'conversa', 'comando', 'iphone', 'android']
    
    for resposta in grupoDeRespostas:
        if int(resposta.feedback) < 0 or resposta.categoria.lower() not in categorias:
            continue
        vector2 = text_to_vector(resposta.questao.lower())
        cosine = get_cosine(vector1, vector2)
        if cosine > 0.30 and cosine > value_cosine:
            value_cosine = cosine
            maiorValorDeFeedback = resposta.feedback
            respostaParaUsuario = resposta.resposta
            categoria = str(resposta.categoria).lower()
        elif cosine > 0.0 and cosine == value_cosine and maiorValorDeFeedback < resposta.feedback:
            value_cosine = cosine
            maiorValorDeFeedback = resposta.feedback
            respostaParaUsuario = resposta.resposta
            categoria = str(resposta.categoria).lower()
    
    if len(APARELHO) == 0 and categoria not in ['geral', 'conversa', 'comando']:
        respostaParaUsuario = 'Encontramos uma resposta, mas precisamos confirmar seu aparelho. Por acaso seu aparelho é ' + categoria + '?'
        categoriaCelular = categoria 
        return respostaParaUsuario
    else:
        if categoria == 'comando':
            return check_output(respostaParaUsuario, shell=True).decode("utf-8").rstrip()
        else:
            return respostaParaUsuario

categoriaCelular = ''
SENTENCES = []
APARELHO = []
def getResposta(SENTENCE):
    SENTENCES.append(SENTENCE)
    if SENTENCE.lower() in ['s','sim', 'y', 'yes']:
        APARELHO.append(categoriaCelular)
        SENTENCE = SENTENCES[-3]

    if SENTENCE.lower() == '*0':
        for resposta in grupoDeRespostas:
            if resposta.resposta == SENTENCES[len(SENTENCES) - 2]:
                resposta.feedback = resposta.feedback - 1
        return 'Obrigado pelo Feedback!'
    elif SENTENCE.lower() == '*1':
        for resposta in grupoDeRespostas:
            if resposta.resposta == SENTENCES[len(SENTENCES) - 2]:
                resposta.feedback = resposta.feedback + 1
        return 'Obrigado pelo Feedback!'
    elif SENTENCE.lower() in ['ajuda', 'versão']:
        return 'Execução de comando'
    else:
        PROCESS = processa_pergunta(SENTENCE.lower(), APARELHO)
        SENTENCES.append(PROCESS)
        return PROCESS


