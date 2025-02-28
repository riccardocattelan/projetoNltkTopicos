import nltk
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from math import sqrt

#criar uma lista com dentro as sentencas
texto='a dog and a cat. a frog and a cat'
stop_words = set(stopwords.words("english"))
lista=[]
texto=texto.lower()
sentencas=nltk.tokenize.sent_tokenize(texto)
# palavras=word_tokenize(sentencas)
for i in sentencas:
  palavras=word_tokenize(i)
  listas=[]
  for j in palavras:
    if j not in stop_words and j.isalpha():
      listas.append(j)
  lista.append(listas)
print(lista)

#daqui vai ter q ser dinamico pra mudar as sentencas
#unir sentencas
uniao=set(lista[0]+lista[1])
uniao=list(uniao)
print(uniao)

#criar os numeros de vezes que aparece uma palavra da uniao nas sentencas em comparacao
sent1=[]
sent2=[]
for i in range(len(uniao)):
  cont=0
  for j in range(len(lista[0])):
    if uniao[i]==lista[0][j]:
      cont+=1
  sent1.append(cont)

for i in range(len(uniao)):
  cont=0
  for j in range(len(lista[0])):
    if uniao[i]==lista[1][j]:
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