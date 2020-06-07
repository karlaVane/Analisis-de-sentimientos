import csv
import re
import nltk
import random
import math
import numpy as np
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from unicodedata import normalize
from string import digits
from sklearn.linear_model import LogisticRegression

nltk.download('stopwords')  ##Descargar el nltk
stemmer = PorterStemmer()  ##Cargar el stemmer

sentimiento_n, sentimiento_p, archivo, nuevo= ([] for i in range(4))

def calpeso(valor):
    if (valor)>0:
        peso =1+math.log10(valor);
    else:
        peso= 0
    return peso

def idf(n,df):
    if(df==0):
        res=0
    else:
        res=math.log10(n/df);
    return res

def fun_normalizado(lista,mod):
    normalizado=[]
    for i in lista:
        normalizado.append(i/mod)
    return normalizado

def funtfIdf(lista,v_idf):
    tfIdf=[]
    for i in lista:
        tfIdf.append(i*v_idf)
    return tfIdf

punctuations = '''¡!()-[]{};:'"\<>./¿?@#$%^&*_~'''
def stop_adicionales(diccionario):
    pos=[]
    arr=[]
    f = open(diccionario, "r",encoding="utf8")
    for linea in f.readlines():
        linea=linea.strip()#quita \n y \t de los string
        no_punct = ""
        for char in linea: #proceso para eliminar signos de pregunta y admiración
            if char not in punctuations:
                no_punct = no_punct + char
            linea=no_punct
        linea = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", 
                       normalize( "NFD", linea.lower()), 0, re.I)
        linea = normalize( 'NFC', linea) #proceso para eliminar las tildes sin problema y no eliminar ñ
        pos.append(linea)
        
    for word in pos:
        arr.append(stemmer.stem(word))#proceso de stemming en el diccionario 
    dic=[]
    for word in arr:
        if (word not in dic):
            dic.append(word) #verificación que no existan mismas palabras en el diccionario
    f.close() 
    return dic   

stopw_adic=stop_adicionales("stopwords.txt")#Stopwords adicionales
stopw_adic.sort(key=str.lower) #ordeno alfabeticamente

f=  open("Tweets.csv", "r", encoding="utf8")
reader = csv.reader(f)
for row in reader:
    archivo.append(row) 
        
for i in range(1,len(archivo)):
    if (archivo[i][3] == "-1" and len(sentimiento_n) < 500):
      sentimiento_n.append(archivo[i][3])
      nuevo.append([archivo[i][2],archivo[i][3]])
    elif (archivo[i][3] == "1" and len(sentimiento_p) < 500):
        sentimiento_p.append(archivo[i][3])
        nuevo.append([archivo[i][2],archivo[i][3]])
 
#En nuevo estan los 1000 tweets con su sentimiento.       
tweet_s, sentimiento, training, test, datos, textoTrain, senTrain, textoTest, senTest = ([] for i in range(9))
for e in range (len(nuevo)):
    tweet_s.append(nuevo[e][0])
    sentimiento.append(nuevo[e][1])

def vocabulario_1000(stopw_a,documento):
    for e in range(len(documento)):
        documento[e]= re.sub('(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w +:\ / \ / \S +)', ' ', documento[e].lower()).split() 
    #hasta aqui esta tockenizado, minusculas y sin caracteres especiales
    for e in range (len(documento)):
        for i in range (len(documento[e])):
            remove_digits =str.maketrans('', '', digits)
            documento[e][i]=documento[e][i].translate(remove_digits )
    stop= stopwords.words('spanish')    
    for e in range (len(stopw_a)):
        stop.append(stopw_a[e])
    stopw=[]
    for e in range(len(documento)):
        stopw.append([])
        for word in documento[e]:
            if word not in stop:
                stopw[e].append(word) #eliminación de stopwords
    documento=stopw
    
    stem=[]
    vocabulario=[]
    for k in range (len(documento)):
        st=[]
        for word in documento[k]:
            st.append(stemmer.stem(word))
            if (stemmer.stem(word) not in vocabulario):
                vocabulario.append(stemmer.stem(word))
        stem.append(st) #documentos con stemming 
    return stem,vocabulario


def td_idf(stem,vocabulario):
    wtf = []
    for e in range(len(stem)):
        pesado = []
        for i in range(len(vocabulario)):
            ocu1 = stem[e].count(vocabulario[i])
            pesado.append(calpeso(ocu1))
        wtf.append(pesado)  # WTF

    paradf = []
    for e in range(len(vocabulario)):
        cant = []
        for i in range(len(stem)):
            if (vocabulario[e] in stem[i]):
                cant.append(i)
        paradf.append(cant)

    df = []
    for e in range(len(paradf)):
        df.append(len(paradf[e]))  # Se obtiene el df

    el_idf = []
    for e in range(len(df)):
        el_idf.append(idf(len(stem), df[e]))  # Saca el idf

    ##tf por palabra
    wtf_p = []
    for e in range(len(vocabulario)):
        pesa = []
        for i in range(len(stem)):
            ocu1 = stem[i].count(vocabulario[e])
            pesa.append(calpeso(ocu1))
        wtf_p.append(pesa)

    ##Sacar el tf-idf
    tf_idf = []
    for e in range(len(el_idf)):
        tf_idf.append(funtfIdf(wtf_p[e], el_idf[e]))  # por palabra

    arreglo1 = []
    arreglo2 = []
    for e in range(len(stem)):
        for l in range(len(vocabulario)):
            arreglo1.append(tf_idf[l][e])  # arreglo1:por documento, aun no en forma de lista

    for u in range(0, len(arreglo1), (len(vocabulario))):
        arreglo2.append(arreglo1[u:u + (len(vocabulario))])  # tf-idf por documento arreglado
    return arreglo2 #devuelve por documento

doc,vocabulario=vocabulario_1000(stopw_adic,tweet_s)

for e in range (len(doc)):
    datos.append([doc[e],sentimiento[e]])
#print(len(datos))

while(len(training) < (len(doc)*0.7)): #El 70% para training, datos = 1000
    aux = random.choice(datos)
    if aux not in training:
        training.append(aux)
        datos.remove(aux)

"""
for i in datos:
    if i not in training and i not in test:
        test.append(i)
"""
test=datos
print("Training",len(training))
print("Test",len(test))

for t in training:
    textoTrain.append(t[0]) #X
    senTrain.append(t[1])#Y

for te in test:
    textoTest.append(te[0]) #X
    senTest.append(te[1]) #solo para comparar

tf_idf_train = td_idf(textoTrain,vocabulario)
tf_id_test = td_idf(textoTest, vocabulario)

x = np.array(tf_idf_train)
y = np.array(senTrain)
x_test = np.array(tf_id_test)
y_test = np.array(senTest)

#print(x.shape)
#print(x_test.shape)

algoritmo = LogisticRegression()#Algoritmo de regresion

#Entrana el modelo
algoritmo.fit(x,y)#(x,y) el trainning

y_pred = algoritmo.predict(x_test)#x_test
print("Predicciones de Y utilizando X_TEST\n",y_pred)
cont=0
for e in range(len(y_pred)):
    if y_test[e] != y_pred[e]:
        cont =+ cont+1
error = (cont/len(y_pred))*100

print("Error: {0:.3f}".format(error),"%")

cont_neg=0
cont_posi=0
for e in y_pred:
    if (e=='-1'):
        cont_neg+=1
    else:
        cont_posi+=1
def porcentaje(contador,test):
    porcen=(contador*100)/len(test)
    return porcen

print("Tweets Negativos: {0:.3f}".format(porcentaje(cont_neg,test)),"%")
print("Tweets Positivos:{0:.3f}".format(porcentaje(cont_posi,test)),"%")

 