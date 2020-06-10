from flask import Flask, render_template,request
from generarTweets import generarTweet
from pregunta1 import resultadosPregunta1
from pregunta2 import resultadosPregunta2
from pregunta3 import resultadoSPregunta3

app= Flask(__name__)

@app.route('/',methods=['GET','POST'])
def home():
    consulta=''
    cantidadTweets=''
    if request.method=='POST':
        consulta=request.form['consulta']
        cantidadTweets=int(request.form['cant'] ) #La cantidad de tweets que se consultaran
        date_since=request.form['fechainicio']
        date_until=request.form['fechafinal']
        ######
        datos, porcentaje_coseno, porcentaje_jaccard,ejecucion=resultadosPregunta1(consulta, cantidadTweets, date_since, date_until)
        #####
        return render_template('resultado.html',tweet=datos,pc=porcentaje_coseno,pj=porcentaje_jaccard,con=consulta,inicio=date_since,final=date_until,cant_tw=cantidadTweets,ejecucion=ejecucion)
    return render_template('primer.html')

@app.route('/preg2',methods=['GET','POST'])
def regresion():
    resultado, error, pos, neg, exe_time,training,test=resultadosPregunta2()
    return render_template('regresion.html',resultado=resultado, error=error, pos=pos, neg=neg, exe_time=exe_time,training=training,test=test)

@app.route('/preg3',methods=['GET','POST'])
def textblob():
    consulta=''
    cantidadTweets=''
    if request.method=='POST':
        consulta=request.form['consulta']
        cantidadTweets=int(request.form['cant'] ) #La cantidad de tweets que se consultaran
        date_since=request.form['fechainicio']
        date_until=request.form['fechafinal']
        res_3,exe_time=resultadoSPregunta3(consulta, cantidadTweets, date_since, date_until)
        return render_template('resultado3.html',resultado=res_3,con=consulta,inicio=date_since,final=date_until,cant_tw=cantidadTweets,exe_time=exe_time)
    return render_template('tercera.html')

if __name__ == '__main__':
    app.run(debug=True) 