import nltk
import spacy

nlp = spacy.load("pt_core_news_sm")

from math import *
from nltk.tokenize import word_tokenize
from nltk import FreqDist
from nltk.corpus import stopwords
from collections import Counter

# |================================================================[ x ]====================================================================|
                                                  # ESPAÇO PARA DOWNLOAD DE PACOTES E EXTRAS
# python -m spacy download pt_core_news_lg
# python -m spacy download pt_core_news_sm

# pip install -U pip setuptools wheel
# pip install -U spacy
# from spacy import displacy

# nltk.download('punkt_tab') # Usado na tokenização
# nltk.download('stopwords') # Módulo para stopwords
# nltk.download('rslp') # Módulo para radicalizar
# nltk.download('averaged_perceptron_tagger_eng')

# |================================================================[ x ]====================================================================|
                                                  # FAZENDO A LEITURA DO ARQUIVO .TXT

# with open ("Colab-2/texto2.txt", "r", encoding="UTF-8") as arquivo:
#   texto1 = arquivo.read()
  #print(texto1)

# with open ("Colab-2/mariele.txt", "r", encoding="UTF-8") as arquivo:
#   mariele_texto = arquivo.read()
  #print(texto2)

# abrir arquivo localmente:
with open ("2-Atividades_colab/Colab-2/texto_auxiliar.txt", "r", encoding="UTF-8") as arquivo:
   programacao = arquivo.read()

# abrir arquivo codespace:
# with open ("/workspaces/Programacao_1/PROJETO_FINAL/2-Atividades_colab/Colab-2/texto_auxiliar.txt") as arquivo:
#    programacao = arquivo.read()
  #print(programacao)

# |================================================================[ x ]====================================================================|  
                                            # FUNÇÃO QUE FAZ O PRE-PROCESSAMENTO DO ARQUIVO .TXT
'''
Essa função serve para processar um texto. Em poucas palavras, a função vai ter como entrada um texto qualquer e a saída será uma lista com
todas sentenças desse texto e cada sentença terá uma lista com seus respectivos "tokens" (que são as palavras da sentença). Importante
lembrar que o conteudo da lista sentença não haverá pontuações, artigos, preposições, ... Enfim, as listas de sentenças não terão stopwords 
e os tokens (palavras) estarão em minusculo.
'''

def lista_tokenizada(texto):
    
    # DIVIDINDO O TEXO EM SENTENCAS 
    sentencas = nltk.tokenize.sent_tokenize(texto)

    # NORMALIZANDO AS SENTENÇAS USANDO A FUNCÃO LOWER 
    sentencas_normalizadas = []

    for palavra in sentencas:
        minusculas = palavra.lower()
        sentencas_normalizadas.append(minusculas)

    # STOPWORDS
    stopwords = nltk.corpus.stopwords.words("portuguese")

    # REMOVENDO STOPWORDS E DEIXANDO OS TOKENS MINUSCULOS
    sentencas_limpas = [] 

    for sentenca in sentencas_normalizadas:
        tokens = word_tokenize(sentenca)

        token_limpo = []
        for palavra in tokens:
            if palavra not in stopwords and palavra.isalnum():
                token_limpo.append(palavra)
        sentencas_limpas.append(token_limpo)

    return sentencas_limpas # --> setenças sem as stopswords e em lowercase

#resultado1 = pre_processamento(texto1)

#resultado2 = pre_processamento(mariele_texto)

#print(resultado2)

# |================================================================[ x ]====================================================================|
                                            # FUNÇÃO QUE CALCULA O POTENCIA E A SOMA DO DENOMINADOR
'''
Essa função servirá como auxiliadora. O objetivo dela é calcular o potencia e a soma de um vetor. Essa função será usada para facilitar o 
cálculo do denonimador da fórmula do cosseno (que iremos ver em seguida).
'''

def potencia_e_soma(vetor):

  total = 0

  for i in range (len(vetor)):
    total += vetor[i] ** 2 # --> aqui ele irá calcular a potencia (2) do item do vetor[i] e somar com a variavel "total"

  return total # --> a soma total da poencia de cada item no vetor

# |================================================================[ x ]====================================================================|                        # FUNÇÃO QUE CALCULA A SIMILARIDADE ENTRE AS SENTENÇAS
                                           # FUNÇÃO QUE CALCULA A SIMILARIDADE ENTRE DUAS SENTENÇAS
'''
Essa função é essencial para o funcionamento do projeto, pois calcula a similaridade entre sentenças consecutivas. Ela recebe uma lista de 
sentenças já processadas (ou seja, tokenizadas, sem stopwords e normalizadas) e compara cada sentença com a próxima. 
'''

def similaridade (sentencas_limpas):
  
  # LISTA COM TODAS AS SIMILARIDADES 
  lista_das_similaridades = []
  
  # ALGORITMO QUE IRÁ FAZER O CALCULO DO COSSENO
  for indice in range(len(sentencas_limpas)-1):

    # AQUI IRA CONCATENAR DUAS SENTENÇAS PARA POSTERIOR VERIFICAÇÃO DA FREQUENCIA 
    uniao_sentencas = list(set(sentencas_limpas[indice] + sentencas_limpas[indice + 1]))

    # CRIAÇÃO DE DOIS VETORES (UM PARA CADA SENTENÇA)
    vetor1 = [0] * len(uniao_sentencas) # sentença 1
    vetor2 = [0] * len(uniao_sentencas) # sentença 2

    # PREENCHENDO OS VETORES
    for token in sentencas_limpas[indice]:
      vetor1[uniao_sentencas.index(token)] += 1

    # explicando o código acima:
    '''
    Estamos acessando cada token em "sentencas_limpas" percorrendo com o for. 
    Na repetição, o valor do token é "lorem" (exemplo) em "sentencas_limpas[0]".
    Depois que ele acessar o token "lorem", ele irá verificar em qual posição esse token ocupa na lista "uniao_sentencas".
    O token "lorem" ocupa a posição 2 (supondo) em "uniao_sentencas", dessa forma, será acrescentado 1 na mesma posição em 
    "vetor1" de zeros.
    '''

    for token in sentencas_limpas[indice + 1]:
      vetor2[uniao_sentencas.index(token)] += 1

  #-----------------------------------------------------------------------------------------------------------------------------------------#
    # APLICANDO A FÓRMULA DO COSSENO 
    numerador = 0

    for i in range(len(uniao_sentencas)):
      numerador += vetor1[i] * vetor2[i] # --> aqui ele ira multiplicar o numero do vetor1 com outro numero do vetor2 nos mesmos indices e
                                         #     somar com a variavel "numerador"

    variavel_a = potencia_e_soma(vetor1) # --> calculando potencIa e soma para o denominador
    variavel_b = potencia_e_soma(vetor2) 
    denominador = sqrt(variavel_a) * sqrt(variavel_b)
                 
    # CALCULANDO A FORMULA FINAL
    cosseno = numerador / denominador
  #-----------------------------------------------------------------------------------------------------------------------------------------#

    # ADICIONANDO O RESULTADO DA SIMILARIDADE A LISTA
    lista_das_similaridades.append(cosseno)

  return lista_das_similaridades

# |================================================================[ x ]====================================================================|
                                              # FUNÇÃO QUE CALCULA A MÉDIA DAS SIMILARIDADES
'''
A função irá somar todas as similaridades e depois dividir pela quantidade de similaridades que tem na lista (média simples)
'''

def media_similaridades(lista_das_similaridades):
  # achar a média entre as similaridades

  soma_similaridades = 0
  quantidade_similaridades = len(lista_das_similaridades)

  for similaridade_entre_sentencas in lista_das_similaridades:
    soma_similaridades += similaridade_entre_sentencas

  media_similaridades = (soma_similaridades / quantidade_similaridades) - 0.15

  return media_similaridades

# |================================================================[ x ]====================================================================|
                                  # FUNÇÃO QUE VAI CRIAR OS SUBTÓPICOS (SEGMENTAR O TEXTO EM SUBTÓPICOS)
'''
Essa função tem o papel de segmentar o texto em subtópicos com base na similaridade entre as sentenças.
'''

def criar_subtopicos(texto, lista_similaridades, media_similaridade):

  # DIVIDINDO O TEXTO EM SENTENÇAS COM NLTK
  sentencas = nltk.tokenize.sent_tokenize(texto)

  # CRIANDO A LISTA COM OS SUBTOPICOS
  sub_topicos = []

  # GRUPO DE SENTENÇAS SEMELHANTES
  sub_topico_atual = [sentencas[0]]

  # ARREDONDANDO A MEDIA
  media = round(media_similaridade, 4) 
  
  # PERCORRENDO A LISTA DE SIMILARIDADES
  for i in range(len(lista_similaridades)):

    # SE A SIMILARIDADE ENTRE DUAS SENTENÇAS FOR MAIOR QUE A MEDIA, ENTÃO ESTÃO NO MESMO GRUPO
    if lista_similaridades[i] > media:
      sub_topico_atual.append(sentencas[i + 1])
    
    # SE A SIMILARIDADE ENTRE DUAS SENTENÇAS FOR MENOR QUE A MEDIA, ENTÃO INICIA UM NOVO GRUPO
    if lista_similaridade[i] < media:
      sub_topicos.append(sub_topico_atual)
      sub_topico_atual = [sentencas[i + 1]]

  return sub_topicos

# |================================================================[ x ]====================================================================|
                                          # FUNÇÃO QUE VAI CRIAR OS RÓTULOS DE CADA SUBTÓPICOS
'''
A função irá criar rótulos de cada subtópicos com base nas palavras mais frequentes (onde também conterá os substantivos e verbos)
'''

def criar_rotulos(lista_de_subtopicos):

  # LISTA PARA ARMAZENAR OS RÓTULOS
  rotulos = []  

  for subtopico in lista_de_subtopicos:

    # LISTA PARA ARMAZENAR SUBSTANTIVOS, VERBOS, NOME PROPRIO E ADJETIVOS
    palavras_validas = []  

    # PERCORRE CADA SENTENÇA DO SUBTOPICO
    for sentenca in subtopico:
      
      # PROCESSA A SENTENÇA COM SPACY
      doc = nlp(sentenca)  
      for token in doc:

        # VERIFICA SE A PALAVRA É SUBSTANTIVO, VERBO, NOME PROPRIO OU ADJETIVO
        if token.pos_ in ["VERB", "ADJ", "PROPN", "NOUN"]:
          palavras_validas.append(token.text.lower())  # --> adiciona em minúsculas

    # CONTA A FREQUENCIA DAS PALAVRAS
    contagem = FreqDist(palavras_validas)

    # SELECIONA AS 5 PALAVRAS MAIS COMUNS
    palavras_frequentes = []

    for palavra, quantidade_wolrd in contagem.most_common(5):
       palavras_frequentes.append(palavra)

    # ADICIONA O RÓTULO À LISTA DE PALAVRAS FREQUENTES
    rotulos.append(palavras_frequentes)

  return rotulos  # Retorna a lista com os rótulos de cada subtópico

# |================================================================[ x ]====================================================================|

resultado3 = lista_tokenizada(programacao)
lista_similaridade = similaridade(resultado3)
media_lista = media_similaridades(lista_similaridade)

subtopicos = criar_subtopicos(programacao, lista_similaridade, media_lista)
#rotulos = criar_rotulos(subtopicos)
rotulos_gerados = criar_rotulos(subtopicos)

print("-" * 170)
print("PROCESSAMENTO: ")
print(resultado3)
print(len(resultado3))
# print(len(teste2))

print("-" * 170)
print("LISTA DAS SIMILARIDADES: ")
print(lista_similaridade)
#print(len(lista_similaridade))

print("-" * 170)
print("MEDIA DAS SIMILARIDADES: ")
print(media_lista)

print("-" * 170)
print("SUBTOPICOS: ")
print(subtopicos)

print("-" * 170)
print("ROTULOS EM CADA SUBTOPICOS: ")

# Exibir os rótulos de cada subtópico
for i, rotulo in enumerate(rotulos_gerados):
    print(f"Subtópico {i+1}: {rotulo}")
    
print("-" * 170)

# |================================================================[ x ]====================================================================|