import nltk
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords


from math import sqrt
#criar uma lista com dentro as sentencas
texto='A dog and a cat. A frog and a cat. A cat and a big horse'
stop_words = set(stopwords.words("english"))
lista=[]
listares=[]
texto=texto.lower()
sentencas=nltk.tokenize.sent_tokenize(texto)
# palavras=word_tokenize(sentencas)
for i in sentencas:
  palavras=word_tokenize(i)
  listas=[]
  for j in palavras:
    if j.isalpha(): #lembrar de botar if j.isalpha and j not in stop_words
      listas.append(j)
  lista.append(listas)
print(lista)

#daqui vai ter q ser dinamico pra mudar as sentencas
#unir sentencas
for k in range(len(lista)-1):
  uniao=set(lista[k]+lista[k+1])
  uniao=list(uniao)
  print(uniao)

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
  print(sent1)
  print(sent2)
#ser dinamico ate aqui


#formula somatoria
#parte cima somatoria
  somatorioup=0
  for i in range(len(uniao)):
    mult=sent1[i]*sent2[i]
    somatorioup+=mult
  print(somatorioup)

  #parte baixo somatoria
  soma1=0
  soma2=0
  for i in range(len(sent1)):
    soma1+=sent1[i]**2
    soma2+=sent2[i]**2
  somatoriodown=sqrt((soma1*soma2))
  print(somatoriodown)

  #calculando somatoria final
  resultadocomparacao=somatorioup/somatoriodown
  print(resultadocomparacao)
  #criando uma lista com as somatorias finais, sent0 com sent1, sent1 com sent2, sent2 com sent3, etc...
  listares.append(resultadocomparacao)
print(listares)