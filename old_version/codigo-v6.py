import nltk
import spacy

nltk.download('stopwords')
nltk.download('punkt_tab')

from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.probability import FreqDist
from nltk.corpus import stopwords
from math import sqrt

nlp = spacy.load("pt_core_news_lg")

# |================================================================[ x ]====================================================================|
                                                              # LEIA RICCARDO
# Fala, mano! De boas? 

# Dei uma olhada no código (a última celula que tu colocou no colab) e fui reescrenvendo por partes:

# 1º) Modifiquei a primeira função "def listaTokenizada" na parte "ELIMINANDO STOPWORDS";
# 2º) Mofifiquei a segunda função "def formulaCosseno";
# 3º) Na função "def mediaSentencas" eu não modifiquei nada, só dei uma organizada;

# obs: onde eu coloco "PARTE EDIVALDO" é a parte que eu adicionei e deixei em comment o teu código "PARTE RICCARDO" (caso não entenda o que 
# eu adicionei, ver a explicação detalhada na pasta da atividades colab no github)

# Tentei organizar o código também, colocando o nome nas variveis. Porém, eu não consegui em todas as funções pq eu não entendi muito bem
# o que as últimas funções fazem; Coloquei umas linhas de divisórias para dividir partes das funções e deixar um pouco mais claro o que cada
# parte faz.

# Se puder me explicar o que as ultimas funções fazem eu agradeceria mt, de rocha🙏

# Esclarecer o que "ainda falta" no comentario final, tipo: como assim "botar os numeros ate 2 casas decimais"?

# Para responder o que disse aqui ou deixar alguma observação, cria "codigo-v7.py" nesse mesmo repositorio e escreva em "LEIA EDIVALDO" logo 
# abaixo ou me chama no zapi

# |================================================================[ x ]====================================================================|
                                                              # LEIA EDIVALDO

# |================================================================[ x ]====================================================================|
                                                 # ESPAÇO PARA DOWNLOAD DE PACOTES E EXTRAS

# python -m spacy download pt_core_news_lg
# python -m spacy download pt_core_news_sm

# pip install -U pip setuptools wheel
# pip install -U spacy
# from spacy import displacy

# |================================================================[ x ]====================================================================|
                                                # FUNÇAO QUE CRIA UMA LISTA COM DENTRO AS SENTENCAS

def listaTokenizada(texto):

  # NORMALIZANDO O TEXTO (DEIXANDO EM MINÚSCULO)
  texto_minusculas = texto.lower()
  
  sentencas = nltk.tokenize.sent_tokenize(texto_minusculas)

  # STOPWORDS
  stop_words = set(stopwords.words('portuguese'))

  #------------------------------------------------->                                     <-------------------------------------------------|
                                                            # ELIMINANDO STOPWORDS

  # PARTE EDIVALDO
  sentencas_limpas = []

  for sentenca in sentencas:
        tokens = word_tokenize(sentenca)

        token_limpo = []
        for palavra in tokens:
            if palavra not in stop_words and palavra.isalnum():
                token_limpo.append(palavra)
        sentencas_limpas.append(token_limpo)
  
  return sentencas_limpas
  
  # PARTE RICCARDO
  # lista = []

  # for i in sentencas:
  #   palavras = word_tokenize(i)
  #   listas = []
  #   for j in palavras:
  #     if j not in stop_words and j.isalpha():
  #       listas.append(j)
  #   lista.append(listas)
  # print('Essa é a lista com todas as sentencas dentro separadas em uma lista interna cada uma:', lista) 
  # return lista

# |================================================================[ x ]====================================================================|
                                                    # FUNÇÃO QUE CALCULA A SIMILARIDADE

def formulaCosseno(lista):

  for k in range(len(lista)-1): # explica aqui o -1 pra mim, man ksksk
    # PARTE RICCARDO
    # uniao = set(lista[k] + lista[k+1])
    # uniao = list(uniao)

    # PARTE EDIVALDO
    uniao = list(set(lista[k] + lista[k+1]))
    
    print('Essa é a uniao de 2 sentencas, sem repeticao, para ser usada na comparacao e na formula: ', uniao)
    print('Primeira sentenca a ser comparada:', lista[k])
    print('Segunda sentenca a ser comparada: ', lista[k+1])

    #------------------------------------------------->                                     <-----------------------------------------------|
                             # CRIA OS NÚMEROS DE VEZES QUE APARECE UMA PALAVRA DA "uniao" NAS SENTENÇAS EM COMPARAÇÃO

    # PARTE EDIVALDO
    # CRIANDO VETORES COM A MESMA QUANTIDADE ZEROS DO TAMANHO DA LISTA "uniao"

    vetor1 = [0] * len(uniao) 
    vetor2 = [0] * len(uniao)

    # ADICIONANDO A FREQUENCIA DAS PALAVRAS NOS VETORES
    for token in lista[k]:
      vetor1[uniao.index(token)] += 1 
    
    for token in lista[k+1]:
      vetor2[uniao.index(token)] += 1

      # Estamos acessando cada token em "lista" percorrendo com o for. 
      # Na primeira repetição, o valor do token é 0, então ele irá acessar o primeiro token (ex: "lorem") em "lista[k]".
      # Depois que ele acessar o token "lorem", ele irá verificar em qual posição esse token ocupa na lista "uniao"
      # "lorem" ocupa a posição 2 (supondo) em "uniao", dessa forma, será acrescentado 1 na mesma posição no vetor1 de zeros. 

    #------------------------------------------------->                                     <-----------------------------------------------|
    # PARTE RICCARDO

    # sent1 = []
    # sent2 = []

    # for i in range(len(uniao)):
    #   cont = 0
    #   for j in range(len(lista[k])):
    #     if uniao[i] == lista[k][j]:
    #       cont += 1
    #   sent1.append(cont)

    # for i in range(len(uniao)):
    #   cont = 0
    #   for j in range(len(lista[k+1])):
    #     if uniao[i] == lista[k+1][j]:
    #       cont += 1
    #   sent2.append(cont)
      
    print('Quantidade de vezes que aparace cada palavra na primeira sentenca, com base a uniao das sentencas: ', vetor1)
    print('Quantidade de vezes que aparace cada palavra na segunda sentenca, com base a uniao das sentencas: ', vetor2)

    #------------------------------------------------->                                     <-----------------------------------------------|
                                    # COMEÇA A IMPLEMENTAÇÃO DA FÓRMULA DO COSSENO PARA FAZER A COMPARAÇÃO

    # parte de cima da formula 
    numerador = 0

    for i in range(len(vetor1)):
      produto = vetor1[i] * vetor2[i]
      numerador += produto
    print('Parte de cima da formula da similaridade: ', numerador)

    # parte de baixo da formula
    soma1 = 0
    soma2 = 0

    for i in range(len(vetor1)):
      soma1 += vetor1[i] ** 2
      soma2 += vetor2[i] ** 2
      
    denominador = sqrt((soma1 * soma2))
    print('Parte de baixo da formula da similaridade: ', denominador)

    # calculando fórmula final
    resultadocomparacao  = numerador / denominador
    print('Esse é o resultado da formula entre as 2 sentencas acima:', resultadocomparacao)

    # criando uma lista com o resultado de todas as somatorias finais
    # tipo: comparacao sent0 com sent1, sent1 com sent2, sent2 com sent3, etc.

    listares = []
    listares.append(resultadocomparacao)

  return listares

# |================================================================[ x ]====================================================================|
                                              # FUNÇÃO QUE CALCULA A MÉDIA ENTRE AS SENTENÇAS

def mediaSentencas(listares):
  # achar a media entre as similaridades

  soma_similaridades = 0
  quantidade_similaridades = len(listares)

  for similaridade_entre_sentencas in listares:
    soma_similaridades += similaridade_entre_sentencas
    #quantidade_de_similaridades += 1

  media_similaridades = soma_similaridades / quantidade_similaridades

  return media_similaridades

# |================================================================[ x ]====================================================================|
                                                              # FUNÇÃO ???

def spacysentencas(listares):
  listaspacy = []
  for i in range(len(listares)):
    contador = 0
    if listares[i] != 0:
      frase = nltk.tokenize.sent_tokenize(texto)
      doc1 = nlp(str(frase[i]))
      doc2 = nlp(str(frase[i+1]))

      print("\ndoc1", doc1)
      print("doc2", doc2)

      listadoc1 = []
      listadoc2 = []
      listaPalavrasTopicos1 = []

      # listaPalavrasTopicos2=[]
      for k in doc1.ents:
        print(f"a frase {doc1} tem palavras" , k, "|", k.label_)
        listadoc1.append(k.label_)
        listaPalavrasTopicos1.append(k)

      for k in doc2.ents:
        print(f"a frase {doc2} tem palavras" , k, "|", k.label_)
        listadoc2.append(k.label_)
        listaPalavrasTopicos1.append(k)

      print("reconhecimento de entidades 1", listadoc1)
      print("reconhecimento de entidades 2", listadoc2)
      print(listaPalavrasTopicos1)

      for i in listadoc1:
        for j in listadoc2:
          if i == j:
            contador += 1
      print("contador similaridades de entidades", contador)

  #     if contador<1:
  #       listaspacy.append("similares")
  #     else:
  #       listaspacy.append("similares")

  #    print("lista spacy", listaspacy)

  return listaPalavrasTopicos1

# |================================================================[ x ]====================================================================|
                                                                # FUNÇÃO ???

def separarSentencasEtopicos(mediaSimilaridades, listares, listaPalavrasTopicos1):
  #separar as sentencas
  listaTopicos = []
  stop_words = set(stopwords.words('portuguese'))
  sentencasMaiusculas = nltk.tokenize.sent_tokenize(texto)
  listaPalavrasLimpas = []

  for similaridadeEntreSentencas in range(len(listares)):
    if listares[similaridadeEntreSentencas]>=mediaSimilaridades:
      sentencasSimilaresUnidas = "\n" + sentencasMaiusculas[similaridadeEntreSentencas] +"\n" + sentencasMaiusculas[similaridadeEntreSentencas+1] + "\n"
      print("SENTENCAS COM SIMILARIDADE \n", sentencasSimilaresUnidas)
      sentencasSimilaresUnidas = word_tokenize(sentencasSimilaresUnidas.lower())
      
      for palavrasUnidas in sentencasSimilaresUnidas:
        if palavrasUnidas.isalnum() and palavrasUnidas not in stop_words:
          listaPalavrasLimpas.append(palavrasUnidas)
      frequencia = FreqDist(listaPalavrasLimpas)
      frequenciaTopicos = frequencia.most_common(5)

  print(frequenciaTopicos)

  for topico in frequenciaTopicos:
    if topico[1] >= 2:
      listaTopicos.append(topico[0])
  print("AQUI EEE", listaTopicos)
  print(listaPalavrasTopicos1)

  if len(listaTopicos) < 5:
    contador = 0
    while len(listaTopicos) < 5 and contador < len(listaPalavrasTopicos1):
      listaTopicos.append(listaPalavrasTopicos1[contador])
      contador += 1

  if len(listaTopicos) < 5:
    # quantosTopicosFaltam = 5-int(len(listaTopicos))
    # while len(listaTopicos) < 5:
    
    for i in range(len(frequenciaTopicos)):
      if frequenciaTopicos[i][0] not in listaTopicos and len(listaTopicos) < 5:
        listaTopicos.append(frequenciaTopicos[i][0])

  print("OS 5 TOPICOS \n", listaTopicos)

  # print(frequenciaTopicos)

# |================================================================[ x ]====================================================================|

print()

# texto = 'A ginasta Jade Barbosa, que obteve três medalhas nos Jogos Pan-Americanos do Rio, em julho, venceu votação na internet e será a representante brasileira no revezamento da tocha olímpica para Pequim-2008. A tocha passará por vinte países, mas o Brasil não estará no percurso olímpico. Por isso, Jade participará do evento em Buenos Aires, na Argentina, única cidade da América do Sul a receber o símbolo dos Jogos. O revezamento terminará em 8 de agosto, primeiro dia das Olimpíadas de Pequim.'
texto = 'Os artistas brasileiros têm tido reconhecimento mundial. Dentre os artistas, destacam-se Anitta, Caetano Veloso e Gilberto Gil. Todos eles já ganharam notórias premiações.'

lista = listaTokenizada(texto)
cosseno = formulaCosseno(lista)
media = mediaSentencas(cosseno)
spcy = spacysentencas(cosseno)
separar = separarSentencasEtopicos(media, cosseno, spcy)

print()
print('Todos os resultados que foram gerados por meio da formula das somatorias (a primeira é similaridadde da s1 com s2, dps é da s2 com s3, etc...): ', cosseno, media)


# falta:

# botar os numeros ate 2 casas decimais;
# resolver os resultados que dao 0, pois tem sentencas que nao tem nenhuma palavra igual, entao a parte de cima da formula fica com 0
# entao o resultado da 0 tb, parecendo que n tem semelhanca mesmo quando tem 
# (na vdd acho que ate separa as sentencas do jeito que a paula deu no enunciado do projeto, mas n sei se ta certo ou é bug);

# continuar o codigo, botando as palavras comuns e etc;
# ver se a separacao em def ta ok;
# perguntar se pode def sem return # ed: pode não man
# ver as aspas para python mais antigos # ed: como assim?