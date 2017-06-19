import os
from flask import Flask, render_template, request, redirect, url_for, Request
import sqlite3


app = Flask(__name__)

@app.route('/')
def pagina_teste():
    return render_template('principal.html')

@app.route('/add_defeito', methods=['GET', 'POST'])
def add_defeito():
    #if request.method == 'GET':
    if request.method == 'GET':
        return render_template('add_defeito.html')
    else:
        conn = sqlite3.connect('db/banco_de_dados')
        c = conn.cursor()
        defeito = request.form['nome_defeito']
        descricao = request.form['descricao']
        conserto = request.form['conserto']
        placa = "123"
        command = "INSERT INTO Defeitos (nome_defeito, descricao, conserto, placa) VALUES('{0}', '{1}', '{2}', '{3}')".format(defeito, descricao, conserto, placa)
        c.execute(command)
        conn.commit()
        conn.close()
        return redirect("add_defeito")

@app.route('/add_placa')
def adicionar_placa():
    return render_template('add_placa.html')
