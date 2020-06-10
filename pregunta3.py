from textblob import TextBlob
from generarTweets import generarTweet
import csv
import unidecode
import re
import time

def analisisSentimientos(corpus):
    analisis = TextBlob(corpus)
    if analisis.sentiment.polarity > 0:
        return ("Positivo",1)
    if analisis.sentiment.polarity == 0:
        return ("Neutro",0)
    else:
        return ("Negativo",-1)

def crearArchivo(nombre_archivo,sentimiento,fecha,autor,texto):
    crearArch = open("%s.csv" % nombre_archivo, "w", newline='',
                     encoding="utf-8")  # Nombre del nuevo archivo si se quiere sobre escribir poner el missmo!
    writer = csv.writer(crearArch)
    writer.writerow(["FECHA", "AUTOR", "TEXTO", "ANALISIS DE SENTIMIENTO TBLOB"])
    for col in range(len(sentimiento)):
        writer.writerow([fecha[col], autor[col], texto[col], sentimiento[col]])
    print("Archivo %s.csv Generado !! :)" % nombre_archivo)


def resultadoSPregunta3(consulta, cantidadTweets, date_since, date_until):
    start_time = time.time()
    datos = generarTweet(consulta, cantidadTweets, date_since, date_until)
    fecha, autor, texto, sentimiento = ([] for i in range(4))
    print("[------------------TEXTO------------------, -----------------SENTIMIENTO----------------]")
    for columna in datos:
        fecha.append(columna[0])
        autor.append(columna[1])
        texto.append(columna[2])
        sentimiento.append(analisisSentimientos(columna[2]))
        print([columna[2], analisisSentimientos(columna[2])])
    crearArchivo("Tweets con TextBlob", sentimiento, fecha, autor, texto)
    total1=[]
    for i in range (len(texto)):
        total=[]
        total.append(fecha[i])
        total.append(autor[i])
        total.append(texto[i])
        total.append(sentimiento[i])
        total1.append(total)
    end_time = time.time()
    exe_time = round((end_time - start_time),2)
    return total1,exe_time


