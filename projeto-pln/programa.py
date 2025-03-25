import nltk
import spacy

nlp = spacy.load("pt_core_news_sm")

from math import *
from nltk.tokenize import word_tokenize
from nltk import FreqDist
from nltk.corpus import stopwords

# |=================================================================================[ x ]==============================================================================================|
                                                                  # ESPAÇO PARA DOWNLOAD DE PACOTES E EXTRAS
# python -m spacy download pt_core_news_lg
# python -m spacy download pt_core_news_sm

# pip install -U pip setuptools wheel
# pip install -U spacy
# from spacy import displacy

nltk.download('punkt_tab') # Usado na tokenização
nltk.download('stopwords') # Módulo para stopwords
nltk.download('rslp') # Módulo para radicalizar
nltk.download('averaged_perceptron_tagger_eng')

# |=================================================================================[ x ]==============================================================================================|
                                                                    # FUNÇÃO QUE FAZ A LEITURA DO ARQUIVO .TXT

def leitura_arquivo(diretorio):
  '''
  A função irá ter como parâmetro o diretório do arquivo de entrada, depois ela faz a leitura do conteúdo do arquivo .txt
  '''

  with open (diretorio, 'r', encoding='UTF-8') as arquivo:
    texto = arquivo.read()

  return texto # --> retorna a variável "texto" com o contéudo salvo do arquivo

# |=================================================================================[ x ]==============================================================================================|  
                                                            # FUNÇÃO QUE FAZ O PRE-PROCESSAMENTO DO ARQUIVO .TXT

def lista_tokenizada(texto):
    '''
    Essa função serve para processar um texto. Em poucas palavras, a função vai ter como entrada um texto qualquer e a saída será uma lista com
    todas sentenças desse texto e cada sentença terá uma lista com seus respectivos "tokens" (que são as palavras da sentença). Importante
    lembrar que o conteudo da lista sentença não haverá pontuações, artigos, preposições, ... Enfim, as listas de sentenças não terão stopwords 
    e os tokens (palavras) estarão em minusculo.
    '''

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

    return sentencas_limpas # --> retorna a lista de setenças sem as stopswords e em lowercase

# |=================================================================================[ x ]==============================================================================================|
                                                            # FUNÇÃO QUE CALCULA O POTENCIA E A SOMA DO DENOMINADOR

def potencia_e_soma(vetor):
  '''
  Essa função servirá como auxiliadora. O objetivo dela é calcular o potencia e a soma de um vetor. Essa função será usada para facilitar o 
  cálculo do denonimador da fórmula do cosseno (que iremos ver em seguida).
  '''

  total = 0

  for indice in range (len(vetor)):
    total += vetor[indice] ** 2 # --> aqui ele irá calcular a potencia (2) do item do vetor[i] e somar com a variavel "total"

  return total # --> retorna a soma total da poencia de cada item no vetor

# |=================================================================================[ x ]==============================================================================================| 
                                                            # FUNÇÃO QUE CALCULA A SIMILARIDADE ENTRE DUAS SENTENÇAS

def similaridade (sentencas_limpas):
  '''
  Essa função é essencial para o funcionamento do projeto, pois calcula a similaridade entre sentenças consecutivas. Ela recebe uma lista de 
  sentenças já processadas (ou seja, tokenizadas, sem stopwords e normalizadas) e compara cada sentença com a próxima. 
  '''

  # LISTA COM TODAS AS SIMILARIDADES 
  lista_das_similaridades = []
  
  #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
  # ALGORITMO QUE IRÁ FAZER O CALCULO DO COSSENO
  
  for indice in range(len(sentencas_limpas)-1):

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

    #----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#    # APLICANDO A FÓRMULA DO COSSENO
    numerador = 0

    for i in range(len(uniao_sentencas)):
      numerador += vetor1[i] * vetor2[i] # --> aqui ele ira multiplicar o numero do vetor1 com outro numero do vetor2 nos mesmos indices e
                                         #     somar com a variavel "numerador"

    variavel_a = potencia_e_soma(vetor1) # --> calculando potencIa e soma para o denominador
    variavel_b = potencia_e_soma(vetor2)

    denominador = sqrt(variavel_a) * sqrt(variavel_b) # --> aqui vamos calcular o denominador 
                 
    # CALCULANDO A FORMULA FINAL
    cosseno = numerador / denominador if denominador != 0 else 0 # aqui garantimos que o denominador seja diferente de 0.

    #----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    # ADICIONANDO O RESULTADO DA SIMILARIDADE A LISTA
    lista_das_similaridades.append(cosseno)

  return lista_das_similaridades # --> retorna a lista de similaridades

# |=================================================================================[ x ]==============================================================================================|
                                                                # FUNÇÃO QUE CALCULA A MÉDIA DAS SIMILARIDADES


def media_similaridades(lista_das_similaridades):
    '''
    A função irá somar todas as similaridades e depois dividir pela quantidade de similaridades que tem na lista (média simples)
    '''

    soma_similaridades = 0
    quantidade_similaridades = len(lista_das_similaridades)

    for similaridade_entre_sentencas in lista_das_similaridades:
        soma_similaridades += similaridade_entre_sentencas

    media_similaridades = (soma_similaridades / quantidade_similaridades)

    return media_similaridades # --> retorna a média das similaridades

# |=================================================================================[ x ]==============================================================================================|
                                                    # FUNÇÃO QUE VAI CRIAR OS SUBTÓPICOS (SEGMENTAR O TEXTO EM SUBTÓPICOS)

def criar_subtopicos(texto, lista_similaridades, media_similaridade):
    '''
    Essa função tem o papel de segmentar o texto em subtópicos com base na similaridade entre as sentenças.
    '''

    # DIVIDE O TEXTO EM SENTENÇAS 
    sentencas = nltk.tokenize.sent_tokenize(texto) # --> aqui vamos dividir o texto em sentenças

    # INICIALIZAR AS LISTAS PARA ARMAZENAR OS SUBTÓPICOS
    sub_topicos = [] # --> aqui vamos guardar todos os subtópicos criados

    sub_topico_atual = [sentencas[0]] # --> lista temporária que armazena as sentenças do subtopicos 

    media = round(media_similaridade * 1.2, 4)  # --> podemos ajustar o valor conforme necessário para outros textos caso a media for muito baixa

    #----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

    # PERCORRE A LISTA DE SIMILARIDADES PARA CRIAR OS SUBTÓPICOS
    for indice in range(len(lista_similaridades)): # --> nesse for vamos analisar cada similaridade
        
        if lista_similaridades[indice] > media: # --> se a similaridade for maior que a media, entao a sentença é pertence ao subtopico atual
            sub_topico_atual.append(sentencas[indice + 1])

        else: # se for menor, o subtópico atual está pronto e precisa ser finalizado
            
            '''
            Aqui vamos verificar a quantidade de sentenças em "sub_topico_atual". O objetivo é evitar que um subtópico seja muito pequeno.
            '''

            if len(sub_topico_atual) >= 3:
                # se o subtópico atual tiver 3 ou mais sentenças, ele é adicionado à lista de subtópicos
                sub_topicos.append(sub_topico_atual)

            else: # se tiver menos de 3 sentenças, ele é mesclado com o último subtópico existente
                
                if sub_topicos: # --> verifica se a lista sub_topicos contem algum subtópico

                    # se tiver, mescla com o último subtópico
                    sub_topicos[-1].extend(sub_topico_atual) # --> aqui ele vai juntar o "sub_topico_atual" na ultima posição em "sub_topicos"

                else:
                    # se não houver subtópicos na lista, adiciona o "sub_topico_atual" como um novo sub_topicos
                    sub_topicos.append(sub_topico_atual)

            # inicia um novo subtópico com a próxima sentença
            sub_topico_atual = [sentencas[indice + 1]]

    #----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

    '''
    Após o loop, pode haver um subtópico atual que ainda não foi adicionado à lista. 
    Essa parte a baixo faz a mesma verificação do passo anterior para garantir que ele seja processado.
    '''

    # FINALIZA O ULTIMO SUBTOPICO (CASO ELE AINDA NÃO TENHA SIDO ADICIONADO)
    if sub_topico_atual:
        if len(sub_topico_atual) >= 3: # --> # garante que o rótulo tenha pelo menos 3 palavras
            # se o último subtópico tiver 3 ou mais sentenças, ele é adicionado a lista
            sub_topicos.append(sub_topico_atual)

        else:
            # se tiver menos de 3 sentenças, ele é mesclado com o último subtópico existente
            if sub_topicos:
                sub_topicos[-1].extend(sub_topico_atual)
            else:
                # se não houver subtópicos na lista, adiciona o subtópico atual como um novo
                sub_topicos.append(sub_topico_atual)

    return sub_topicos # --> retorna a lista com os subtópicos

# |=================================================================================[ x ]==============================================================================================|
                                                            # FUNÇÃO QUE VAI CRIAR OS RÓTULOS DE CADA SUBTÓPICOS

def criar_rotulos(lista_de_subtopicos):
    '''
    A função irá criar rótulos de cada subtópicos com base nas palavras mais frequentes (onde também conterá os substantivos e verbos)
    '''

    rotulos = []  # --> lista para armazenar os rótulos

    # LISTA DE PALAVRAS COMUNS QUE SERÃO FILTRADAS
    palavras_comuns = ["tem", "depende", "também", "para", "que", "é", "um", "uma", "na", "da", "do", "de", "e", "com", "como", "mais", 
                       "mas", "se", "ou", "ajuda", "desempenha"]

    # CONJUNTO PARA ARMAZENAR PALAVRAS JÁ USADAS EM RÓTULOS ANTERIORES
    palavras_ja_usadas = set() # --> evita que a mesma palavra seja usada como rótulo em mais de um subtópico.

    #----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

    # PERCORRE CADA SUBTÓPICO NA LISTA DE SUBTÓPICOS
    for subtopico in lista_de_subtopicos: 
        
        palavras_validas = [] # --> lista para armazenar substantivos, verbos, nomes próprios e adjetivos

        # PERCORRE CADA SENTENÇA DO SUBTÓPICO
        for sentenca in subtopico:

            doc = nlp(sentenca) # --> processa a sentença com spacy

            # PERCORRE CADA PALAVRA (TOKEN) NA SENTENÇA PROCESSADA
            for token in doc:

                # VERIFICA SE A PALAVRA É SUBSTANTIVO, VERBO, NOME PRÓPRIO OU ADJETIVO
                if token.pos_ in ["VERB", "ADJ", "PROPN", "NOUN"]:
                    palavra = token.lemma_.lower()  # --> usar a forma lematizada da palavra (ex: "correndo" -> "correr")
                    if palavra not in palavras_comuns and palavra not in palavras_ja_usadas:
                        palavras_validas.append(palavra)

        # CONTA A FREQUÊNCIA DAS PALAVRAS
        contagem = FreqDist(palavras_validas)

        # SELECIONA AS 5 PALAVRAS MAIS COMUNS
        palavras_e_frequencias = contagem.most_common(5) # --> pegar as 5 palavras mais frequentes com suas frequências

       # CRIA UMA LISTA APENAS COM AS PALAVRAS (IGNORANDO AS FREQUÊNCIAS)
        palavras_frequentes = []
        for palavra, frequencia in palavras_e_frequencias:
            palavras_frequentes.append(palavra)

        # ADICIONA AS PALAVRAS AO CONJUNTO DE PALAVRAS JÁ USADAS
        palavras_ja_usadas.update(palavras_frequentes)
        '''
        O ".update" adiciona varios elementos de uma lista a um conjunto. Ele garante que apenas elementos unicos sejam adicionados.
        '''

        # ADICIONA O RÓTULO A LISTA DE RÓTULOS 
        rotulos.append(palavras_frequentes)

    return rotulos  # --> retorna a lista com os rótulos de cada subtópico

# |=================================================================================[ x ]==============================================================================================|
                                                            # FUNÇÃO QUE TIRA AS ASPAS DOS ROTULOS DA LISTA DE ROTULOS
'''
Como a lista de rotulos estao nesse formato: ex: ["alimentação", "saúde", "fundamental", "bem-estar", "bom"], a função irá remover as aspas 
dos rótulos.
'''

def juntar_rotulos(rotulos):
    lista_rotulos_juntos = []

    for rotulo in rotulos:
        rotulo_sem_aspas = ', '.join(rotulo)
        lista_rotulos_juntos.append(rotulo_sem_aspas)
    
    return lista_rotulos_juntos # --> retorna a lista de rótulos, mas agora sem aspas

# |=================================================================================[ x ]==============================================================================================|
                                                                    # FUNÇÃO QUE VAI CRIAR O ARQUIVO DE SAIDA

def saida_arquivo(diretorio, sub_topicos, lista_rotulos_juntos):
    with open(diretorio, 'w', encoding='UTF-8') as arquivo:

        # VAI PERCORRER CADA SUBTÓPICO E SEU RESPECTIVO RÓTULO E ESCREVE NO ARQUIVO .TXT
        for i in range(len(sub_topicos)):
            
            # ESCREVE AS SENTENÇAS DO SUBTÓPICO
            for sentenca in sub_topicos[i]:
                arquivo.write(f"{sentenca}\n")
            
            # ESCREVE O RÓTULO DO SUBTÓPICO =
            arquivo.write(f"<tópico: {lista_rotulos_juntos[i]}>\n")
            
            # ADICIONA UMA LINHA EM BRANCO PARA SEPARAR OS SUBTÓPICOS 
            arquivo.write("\n")
        
# |=================================================================================[ x ]==============================================================================================|
                                                                            # APLICANDO AS FUNÇÕES 

texto = leitura_arquivo("projeto-pln/texto_entrada.txt")
resultado = lista_tokenizada(texto)


lista_similaridade = similaridade(resultado)
media_lista = media_similaridades(lista_similaridade)

lista_subtopicos = criar_subtopicos(texto, lista_similaridade, media_lista)
rotulos_gerados = criar_rotulos(lista_subtopicos)

lista_rotulos_juntos = juntar_rotulos(rotulos_gerados)

saida = saida_arquivo("projeto-pln/texto_saida.txt", lista_subtopicos, lista_rotulos_juntos)

print("ARQUIVO GERADO.")
# |=================================================================================[ x ]==============================================================================================|