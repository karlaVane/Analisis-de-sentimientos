from flask import Flask, render_template
from generarTweets import generarTweet

app= Flask(__name__)

@app.route('/')
def home():
    tw1=[]
    consulta="coronavirus"    #la consulta que se realizara a la API de tweeter
    cantidadTweets = 20  #La cantidad de tweets que se consultaran
    date_since = "2020-05-29"   #fecha hasta
    date_until = "2020-06-03"   #fecha desde, OJO--> coge tweets de un dia menos
    datos = generarTweet(consulta, cantidadTweets, date_since, date_until)
    return render_template('primer.html',tweet=datos)

@app.route('/segunda')
def segunda():
    return 'Segunda Opción'

if __name__ == '__main__':
    app.run(debug=True) 