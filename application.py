import os
from flask import Flask, render_template, request, redirect, url_for, Request, flash
from werkzeug.utils import secure_filename
import sqlite3

UPLOAD_FOLDER = 'static/pictures/raw/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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

@app.route('/add_placa', methods=['GET', 'POST'])
def adicionar_placa():
    if request.method == 'GET':
        return render_template('add_placa.html')
    if request.method == 'POST':
        placa = request.form['nome_placa']
        if placa == '':
            flash('Placa sem Nome')
            return redirect("add_placa")
        fabricante = request.form['fabricante']

        if fabricante == '':
            flash('Fabricante sem Nome')
            return redirect("add_placa")

        tipo = request.form['tipo']
        if tipo == '':
            flash('Placa sem tipo')
            return redirect("add_placa")

        conector = request.form['conector']
        if conector == '':
            flash('Insira o tipo de donector')
            return redirect("add_placa")

        if 'file' not in request.files:
            flash('Arquivo não selecionado')
            return str(request.files)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('Arquvio sem nome')
            return redirect("add_placa")
        if file and allowed_file(file.filename):
            filename = "{0}.png".format(placa)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            conn = sqlite3.connect('db/banco_de_dados')
            c = conn.cursor()
            command = "INSERT INTO Placas (nome_placa, fabricante, tipo, conector) VALUES('{0}', '{1}', '{2}', '{3}')".format(placa, fabricante, tipo, conector)
            c.execute(command)
            conn.commit()
            conn.close()
            flash('Placa {0} Registrada'.format(placa))

            return redirect("add_placa")
