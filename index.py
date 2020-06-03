from flask import Flask

app= Flask(__name__)

@app.route('/')
def home():
    return 'Hello world'

@app.route('/segunda')
def segunda():
    return 'Segunda Opción'

if __name__ == '__main__':
    app.run()