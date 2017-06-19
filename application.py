from flask import Flask, render_template
import sqlite3


app = Flask(__name__)
conn = sqlite3.connect('db/banco_de_dados')
c = conn.cursor()
@app.route('/')
def pagina_teste():
    return render_template('principal.html')

@app.route('/add_defeito')
def adicionar_defeito():
    #if request.method == 'GET':
    return render_template('add_defeito.html')
    #else:
        ##c.execute("INSERT INTO Defeitos VALUES(%s, %s, %s, %s) ") % (nome_defeito, descricao,conserto, placa)
        ##conn.commit()

@app.route('/add_placa')
def adicionar_placa():
    return render_template('add_placa.html')
