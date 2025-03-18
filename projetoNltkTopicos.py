####FUNCIONA OK

#####################################################

import nltk
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.probability import FreqDist
from nltk.corpus import stopwords
from math import sqrt
import spacy
nlp=spacy.load("pt_core_news_lg")

# PARA VER UM CONTEXTO MELHOR, PODE DESCOMENTAR OS PRINT


#nesse def vai criar uma lista grande com dentro mini listas com uma sentenca cada.
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

#aqui vai fazer a formula da similaridade dos cossenos
def formulaCosseno(listaComSentencasSeparadas):
  listaDasSimilaridades=[]
  for k in range(len(listaComSentencasSeparadas)-1):
    uniaoDuasSentencas=set(listaComSentencasSeparadas[k]+listaComSentencasSeparadas[k+1])
    uniaoDuasSentencas=list(uniaoDuasSentencas)  #aqui uniu duas sentencas para ser feita a comparacao
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
      aparecimentoPalavrasSentenca1.append(cont) #nessa variavel tem uma lista de numeros, cada numero representa se apareceu a palavra referente a mesma posicao comparada
      #a uniao das duas frases em comparacao, sem palavras repetidas. Para visualizar pode printar ou ver no slide da prof, em um slide onde ela fala da formula dos cossenos,
      #q ela usa o exemplo a cat and a frog, la tem uma lista de numeros, a ideia daquela lista é essa daqui. Essa lista serve so para calcular a similaridade

    for i in range(len(uniaoDuasSentencas)):
      cont=0
      for j in range(len(listaComSentencasSeparadas[k+1])):
        if uniaoDuasSentencas[i]==listaComSentencasSeparadas[k+1][j]:
          cont+=1
      aparecimentoPalavrasSentenca2.append(cont) #aqui tb é aquela lista com aqueles numeros q tem um exemplo no slide
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

#nesse def vai criar uma lista, com mini listas dentro. Cada mini lista vai ter algumas palavras que sao as entidades de cada bloco de sentenca (bloco de sentenca seria
#as sentencas juntas quando similares ou sozinhas se nao similares, cada bloco vai ter uma lista de palavras de entidades), as entidades sao tipo nomes, lugares, eventos etc.,
#basicamente palavras chaves que podem ser usadas como palavras nos topicos, elas sao achadas como o spacy
def spacysentencas(listaDasSimilaridades):
  listaEntidades=[]
  for i in range(len(listaDasSimilaridades)): #vai executar o negocio a quantidade de blocos, entao tipo em um texto de 4 sentencas, e a sentenca 1 ta junta com sentenca 2
    #por causa de similaridade ja vai ser um bloco, e a sentenca 3 e 4 tao sozinhas pq tem similaridade com nd, entao sao 3 blocos (sent1+sent2, sent3, sent4), entao o for ai
    #vai ser feito 3 vezes, para achar as entidades de 3 sentencas, nesse exemplo
    contador=0
    contadorUnidas=0
    if listaDasSimilaridades[i]!=0: #aqui se a similaridade for diferente q 0, significa que tem similaridade, logo sao pelo menos 2 sentencas juntas
      frase=nltk.tokenize.sent_tokenize(texto)
      sentenca1=nlp(str(frase[i+contadorUnidas]))
      sentenca2=nlp(str(frase[i+1+contadorUnidas])) #o i+1 é pq a sentenca i é uma sentenca, e quero pegar logo a proxima, entao i+1
      # print("\nprimeira frase para buscar as entidades com spacy ", sentenca1)
      # print("segunda frase para buscar as entidades com spacy ", sentenca2)
      listaEntidades1=[] #vai receber as sentencas da sentenca 1
      listaEntidades2=[] #aqui da segunda
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
      # for entidade1 in listaEntidades1:
      #   for entidade2 in listaEntidades2:
      #     if entidade1==entidade2:
      #       contador+=1 #aqui é so um contador de similaridades das entidades, n serve pra nd, pode ignorar
      # print("contador similaridades de entidades, ver quantas vezes tem o mesmo tipo de entidades em ambas as frases", contador)
    contadorUnidas+=1
    if listaDasSimilaridades[i]==0: #aqui a similaridade de uma sentenca é 0, entao ela vai ser um bloco de uma unica sentenca
        frase=nltk.tokenize.sent_tokenize(texto)
        sentenca1=nlp(str(frase[i+contadorUnidas])) #o frase[i] é pq quero pegar a sentenca q ta indicada pela ordem do primeiro for la no topo+contadorUnidas pq se caso
        #ja teve uma comparacao anterior, vai ser pego a proxima sentenca, senao pega a mesma sentenca que foi pega antes
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
  # print(listaEntidades) #essa lista é a mesma coisa da primeira lista de sentencas, com mini listas, so que ai é com as entidades
  return listaEntidades

#aqui vai separar em blocos e colocar os topicos logo abaixo
def separarSentencasEtopicos(mediaSimilaridades, listaDasSimilaridades, listaEntidades):
  #separar as sentencas
  stop_words = set(stopwords.words('portuguese'))
  sentencasMaiusculas=nltk.tokenize.sent_tokenize(texto)
  listaPalavrasLimpas=[]
  contadorUnicas=0
  contadorUnidas=0
  for i in range(len(listaDasSimilaridades)):
    if listaDasSimilaridades[i]>=mediaSimilaridades: #se a similaridade for acima da media das similaridades entao vai pegar as similaridades de duas sentencas no minimo
      listaTopicos=[]
      contadorUnidas=0
      sentencasSimilaresUnidas="\n" + sentencasMaiusculas[i]+"\n" + sentencasMaiusculas[i+1] + "\n" #aqu vai pegar 2 sentencas e uni-las como antes, refiz o processo pq n sabia
      #como unir com o processo ja feito antes
      print("SENTENCAS COM SIMILARIDADE \n", sentencasSimilaresUnidas)
      sentencasSimilaresUnidas=word_tokenize(sentencasSimilaresUnidas.lower())
      for palavrasUnidas in sentencasSimilaresUnidas:
        if palavrasUnidas.isalnum() and palavrasUnidas not in stop_words:
          listaPalavrasLimpas.append(palavrasUnidas)
      frequencia=FreqDist(listaPalavrasLimpas)
      frequenciaTopicos=frequencia.most_common(5) #aqui sao as palavras mais frequentes da sentencas, pode ser usadas nos topicos, tem a palavra e quantas vezes apareceu
  # print(frequenciaTopicos)
      for topico in frequenciaTopicos:
        if topico[1]>=2:
          listaTopicos.append(topico[0]) #aqui vai na lista de palavras frequentes de antes e pega somente a palavra, sem a quantidade de repeticoes. Ai se caso uma palavra
          #apareceu mais de 2 vezes, bota na lista de topicos
    # print("palavra/palavras com mais de uma aparicao em ambas as frases que estao sendo comparadas", listaTopicos)
    # print(listaPalavrasTopicos1)
      if len(listaTopicos)<5: #tem q ter 5 palavras topicos, entao se tem menos de 5 palavras ainda, vai colocar as entidades pra completar 5 palavras
        contador=0
        if len(listaEntidades[contadorUnidas + contadorUnicas]) > 0:
          while len(listaTopicos) < 5 and contador < len(listaEntidades[contadorUnidas + contadorUnicas]):
            listaTopicos.append(listaEntidades[contadorUnidas+contadorUnicas][contador])
            contador+=1
      if len(listaTopicos)<5: #se caso ainda n completou, vai pegar o resto de palavras da sentenca e vai inserir nos topicos
        for j in range(len(frequenciaTopicos)):
          if frequenciaTopicos[j][0] not in listaTopicos and len(listaTopicos)<5:
            listaTopicos.append(frequenciaTopicos[j][0])
      contadorUnidas+=1
      print("OS 5 TOPICOS \n", listaTopicos, "\n")
    if listaDasSimilaridades[i]<mediaSimilaridades: #aqui é a mesma coisa de antes, so que quando a similaridade for abaixo da media, o q muda de antes acho que é so no
      #primeiro if, talvez da pra unir em um so processo
      listaPalavrasLimpas=[]
      listaTopicos=[]
      sentencasSimilaridade=sentencasMaiusculas[i+contadorUnidas]
      print("SENTENCAS SEM SIMILARIDADE \n", sentencasSimilaridade, "\n")
      # contadorUnicas+=1
      sentencasSimilaridade=word_tokenize(sentencasSimilaridade.lower())
      for palavrasUnidas in sentencasSimilaridade:
        if palavrasUnidas.isalnum() and palavrasUnidas not in stop_words:
          listaPalavrasLimpas.append(palavrasUnidas)
      frequencia=FreqDist(listaPalavrasLimpas)
      frequenciaTopicos=frequencia.most_common(5)
      for topico in frequenciaTopicos:
        if topico[1]>=2:
          listaTopicos.append(topico[0])
      # print("palavra/palavras com mais de uma aparicao em ambas as frases que estao sendo comparadas", listaTopicos)
      # print(listaPalavrasTopicos1)
      if len(listaTopicos)<5:
        contador=0
        if len(listaEntidades[contadorUnidas + contadorUnicas]) > 0:
          while len(listaTopicos) < 5 and contador < len(listaEntidades[contadorUnidas + contadorUnicas]):
            listaTopicos.append(listaEntidades[contadorUnidas + contadorUnicas][contador])
            contador += 1
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
# print('Todos os resultados que foram gerados por meio da formula das somatorias. Depois é a média entre elas): ', cosseno, media)

#falta:
#botar os numeros ate 2 casas decimais
#ver se a separacao em def ta ok
#perguntar se pode def sem return
#ver as aspas para python mais antigos

#limitacoes:
#o codigo ta meio limitado em 2 sentencas em cada bloco onde sentencas tem similaridades, se caso tiver um bloco com 3 sentencas unidas similares ou mais, acho q n funciona
#as palavras nos topicos, quando tem poucas palavras repetidas mais de 2 vezes e poucas entidades, acabam entrando as primeiras palavras da sentenca, mesmo n sendo
#palavras importantes