# BACKUP

##################################################################################################


import nltk
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.probability import FreqDist
from nltk.corpus import stopwords
from math import sqrt
import spacy
nlp=spacy.load("pt_core_news_lg")


#criar uma lista com dentro as sentencas
def listaTokenizada(texto):
  stop_words = set(stopwords.words('portuguese'))
  listaComSentencasSeparadas=[]
  textoMinusculas=texto.lower()
  sentencas=nltk.tokenize.sent_tokenize(textoMinusculas)
  for sentencaUnica in sentencas:
    palavras=word_tokenize(sentencaUnica)
    miniListas=[]
    for palavraUnica in palavras:
      if palavraUnica not in stop_words and palavraUnica.isalpha():
        miniListas.append(palavraUnica)
    listaComSentencasSeparadas.append(miniListas)
  # print('Essa é a lista com todas as sentencas dentro separadas em uma lista interna cada uma:', listaComSentencasSeparadas)  #agora tem uma lista maior com varias listas dentro, cada uma das mini listas tem uma sentenca (em teoria)
  return listaComSentencasSeparadas

#unir sentenças
def formulaCosseno(listaComSentencasSeparadas):
  listaDasSimilaridades=[]
  for k in range(len(listaComSentencasSeparadas)-1):
    uniaoDuasSentencas=set(listaComSentencasSeparadas[k]+listaComSentencasSeparadas[k+1])
    uniaoDuasSentencas=list(uniaoDuasSentencas)
    # print()
    # print('Essa é a uniao de 2 sentencas, sem repeticao, para ser usada na comparacao e na formula: ', uniaoDuasSentencas) # aqui vai ter uma sentenca unica que na vdd é a uniao de duas sentencas, que nem "a dog and a cat + a cat and a frog = a dog and cat frog"
    # print('Primeira sentenca a ser comparada:', listaComSentencasSeparadas[k])
    # print('Segunda sentenca a ser comparada: ', listaComSentencasSeparadas[k+1])

    #criar os numeros de vezes que aparece uma palavra da uniao nas sentencas em comparacao
    aparecimentoPalavrasSentenca1=[]
    aparecimentoPalavrasSentenca2=[]
    for i in range(len(uniaoDuasSentencas)):
      cont=0
      for j in range(len(listaComSentencasSeparadas[k])):
        if uniaoDuasSentencas[i]==listaComSentencasSeparadas[k][j]:
          cont+=1
      aparecimentoPalavrasSentenca1.append(cont)

    for i in range(len(uniaoDuasSentencas)):
      cont=0
      for j in range(len(listaComSentencasSeparadas[k+1])):
        if uniaoDuasSentencas[i]==listaComSentencasSeparadas[k+1][j]:
          cont+=1
      aparecimentoPalavrasSentenca2.append(cont)
    # print('Quantidade de vezes que aparace cada palavra na primeira sentenca, com base a uniao das sentencas: ', aparecimentoPalavrasSentenca1)
    # print('Quantidade de vezes que aparace cada palavra na segunda sentenca, com base a uniao das sentencas: ', aparecimentoPalavrasSentenca2)

  #comeca a implementacao da formula com somatoria para fazer a comparacao
  #parte de cima da formula da somatoria
    somatorioCossenoParteSuperior=0
    for i in range(len(uniaoDuasSentencas)):
      multiplicacao=aparecimentoPalavrasSentenca1[i]*aparecimentoPalavrasSentenca2[i]
      somatorioCossenoParteSuperior+=multiplicacao
    # print('Parte de cima da formula da similaridade: ', somatorioCossenoParteSuperior)

    #parte de baixo da formula da somatoria
    variavelA=0
    variavelB=0
    for i in range(len(aparecimentoPalavrasSentenca1)):
      variavelA+=aparecimentoPalavrasSentenca1[i]**2
      variavelB+=aparecimentoPalavrasSentenca2[i]**2
    somatorioCossenoParteInferior=sqrt((variavelA*variavelB))
    # print('Parte de baixo da formula da similaridade: ', somatorioCossenoParteInferior)

    #calculando somatoria final
    resultadocomparacao=somatorioCossenoParteSuperior/somatorioCossenoParteInferior
    # print('Esse é o resultado da formula entre as 2 sentencas acima:', resultadocomparacao)
    #criando uma lista com o resultado de todas as somatorias finais, tipo comparacao sent0 com sent1, sent1 com sent2, sent2 com sent3, etc...
    listaDasSimilaridades.append(resultadocomparacao)
  return listaDasSimilaridades

def mediaSentencas(listaDasSimilaridades):
  #achar a media entre as similaridades
  somaDasSimilaridades=0
  quantidadeDeSimilaridades=0
  for similaridadeEntreSentencas in listaDasSimilaridades:
    somaDasSimilaridades+=similaridadeEntreSentencas
    quantidadeDeSimilaridades+=1
  mediaSimilaridades=somaDasSimilaridades/quantidadeDeSimilaridades
  return mediaSimilaridades


def spacysentencas(listaDasSimilaridades):
  listaEntidades=[]
  for i in range(len(listaDasSimilaridades)):
    contador=0
    contadorUnidas=0
    if listaDasSimilaridades[i]!=0:
      frase=nltk.tokenize.sent_tokenize(texto)
      sentenca1=nlp(str(frase[i+contadorUnidas]))
      sentenca2=nlp(str(frase[i+1+contadorUnidas]))
      # print("\nprimeira frase para buscar as entidades com spacy ", sentenca1)
      # print("segunda frase para buscar as entidades com spacy ", sentenca2)
      listaEntidades1=[]
      listaEntidades2=[]
      listaPalavrasTopicos1=[]
      for entidadesDaSentenca1 in sentenca1.ents:
        # print(f"a frase - {sentenca1} - tem entidade: " , entidadesDaSentenca1, "|", entidadesDaSentenca1.label_)
        listaEntidades1.append(entidadesDaSentenca1.label_)
        listaPalavrasTopicos1.append(entidadesDaSentenca1)
      for entidadesDaSentenca2 in sentenca2.ents:
        # print(f"a frase - {sentenca2} - tem entidade: " , entidadesDaSentenca2, "|", entidadesDaSentenca2.label_)
        listaEntidades2.append(entidadesDaSentenca2.label_)
        listaPalavrasTopicos1.append(entidadesDaSentenca2)
      listaEntidades.append(listaPalavrasTopicos1)
      # print("LISTA PALAVRAS TOPICOS 1", listaPalavrasTopicos1)
      # print("reconhecimento de entidades frase 1", listaEntidades1)
      # print("reconhecimento de entidades frase 2", listaEntidades2)
      # print(listaPalavrasTopicos1)
      for entidade1 in listaEntidades1:
        for entidade2 in listaEntidades2:
          if entidade1==entidade2:
            contador+=1
      # print("contador similaridades de entidades, ver quantas vezes tem o mesmo tipo de entidades em ambas as frases", contador)
    contadorUnidas+=1
    if listaDasSimilaridades[i]==0:
        frase=nltk.tokenize.sent_tokenize(texto)
        sentenca1=nlp(str(frase[i+contadorUnidas]))
        # print("\nprimeira frase para buscar as entidades com spacy ", sentenca1)
        listaEntidades1=[]
        listaPalavrasTopicos1=[]
        for entidadesDaSentenca1 in sentenca1.ents:
          # print(f"a frase - {sentenca1} - tem entidade: " , entidadesDaSentenca1, "|", entidadesDaSentenca1.label_)
          listaEntidades1.append(entidadesDaSentenca1.label_)
          listaPalavrasTopicos1.append(entidadesDaSentenca1)
        listaEntidades.append(listaPalavrasTopicos1)
        # print("reconhecimento de entidades frase 1", listaEntidades1)
        # print(listaPalavrasTopicos1)
        # print("LISTA PALAVRAS TOPICOS 1", listaPalavrasTopicos1)
  print(listaEntidades)
  return listaEntidades

def separarSentencasEtopicos(mediaSimilaridades, listaDasSimilaridades, listaEntidades):
  #separar as sentencas
  stop_words = set(stopwords.words('portuguese'))
  sentencasMaiusculas=nltk.tokenize.sent_tokenize(texto)
  listaPalavrasLimpas=[]
  contadorUnicas=0
  contadorUnidas=0
  for i in range(len(listaDasSimilaridades)):
    if listaDasSimilaridades[i]>=mediaSimilaridades:
      listaTopicos=[]
      contadorUnidas=0
      sentencasSimilaresUnidas="\n" + sentencasMaiusculas[i]+"\n" + sentencasMaiusculas[i+1] + "\n"
      print("SENTENCAS COM SIMILARIDADE \n", sentencasSimilaresUnidas)
      sentencasSimilaresUnidas=word_tokenize(sentencasSimilaresUnidas.lower())
      for palavrasUnidas in sentencasSimilaresUnidas:
        if palavrasUnidas.isalnum() and palavrasUnidas not in stop_words:
          listaPalavrasLimpas.append(palavrasUnidas)
      frequencia=FreqDist(listaPalavrasLimpas)
      frequenciaTopicos=frequencia.most_common(5)
      contadorUnidas+=1
      # print("DREQUENCIA TOPICOS UNIDAS", frequenciaTopicos) ####
  # print(frequenciaTopicos)
      for topico in frequenciaTopicos:
        if topico[1]>=2:
          listaTopicos.append(topico[0])
    # print("palavra/palavras com mais de uma aparicao em ambas as frases que estao sendo comparadas", listaTopicos)
    # print(listaPalavrasTopicos1)
      if len(listaTopicos)<5:
        contador=0
        # print("AQUI OH", listaEntidades[contadorUnidas+contadorUnicas][contador]) ####
        while len(listaTopicos) < 5 and contador < len(listaTopicos):
          listaTopicos.append(listaEntidades[contadorUnidas+contadorUnicas][contador])
          contador+=1
        # print(listaTopicos) ####
      if len(listaTopicos)<5:
        for j in range(len(frequenciaTopicos)):
          if frequenciaTopicos[j][0] not in listaTopicos and len(listaTopicos)<5:
            listaTopicos.append(frequenciaTopicos[j][0])
      print("OS 5 TOPICOS \n", listaTopicos, "\n")
    ##################################
    if listaDasSimilaridades[i]<mediaSimilaridades:
      listaPalavrasLimpas=[]
      listaTopicos=[]
      sentencasSimilaridade=sentencasMaiusculas[i+contadorUnidas]
      # print(contadorUnidas) ####
      # print(sentencasSimilaridade) ####
      print("SENTENCAS SEM SIMILARIDADE \n", sentencasSimilaridade, "\n")
      # contadorUnicas+=1
      sentencasSimilaridade=word_tokenize(sentencasSimilaridade.lower())
      for palavrasUnidas in sentencasSimilaridade:
        if palavrasUnidas.isalnum() and palavrasUnidas not in stop_words:
          listaPalavrasLimpas.append(palavrasUnidas)
      frequencia=FreqDist(listaPalavrasLimpas)
      frequenciaTopicos=frequencia.most_common(5)
      # print("FREQUENCIA TOPICOS UNICAS", frequenciaTopicos) ####
      for topico in frequenciaTopicos:
        if topico[1]>=2:
          listaTopicos.append(topico[0])
      # print("palavra/palavras com mais de uma aparicao em ambas as frases que estao sendo comparadas", listaTopicos)
      # print(listaPalavrasTopicos1)
      if len(listaTopicos)<5:
        contador=0
        # print("AQUI OH ", listaEntidades[contadorUnidas + contadorUnicas][contador]) ####
        # print(contadorUnidas + contadorUnicas, contador) ####
        # while len(listaTopicos)<5 and contador <= len(listaTopicos):  ####
        # print("OUT OF RANGE", listaEntidades[contadorUnicas+contadorUnidas][contador]) ####
        while len(listaTopicos) < 5 and contador < len(listaEntidades[contadorUnidas + contadorUnicas]):
          listaTopicos.append(listaEntidades[contadorUnidas + contadorUnicas][contador])
          contador += 1
          # print(listaTopicos) ####
          # print("LISTA TOPICOS UNICAS", listaTopicos) ####
      if len(listaTopicos)<5:
        for j in range(len(frequenciaTopicos)):
          if frequenciaTopicos[j][0] not in listaTopicos and len(listaTopicos)<5:
            listaTopicos.append(frequenciaTopicos[j][0])
      contadorUnicas+=1
      print("\nOS 5 TOPICOS \n", listaTopicos, "\n")
      
print()

texto='A ginasta Jade Barbosa, que obteve três medalhas nos Jogos Pan-Americanos do Rio, em julho, venceu votação na internet e será a representante brasileira no revezamento da tocha olímpica para Pequim-2008. A tocha passará por vinte países, mas o Brasil não estará no percurso olímpico. Por isso, Jade participará do evento em Buenos Aires, na Argentina, única cidade da América do Sul a receber o símbolo dos Jogos. O revezamento terminará em 8 de agosto, primeiro dia das Olimpíadas de Pequim.'
# texto='Os artistas brasileiros têm tido reconhecimento mundial. Dentre os artistas, destacam-se Anitta, Caetano Veloso e Gilberto Gil. Todos eles já ganharam notórias premiações.'
lista=listaTokenizada(texto)
cosseno=formulaCosseno(lista)
media=mediaSentencas(cosseno)
spcy=spacysentencas(cosseno)
separar=separarSentencasEtopicos(media, cosseno, spcy)
print()
print('Todos os resultados que foram gerados por meio da formula das somatorias. Depois é a média entre elas): ', cosseno, media)

#falta:
#botar os numeros ate 2 casas decimais
#continuar o codigo, separando sentencas e etc
#ver se a separacao em def ta ok
#perguntar se pode def sem return
#ver as aspas para python mais antigos