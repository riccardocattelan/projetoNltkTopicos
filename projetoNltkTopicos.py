import nltk
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from math import sqrt

#criar uma lista com dentro as sentencas
texto="A ginasta Jade Barbosa, que obteve três medalhas nos Jogos Pan-Americanos do Rio, em julho, venceu votação na internet e será a representante brasileira no revezamento da tocha olímpica para Pequim-2008. A tocha passará por vinte países, mas o Brasil não estará no percurso olímpico. Por isso, Jade participará do evento em Buenos Aires, na Argentina, única cidade da América do Sul a receber o símbolo dos Jogos. O revezamento terminará em 8 de agosto, primeiro dia das Olimpíadas de Pequim."
stop_words = set(stopwords.words("portuguese"))
lista=[]
listares=[]
texto=texto.lower()
sentencas=nltk.tokenize.sent_tokenize(texto)
for i in sentencas:
  palavras=word_tokenize(i)
  listas=[]
  for j in palavras:
    if j not in stop_words and j.isalpha():
      listas.append(j)
  lista.append(listas)
print(lista)  #agora tem uma lista maior com varias listas dentro, cada uma das mini listas tem uma sentenca (em teoria)

#daqui para frente temos q achar um jeito para mudar as sentencas automaticamente, para comparar todas (tentei usar esse for k in range(len(listas[k+1])) )
#unir sentencas
for k in range(len(lista)-1):
  uniao=set(lista[k]+lista[k+1])
  uniao=list(uniao)
  print(uniao)
  print() # aqui vai ter uma sentenca unica que na vdd é a uniao de duas sentencas, que nem "a dog and a cat + a cat and a frog = a dog and cat frog"
  print(lista[k])
  print(lista[k+1])

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
#ser dinamico ate aqui eu acho talvez


#comeca a implementacao da formula com somatoria para fazer a comparacao
#parte de cima da formula da somatoria
  somatorioup=0
  for i in range(len(uniao)):
    mult=sent1[i]*sent2[i]
    somatorioup+=mult
  print(somatorioup)

  #parte de baixo da formula da somatoria
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
  #criando uma lista com o resultado de todas as somatorias finais, tipo comparacao sent0 com sent1, sent1 com sent2, sent2 com sent3, etc...
  listares.append(resultadocomparacao)
print(listares)

#falta:
#botar os numeros ate 2 casas decimais
#resolver os resultados que dao 0, pois tem sentencas que nao tem NENHUMA palavra igual, entao a parte de cima da formula fica com 0, entao o resultado da 0 tb, parecendo que n tem semelhanca mesmo quando tem (na vdd acho que ate separa as sentencas do jeito que a paula deu no enunciado do projeto, mas n sei se ta certo ou é bug)

#ps: a formula ta em um dos arq do colab q a prof botou no sigaa, n sei qual arq é