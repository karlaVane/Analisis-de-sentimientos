from flask import Flask, render_template,request
from generarTweets import generarTweet
from pregunta1 import calpeso,idf,fun_normalizado,cos,fun_modulo,funtfIdf,jac,diccionario,limpieza,similitud,analisis,porcentaje

app= Flask(__name__)

@app.route('/')
def home():
    tw1=[]
    consulta="coronavirus"    #la consulta que se realizara a la API de tweeter
    cantidadTweets = 5  #La cantidad de tweets que se consultaran
    date_since = "2020-05-29"   #fecha hasta
    date_until = "2020-06-03"   #fecha desde, OJO--> coge tweets de un dia menos
    ######
    posi=diccionario("palabras_positivas.txt")#se almacena el diccionario de palabras positivas.(lista)
    negativa=diccionario("palabras_negativas.txt")#se almacena el diccionario de palabras neg.(lista)
    posi.sort(key=str.lower) #ordeno alfabeticamente
    negativa.sort(key=str.lower) #ordeno alfabeticamente
    datos = generarTweet(consulta, cantidadTweets, date_since, date_until)
    for i in datos:
        tw1.append(i[2])
    tweets=limpieza(tw1,negativa)
    tweets2=limpieza(tw1,posi)
    neg_cos,neg_jaccard=similitud(tweets,negativa)
    pos_cos,pos_jaccard=similitud(tweets2,posi)
    cont_p,cont_n,cont_neutro,mensaje=analisis(pos_cos,neg_cos)
    cont_pJ,cont_nJ,cont_neutroJ,mensajeJ=analisis(pos_jaccard,neg_jaccard)

    porcentaje_coseno=[]
    porcentaje_coseno.append(porcentaje(cont_p,tw1))
    porcentaje_coseno.append(porcentaje(cont_n,tw1))
    porcentaje_coseno.append(porcentaje(cont_neutro,tw1))

    porcentaje_jaccard=[]
    porcentaje_jaccard.append(porcentaje(cont_pJ,tw1))
    porcentaje_jaccard.append(porcentaje(cont_nJ,tw1))
    porcentaje_jaccard.append(porcentaje(cont_neutroJ,tw1))

    for e in range(len(datos)):
        datos[e].append(mensaje[e])
        datos[e].append(mensajeJ[e])
    ######
    
    #return render_template('primer.html',tweet=datos,mensajeCoseno=mensaje)
    return render_template('primer.html',tweet=datos,pc=porcentaje_coseno,pj=porcentaje_jaccard)
    


if __name__ == '__main__':
    app.run(debug=True) 