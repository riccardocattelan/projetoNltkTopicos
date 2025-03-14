#O MENOS PIOR ATE AGORA E UM POUCO MAIS COMPLETO

##################################################################################################


import nltk
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.probability import FreqDist
from nltk.corpus import stopwords
from math import sqrt

import spacy
nlp=spacy.load("pt_core_news_lg")

# nlp=spacy.load("pt_core_news_sm")
# doc=nlp("Apple está tentando comprar uma startup do Reino Unido por R$1 bilhão.")
# for tokeniza in doc.ents:
#   print(tokeniza, "|", tokeniza.label_)

#criar uma lista com dentro as sentencas
def listaTokenizada(texto):
  stop_words = set(stopwords.words('portuguese'))
  lista=[]
  # listares=[]
  textoMinusculas=texto.lower()
  sentencas=nltk.tokenize.sent_tokenize(textoMinusculas)
  for i in sentencas:
    palavras=word_tokenize(i)
    listas=[]
    for j in palavras:
      if j not in stop_words and j.isalpha():
        listas.append(j)
    lista.append(listas)
  print('Essa é a lista com todas as sentencas dentro separadas em uma lista interna cada uma:', lista)  #agora tem uma lista maior com varias listas dentro, cada uma das mini listas tem uma sentenca (em teoria)
  return lista

#unir sentenças
def formulaCosseno(lista):
  listares=[]
  for k in range(len(lista)-1):
    uniao=set(lista[k]+lista[k+1])
    uniao=list(uniao)
    print()
    print('Essa é a uniao de 2 sentencas, sem repeticao, para ser usada na comparacao e na formula: ', uniao) # aqui vai ter uma sentenca unica que na vdd é a uniao de duas sentencas, que nem "a dog and a cat + a cat and a frog = a dog and cat frog"
    print('Primeira sentenca a ser comparada:', lista[k])
    print('Segunda sentenca a ser comparada: ', lista[k+1])

    #criar os numeros de vezes que aparece uma palavra da uniao nas sentencas em comparacao
    sent1=[]
    sent2=[]
    for i in range(len(uniao)):
      cont=0
      for j in range(len(lista[k])):
        if uniao[i]==lista[k][j]:
          cont+=1
      sent1.append(cont)

    for i in range(len(uniao)):
      cont=0
      for j in range(len(lista[k+1])):
        if uniao[i]==lista[k+1][j]:
          cont+=1
      sent2.append(cont)
    print('Quantidade de vezes que aparace cada palavra na primeira sentenca, com base a uniao das sentencas: ', sent1)
    print('Quantidade de vezes que aparace cada palavra na segunda sentenca, com base a uniao das sentencas: ', sent2)

  #comeca a implementacao da formula com somatoria para fazer a comparacao
  #parte de cima da formula da somatoria
    somatorioup=0
    for i in range(len(uniao)):
      mult=sent1[i]*sent2[i]
      somatorioup+=mult
    print('Parte de cima da formula da similaridade: ', somatorioup)

    #parte de baixo da formula da somatoria
    soma1=0
    soma2=0
    for i in range(len(sent1)):
      soma1+=sent1[i]**2
      soma2+=sent2[i]**2
    somatoriodown=sqrt((soma1*soma2))
    print('Parte de baixo da formula da similaridade: ', somatoriodown)

    #calculando somatoria final
    resultadocomparacao=somatorioup/somatoriodown
    print('Esse é o resultado da formula entre as 2 sentencas acima:', resultadocomparacao)
    #criando uma lista com o resultado de todas as somatorias finais, tipo comparacao sent0 com sent1, sent1 com sent2, sent2 com sent3, etc...
    listares.append(resultadocomparacao)
  return listares

def mediaSentencas(listares):
  #achar a media entre as similaridades
  somaDasSimilaridades=0
  quantidadeDeSimilaridades=0
  for similaridadeEntreSentencas in listares:
    somaDasSimilaridades+=similaridadeEntreSentencas
    quantidadeDeSimilaridades+=1
  mediaSimilaridades=somaDasSimilaridades/quantidadeDeSimilaridades
  return mediaSimilaridades

# def separarSentencasEtopicos(mediaSimilaridades, listares, stop_words):
#   #separar as sentencas
#   stop_words = set(stopwords.words('portuguese'))
#   sentencasMaiusculas=nltk.tokenize.sent_tokenize(texto)
#   listaPalavrasLimpas=[]
#   for similaridadeEntreSentencas in range(len(listares)):
#     if listares[similaridadeEntreSentencas]>=mediaSimilaridades:
#       sentencasSimilaresUnidas="\n" + sentencasMaiusculas[similaridadeEntreSentencas]+"\n" + sentencasMaiusculas[similaridadeEntreSentencas+1] + "\n"
#       print(sentencasSimilaresUnidas)
#       sentencasSimilaresUnidas=word_tokenize(sentencasSimilaresUnidas.lower())
#       for palavrasUnidas in sentencasSimilaresUnidas:
#         if palavrasUnidas.isalnum() and palavrasUnidas not in stop_words:
#           listaPalavrasLimpas.append(palavrasUnidas)
#   frequencia=FreqDist(listaPalavrasLimpas)
#   frequenciatopicos=frequencia.most_common(5)

#   print(frequenciatopicos)


def spacysentencas(listares):
  listaspacy=[]
  for i in range(len(listares)):
    contador=0
    if listares[i]!=0:
      frase=nltk.tokenize.sent_tokenize(texto)
      doc1=nlp(str(frase[i]))
      doc2=nlp(str(frase[i+1]))
      print("\ndoc1", doc1)
      print("doc2", doc2)
      listadoc1=[]
      listadoc2=[]
      listaPalavrasTopicos1=[]
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
          if i==j:
            contador+=1
      print("contador similaridades de entidades", contador)
  #     if contador<1:
  #       listaspacy.append("similares")
  #   else:
  #     listaspacy.append("similares")
  # print("lista spacy", listaspacy)
  return listaPalavrasTopicos1

def separarSentencasEtopicos(mediaSimilaridades, listares, listaPalavrasTopicos1):
  #separar as sentencas
  listaTopicos=[]
  stop_words = set(stopwords.words('portuguese'))
  sentencasMaiusculas=nltk.tokenize.sent_tokenize(texto)
  listaPalavrasLimpas=[]
  for similaridadeEntreSentencas in range(len(listares)):
    if listares[similaridadeEntreSentencas]>=mediaSimilaridades:
      sentencasSimilaresUnidas="\n" + sentencasMaiusculas[similaridadeEntreSentencas]+"\n" + sentencasMaiusculas[similaridadeEntreSentencas+1] + "\n"
      print("SENTENCAS COM SIMILARIDADE \n", sentencasSimilaresUnidas)
      sentencasSimilaresUnidas=word_tokenize(sentencasSimilaresUnidas.lower())
      for palavrasUnidas in sentencasSimilaresUnidas:
        if palavrasUnidas.isalnum() and palavrasUnidas not in stop_words:
          listaPalavrasLimpas.append(palavrasUnidas)
      frequencia=FreqDist(listaPalavrasLimpas)
      frequenciaTopicos=frequencia.most_common(5)
  print(frequenciaTopicos)
  for topico in frequenciaTopicos:
    if topico[1]>=2:
      listaTopicos.append(topico[0])
  print("AQUI EEE", listaTopicos)
  print(listaPalavrasTopicos1)
  if len(listaTopicos)<5:
    contador=0
    while len(listaTopicos) < 5 and contador < len(listaPalavrasTopicos1):
      listaTopicos.append(listaPalavrasTopicos1[contador])
      contador+=1
  if len(listaTopicos)<5:
    # quantosTopicosFaltam=5-int(len(listaTopicos))
    # while len(listaTopicos) < 5:
    for i in range(len(frequenciaTopicos)):
      if frequenciaTopicos[i][0] not in listaTopicos and len(listaTopicos)<5:
        listaTopicos.append(frequenciaTopicos[i][0])
  print("OS 5 TOPICOS \n", listaTopicos)

# def separarSentencasEtopicos(mediaSimilaridades, listares, listaPalavrasTopicos1):
#     # Separar as sentenças
#     listaTopicos = []
#     stop_words = set(stopwords.words('portuguese'))
#     sentencasMaiusculas = nltk.tokenize.sent_tokenize(texto)
#     listaPalavrasLimpas = []
    
#     for similaridadeEntreSentencas in range(len(listares)):
#         if listares[similaridadeEntreSentencas] >= mediaSimilaridades:
#             sentencasSimilaresUnidas = "\n" + sentencasMaiusculas[similaridadeEntreSentencas] + "\n" + sentencasMaiusculas[similaridadeEntreSentencas + 1] + "\n"
#             print(sentencasSimilaresUnidas)
#             sentencasSimilaresUnidas = word_tokenize(sentencasSimilaresUnidas.lower())
            
#             for palavrasUnidas in sentencasSimilaresUnidas:
#                 if palavrasUnidas.isalnum() and palavrasUnidas not in stop_words:
#                     listaPalavrasLimpas.append(palavrasUnidas)
            
#             # Frequência das palavras
#             frequencia = FreqDist(listaPalavrasLimpas)
#             frequenciaTopicos = frequencia.most_common(5)
#             print(frequenciaTopicos)

#             # Adicionando palavras que apareceram pelo menos 2 vezes
#             for topico in frequenciaTopicos:
#                 if topico[1] >= 2:
#                     listaTopicos.append(topico[0])

#     # Garantindo que teremos 5 tópicos (adicionando entidades se necessário)
#     print("AQUI EEE", listaTopicos)
#     print(listaPalavrasTopicos1)
    
#     if len(listaTopicos) < 5:
#         contador = 0
#         # Agora, verificamos se o contador não ultrapassa o tamanho da lista
#         while len(listaTopicos) < 5 and contador < len(listaPalavrasTopicos1):
#             listaTopicos.append(listaPalavrasTopicos1[contador])
#             contador += 1
#         print("Lista final de tópicos:", listaTopicos)

#     return listaTopicos

      



  # print(frequenciaTopicos)

print()

# texto='A ginasta Jade Barbosa, que obteve três medalhas nos Jogos Pan-Americanos do Rio, em julho, venceu votação na internet e será a representante brasileira no revezamento da tocha olímpica para Pequim-2008. A tocha passará por vinte países, mas o Brasil não estará no percurso olímpico. Por isso, Jade participará do evento em Buenos Aires, na Argentina, única cidade da América do Sul a receber o símbolo dos Jogos. O revezamento terminará em 8 de agosto, primeiro dia das Olimpíadas de Pequim.'
texto='Os artistas brasileiros têm tido reconhecimento mundial. Dentre os artistas, destacam-se Anitta, Caetano Veloso e Gilberto Gil. Todos eles já ganharam notórias premiações.'
lista=listaTokenizada(texto)
cosseno=formulaCosseno(lista)
media=mediaSentencas(cosseno)
spcy=spacysentencas(cosseno)
separar=separarSentencasEtopicos(media, cosseno, spcy)
print()
print('Todos os resultados que foram gerados por meio da formula das somatorias (a primeira é similaridadde da s1 com s2, dps é da s2 com s3, etc...): ', cosseno, media)
# pip install -U pip setuptools wheel
# pip install -U spacy
# !python -m spacy download pt_core_news_lg
# from spacy import displacy


#falta:
#botar os numeros ate 2 casas decimais
#resolver os resultados que dao 0, pois tem sentencas que nao tem nenhuma palavra igual, entao a parte de cima da formula fica com 0, entao o resultado da 0 tb, parecendo que n tem semelhanca mesmo quando tem (na vdd acho que ate separa as sentencas do jeito que a paula deu no enunciado do projeto, mas n sei se ta certo ou é bug)
#continuar o codigo, botando as palavras comuns e etc
#ver se a separacao em def ta ok
#perguntar se pode def sem return
#ver as aspas para python mais antigos