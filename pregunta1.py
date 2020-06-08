from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import nltk
from unicodedata import normalize
from generarTweets import generarTweet
import tweepy
import unidecode
import math
import re
nltk.download('stopwords')##Descargar el nltk
stemmer = PorterStemmer()  ##Cargar el stemmer

################################FUNCIONES DEL COSENO####################################################
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
        if (mod==0):
            normalizado.append(0)
        else:
            normalizado.append(i/mod)
    return normalizado

def cos(lista1,lista2):
    laSuma = 0
    for i in range (len(lista1)):
        laSuma = laSuma+(lista1[i]*lista2[i])
    return laSuma

def fun_modulo(lista):
    laSuma = 0
    for i in lista:
        laSuma = laSuma + i**2
    return math.sqrt(laSuma)

def funtfIdf(lista,v_idf):
    tfIdf=[]
    for i in lista:
        tfIdf.append(i*v_idf)
    return tfIdf

def jac(a,b):
    c = (set(a) | set(b))
    d = (set(a) & set(b))
    jacc = len(d)/len(c)
    return jacc

def diccionario (diccionario, punctuations):
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

def limpieza(tw1,vocabulario):
    doc=[]
    for e in range(len(tw1)):
        doc.append(re.sub('(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w +:\ / \ / \S +)', ' ', tw1[e].lower()).split()) 
    #hasta aqui esta tockenizado, minusculas y sin caracteres especiales
    stop= stopwords.words('spanish')
    stopw=[]
    for e in range(len(doc)):
        stopw.append([])
        for word in doc[e]:
            if word not in stop:
                stopw[e].append(word) #eliminación de stopwords
    doc=stopw
    stem=[]
    for k in range (len(doc)):
        st=[]
        for word in doc[k]:
            st.append(stemmer.stem(word))
        stem.append(st) #documentos con stemming 
    stem.append(vocabulario)
    return stem

def similitud(stem,vocabulario):  
    wtf=[]        
    for e in range (len(stem)): 
        pesado=[]
        for i in range (len(vocabulario)):
            ocu1=stem[e].count(vocabulario[i])
            pesado.append(calpeso(ocu1))
        wtf.append(pesado)   #WTF

    paradf=[]
    for e in range(len(vocabulario)):
        cant=[]
        for i in range(len(stem)):
            if (vocabulario[e] in stem[i]):
                cant.append(i)
        paradf.append(cant)
        
    df=[]
    for e in range (len(paradf)):
        df.append(len(paradf[e])) #Se obtiene el df                    

    el_idf=[]
    for e in range (len(df)):
        el_idf.append(idf(len(stem),df[e])) #Saca el idf
    
    ##tf por palabra
    wtf_p=[]
    for e in range (len(vocabulario)):
        pesa=[]
        for i in range (len(stem)):
            ocu1=stem[i].count(vocabulario[e])
            pesa.append(calpeso(ocu1))
        wtf_p.append(pesa)
        
    ##Sacar el tf-idf
    tf_idf=[]
    for e in range (len(el_idf)):
        tf_idf.append(funtfIdf(wtf_p[e], el_idf[e])) #por palabra
        
    arreglo1=[]
    arreglo2=[]
    for e in range(len(stem)):
        for l in range(len(vocabulario)):
            arreglo1.append(tf_idf[l][e]) #arreglo1:por documento, aun no en forma de lista

    for u in range(0,len(arreglo1),(len(vocabulario))):
        arreglo2.append(arreglo1[u:u+(len(vocabulario))])#peso por documento arreglado
    
    modulo=[]
    for e in range (len(arreglo2)):
        modulo.append(fun_modulo(arreglo2[e]))
    
    normalizado=[]
    for e in range (len(wtf)):
        normalizado.append(fun_normalizado(arreglo2[e], modulo[e]))
    res=[] 
    res2=[]
    for e in range (len(stem)-1):
        res.append(cos(normalizado[e],normalizado[len(stem)-1]))
        res2.append(jac(stem[e],stem[len(stem)-1]))
    
    return res,res2

def analisis(pos,neg, tw1):
    mensaje=[]
    cont_p=0
    cont_n=0
    cont_neutro=0
    for e in range (len(pos)):
        if(pos[e]>neg[e]):
            cont_p+=1
            mens='Positivo'
            mensaje.append('Positivo')
        elif(neg[e]>pos[e]):
            cont_n+=1
            mens='Negativo'
            mensaje.append('Negativo')
        else:
            cont_neutro+=1
            mens='Neutro'
            mensaje.append('Neutro')
        print(tw1[e],"--",mens,"\n")
    return cont_p,cont_n,cont_neutro,mensaje

def porcentaje(contador,tw1):
    porcen=(contador*100)/len(tw1)
    return porcen

def resultadosPregunta1(consulta, cantidadTweets, date_since, date_until):
    tw1 = []
    datos = generarTweet(consulta, cantidadTweets, date_since, date_until)
    for i in datos:
        tw1.append(i[2])
    punctuations = '''¡!()-[]{};:'"\<>./¿?@#$%^&*_~'''
    posi = diccionario("palabras_positivas.txt", punctuations)  # se almacena el diccionario de palabras positivas.(lista)
    negativa = diccionario("palabras_negativas.txt", punctuations)  # se almacena el diccionario de palabras neg.(lista)
    posi.sort(key=str.lower)  # ordeno alfabeticamente
    negativa.sort(key=str.lower)  # ordeno alfabeticamente
    tweets = limpieza(tw1, negativa)
    tweets2 = limpieza(tw1, posi)
    neg_cos, neg_jaccard = similitud(tweets, negativa)
    pos_cos, pos_jaccard = similitud(tweets2, posi)

    print("Por coseno: ")
    cont_p, cont_n, cont_neutro, mensaje = analisis(pos_cos, neg_cos, tw1)

    print("\nTweets Positivos: ", porcentaje(cont_p, tw1), "%")
    print("Tweets Negativos: ", porcentaje(cont_n, tw1), "%")
    print("Tweets Neutros: ", porcentaje(cont_neutro, tw1), "%")

    print("\nPor Jaccard")
    cont_pJ, cont_nJ, cont_neutroJ, mensajeJ = analisis(pos_jaccard, neg_jaccard, tw1)

    print("\nTweets Positivos: ", porcentaje(cont_pJ, tw1), "%")
    print("Tweets Negativos: ", porcentaje(cont_nJ, tw1), "%")
    print("Tweets Neutros: ", porcentaje(cont_neutroJ, tw1), "%")
    print(mensaje)

    porcentaje_coseno = []
    porcentaje_coseno.append(porcentaje(cont_p, tw1))
    porcentaje_coseno.append(porcentaje(cont_n, tw1))
    porcentaje_coseno.append(porcentaje(cont_neutro, tw1))

    porcentaje_jaccard = []
    porcentaje_jaccard.append(porcentaje(cont_pJ, tw1))
    porcentaje_jaccard.append(porcentaje(cont_nJ, tw1))
    porcentaje_jaccard.append(porcentaje(cont_neutroJ, tw1))

    for e in range(len(datos)):
        datos[e].append(mensaje[e])
        datos[e].append(mensajeJ[e])
    return(datos, porcentaje_coseno, porcentaje_jaccard)