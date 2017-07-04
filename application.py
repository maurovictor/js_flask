import os
from flask import Flask, render_template, request, redirect, url_for, Request, flash, session
from werkzeug.utils import secure_filename
from PIL import Image
from resizeimage import resizeimage
import sqlite3
import base64
import io
import pymysql
import helpers


UPLOAD_FOLDER = 'static/pictures/'
ALLOWED_EXTENSIONS = set(['png'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = os.urandom(24)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/no_db')
def no_db():
    return render_template('no_data_base.html')

@app.route('/')
def pagina_incial():
    return render_template('principal.html')

@app.route('/add_defeito', methods=['GET', 'POST'])
def add_defeito():
    try:
        conn = sqlite3.connect('db/banco_de_dados')
        c = conn.cursor()
    except Exception as e:
        return redirect("no_db", error = e)

    if request.method == 'GET':
        command_1 = "SELECT nome_placa FROM Placas ORDER BY placa_id"
        c.execute(command_1)
        placas_raw = c.fetchall()
        placas = [placas_raw[x][0] for x in range(len(placas_raw))]

        command_2 = "SELECT fabricante FROM Placas ORDER BY placa_id"
        c.execute(command_2)
        fabricantes_raw = c.fetchall()
        fabricantes = [fabricantes_raw[x][0] for x in range(len(fabricantes_raw))]

        dados_placas = list(zip(placas, fabricantes)) ## zip placas' list with fabricantes' list and turn it into a list
        ##print(dados_placas)
        return render_template('add_defeito.html', dados_placas = dados_placas)
    else:

        defeito = request.form['nome_defeito']
        descricao = request.form['descricao']
        conserto = request.form['conserto']
        nome_placa = request.form['placa']
        ## Take the id from selected board
        c.execute("SELECT placa_id FROM Placas WHERE nome_placa=?", (nome_placa,))
        placa_id = c.fetchone()[0]

        ## Add flaw to database
        command = "INSERT INTO Defeitos (nome_defeito, descricao, conserto, placa) VALUES('{0}', '{1}', '{2}', '{3}')".format(defeito, descricao, conserto, placa_id)
        c.execute(command)
        conn.commit()
        conn.close()
        session['nome_placa'] = nome_placa
        session['nome_defeito'] = defeito
        return redirect("add_desenho")

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
            file.save(os.path.join(app.config['UPLOAD_FOLDER']+"raw/", filename))

            with open('static/pictures/raw/{0}'.format(filename), 'r+b') as f:
                with Image.open(f) as image:
                    cover = resizeimage.resize_contain(image, [1100, 520])
                    cover.save('static/pictures/raw/{0}'.format(filename), image.format)

        print(fabricante)
        conn = sqlite3.connect('db/banco_de_dados')
        c = conn.cursor()
        command = "INSERT INTO Placas (nome_placa, fabricante, tipo, conector) VALUES('{0}', '{1}', '{2}', '{3}')".format(placa, fabricante, tipo, conector)
        c.execute(command)
        conn.commit()
        conn.close()
        flash('Placa {0} Registrada'.format(placa))
        return redirect("add_placa")

@app.route('/add_desenho', methods=['GET','POST'])
def desenho():
    if request.method == 'GET':
        try:
            nome_placa = session['nome_placa']
            return render_template("desenho_aux.html", nome_placa=nome_placa)
        except Exception as e:
            return render_template("denied_access.html")
    if request.method == 'POST':
        try:
            #print(session['nome_placa'])
            #session.pop('nome_placa', None)
            image_b64 = request.values['imageBase64'].strip()
            image_b64 = image_b64[22:]

            decoded = base64.b64decode(image_b64)

            img_bytes = io.BytesIO(decoded)
            img = Image.open(img_bytes, mode='r')
            img.save("{0}editions/{1}_{2}.png".format(app.config['UPLOAD_FOLDER'], session['nome_defeito'],session['nome_placa']))
            flash("Defeito {0} adicionado à placa {1}".format(session['nome_defeito'], session['nome_placa']))
        except Exception as e:
                print(e)

        return ''

@app.route('/add_conector', methods=['GET', 'POST'])
def conector():
    if request.method == 'GET':
        return render_template('conectores.html')
    else:
        values=request.form['c']
        coordinates = helpers.get_coordinates(values)
        print(coordinates)
        commands = helpers.generate_commands(coordinates)
        

        return ''
