from textblob import TextBlob
from generarTweets import generarTweet
import csv
import unidecode
import re
consulta="coronavirus"    #la consulta que se realizara a la API de tweeter
cantidadTweets = 100    #La cantidad de tweets que se consultaran
date_since = "2020-05-29"   #fecha hasta
date_until = "2020-06-03"   #fecha desde, OJO--> coge tweets de un dia menos
nombre_archivo = "Tweets con textBlob"
datos = generarTweet(consulta, cantidadTweets, date_since, date_until)
def analisisSentimientos(corpus):
    analisis = TextBlob(corpus)
    if analisis.sentiment.polarity > 0:
        return ("Positivo",1)
    if analisis.sentiment.polarity == 0:
        return ("Neutro",0)
    else:
        return ("Negativo",-1)


fecha, autor, texto, sentimiento = ([] for i in range(4))
print("[------------------TEXTO------------------, -----------------SENTIMIENTO----------------]")
for columna in datos:
    fecha.append(columna[0])
    autor.append(columna[1])
    texto.append(columna[2])
    sentimiento.append(analisisSentimientos(columna[2]))
    print([columna[2], analisisSentimientos(columna[2])])

crearArch = open("%s.csv" %nombre_archivo, "w", newline='', encoding="utf-8")   #Nombre del nuevo archivo si se quiere sobre escribir poner el missmo!
writer = csv.writer(crearArch)
writer.writerow(["FECHA", "AUTOR", "TEXTO", "ANALISIS DE SENTIMIENTO TBLOB"])
for col in range(len(sentimiento)):
    writer.writerow([fecha[col], autor[col], texto[col], sentimiento[col]])
print("Archivo %s.csv Generado !! :)" %nombre_archivo)