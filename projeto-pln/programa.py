import nltk
import spacy

nlp = spacy.load("pt_core_news_sm")

from math import *
from nltk.tokenize import word_tokenize
from nltk import FreqDist
from nltk.corpus import stopwords

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
                                                  # FUNÇÃO QUE FAZ A LEITURA DO ARQUIVO 

def leitura_arquivo(diretorio):
  with open (diretorio, 'r', encoding='UTF-8') as arquivo:
    texto = arquivo.read()

  return texto

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
 
  for indice in range(len(sentencas_limpas)-1): # 9

    # AQUI IRA CONCATENAR DUAS SENTENÇAS PARA POSTERIOR VERIFICAÇÃO DA FREQUENCIA 
    uniao_sentencas = list(set(sentencas_limpas[indice] + sentencas_limpas[indice+1]))

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
    numerador = sum(vetor1[i] * vetor2[i] for i in range(len(uniao_sentencas)))
    denominador = sqrt(potencia_e_soma(vetor1)) * sqrt(potencia_e_soma(vetor2))
                 
    # CALCULANDO A FORMULA FINAL
    cosseno = numerador / denominador if denominador != 0 else 0
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

  media_similaridades = (soma_similaridades / quantidade_similaridades)

  return media_similaridades

# |================================================================[ x ]====================================================================|
                                  # FUNÇÃO QUE VAI CRIAR OS SUBTÓPICOS (SEGMENTAR O TEXTO EM SUBTÓPICOS)
'''
Essa função tem o papel de segmentar o texto em subtópicos com base na similaridade entre as sentenças.
'''

def criar_subtopicos(texto, lista_similaridades, media_similaridade):
    sentencas = nltk.tokenize.sent_tokenize(texto)
    sub_topicos = []
    sub_topico_atual = [sentencas[0]]

    media = round(media_similaridade * 1.2, 4)  # Ajustar o valor conforme necessário

    for i in range(len(lista_similaridades)):
        if lista_similaridades[i] > media:
            sub_topico_atual.append(sentencas[i + 1])
        else:
            # Verifica se o subtópico atual tem pelo menos 3 sentenças
            if len(sub_topico_atual) >= 3:
                sub_topicos.append(sub_topico_atual)
            else:
                # Se não tiver, mescla com o próximo subtópico
                if sub_topicos:
                    sub_topicos[-1].extend(sub_topico_atual)
                else:
                    sub_topicos.append(sub_topico_atual)
            sub_topico_atual = [sentencas[i + 1]]

    if sub_topico_atual:
        if len(sub_topico_atual) >= 3: # --> # Garante que o rótulo tenha pelo menos 3 palavras
            sub_topicos.append(sub_topico_atual)
        else:
            if sub_topicos:
                sub_topicos[-1].extend(sub_topico_atual)
            else:
                sub_topicos.append(sub_topico_atual)

    return sub_topicos

# |================================================================[ x ]====================================================================|
                                          # FUNÇÃO QUE VAI CRIAR OS RÓTULOS DE CADA SUBTÓPICOS
'''
A função irá criar rótulos de cada subtópicos com base nas palavras mais frequentes (onde também conterá os substantivos e verbos)
'''

def criar_rotulos(lista_de_subtopicos):
    # Lista para armazenar os rótulos
    rotulos = []

    # Lista de palavras comuns que serão filtradas
    palavras_comuns = ["tem", "depende", "também", "para", "que", "é", "um", "uma", "na", "da", "do", "de", "e", "com", "como", "mais", "mas", "se", "ou", "ajuda", "desempenha"]

    # Conjunto para armazenar palavras já usadas em rótulos anteriores
    palavras_ja_usadas = set()

    for subtopico in lista_de_subtopicos:
        # Lista para armazenar substantivos, verbos, nomes próprios e adjetivos
        palavras_validas = []

        # Percorre cada sentença do subtópico
        for sentenca in subtopico:

            # Processa a sentença com spaCy
            doc = nlp(sentenca)
            for token in doc:

                # Verifica se a palavra é substantivo, verbo, nome próprio ou adjetivo
                if token.pos_ in ["VERB", "ADJ", "PROPN", "NOUN"]:
                    palavra = token.lemma_.lower()  # Usa a forma lematizada da palavra
                    if palavra not in palavras_comuns and palavra not in palavras_ja_usadas:
                        palavras_validas.append(palavra)

        # Conta a frequência das palavras
        contagem = FreqDist(palavras_validas)

        # Seleciona as 5 palavras mais comuns
        palavras_frequentes = [palavra for palavra, _ in contagem.most_common(5)]

        # Adiciona as palavras ao conjunto de palavras já usadas
        palavras_ja_usadas.update(palavras_frequentes)

        # Adiciona o rótulo à lista de rótulos
        rotulos.append(palavras_frequentes)

    return rotulos  # Retorna a lista com os rótulos de cada subtópico

# |================================================================[ x ]====================================================================|
                                            # FUNÇÃO QUE VAI JUNTAR AS SENTENÇAS DOS SUBTOPICOS

def juntar_subtopicos(sub_topicos):
    subtopicos_sentencas_unidas = []

    for subtopico in sub_topicos:
        juntar_sentencas = ' '.join(subtopico)
        subtopicos_sentencas_unidas.append(juntar_sentencas)
    
    return subtopicos_sentencas_unidas

# |================================================================[ x ]====================================================================|
                                        # FUNÇÃO QUE TIRA AS ASPAS DOS ROTULOS DA LISTA DE ROTULOS

def juntar_rotulos(rotulos):
    lista_rotulos_juntos = []

    for rotulo in rotulos:
        rotulo_sem_aspas = ', '.join(rotulo)
        lista_rotulos_juntos.append(rotulo_sem_aspas)
    
    return lista_rotulos_juntos

# |================================================================[ x ]====================================================================|
                                                # FUNÇÃO QUE VAI CRIAR O ARQUIVO DE SAIDA

def saida_arquivo(diretorio, sub_topicos, lista_rotulos_juntos):
    with open(diretorio, 'w', encoding='UTF-8') as arquivo:

        # Itera sobre cada subtópico e seu respectivo rótulo
        for i in range(len(sub_topicos)):
            
            # Escreve as sentenças do subtópico
            for sentenca in sub_topicos[i]:
                arquivo.write(f"{sentenca}\n")
            
            # Escreve o rótulo do subtópico
            arquivo.write(f"<tópico: {lista_rotulos_juntos[i]}>\n")
            
            # Adiciona uma linha em branco para separar os subtópicos
            arquivo.write("\n")
        
# |================================================================[ x ]====================================================================|
                                                          # APLICANDO AS FUNÇÕES 

texto = leitura_arquivo("/workspaces/Programacao_1/PROJETO_FINAL/projeto-pln/texto_entrada.txt")
resultado = lista_tokenizada(texto)


lista_similaridade = similaridade(resultado)
media_lista = media_similaridades(lista_similaridade)

lista_subtopicos = criar_subtopicos(texto, lista_similaridade, media_lista)
rotulos_gerados = criar_rotulos(lista_subtopicos)
lista_rotulos_juntos = juntar_rotulos(rotulos_gerados)

saida = saida_arquivo("/workspaces/Programacao_1/PROJETO_FINAL/projeto-pln/texto_saida.txt", lista_subtopicos, lista_rotulos_juntos)

print("ARQUIVO GERADO.")
# |================================================================[ x ]====================================================================|