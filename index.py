from flask import Flask, render_template,request
from generarTweets import generarTweet
from pregunta1 import resultadosPregunta1

app= Flask(__name__)

@app.route('/',methods=['GET','POST'])
def home():
    consulta=''
    cantidadTweets=''
    tw1=[]
    if request.method=='POST':
        consulta=request.form['consulta']
        cantidadTweets=int(request.form['cant'] ) #La cantidad de tweets que se consultaran
        date_since=request.form['fechainicio']
        date_until=request.form['fechafinal']
        ######
        datos, porcentaje_coseno, porcentaje_jaccard=resultadosPregunta1(consulta, cantidadTweets, date_since, date_until)
        #####
        return render_template('resultado.html',tweet=datos,pc=porcentaje_coseno,pj=porcentaje_jaccard,con=consulta,inicio=date_since,final=date_until)
    return render_template('primer.html')
if __name__ == '__main__':
    app.run(debug=True) 