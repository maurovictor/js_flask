## Mauro Victor Castro

import os
from flask import Flask, render_template, request, redirect, url_for, Request, flash, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from PIL import Image
from resizeimage import resizeimage
import sqlite3
import base64
import io
import helpers
import database_helper

UPLOAD_FOLDER = 'static/pictures/'
ALLOWED_EXTENSIONS = set(['png'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = os.urandom(24)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/auth', methods=['GET','POST'])
def authentication():
    if request.method == 'GET':
        return render_template("login.html")
    else:
        user = request.form['usuario']
        password = request.form['password']

        user_list = database_helper.load_users_name()
        hashed_password = database_helper.load_hashed_password(user)
        rigth_password = check_password_hash(hashed_password, password)
        adm = database_helper.load_role(user)
        if user in user_list and rigth_password:
            session['user'] = user
            session['role'] = adm
            flash("Você está logado como: " + user)
            return redirect(url_for('pagina_incial'))
        else:
            flash("Usuário não registrado ou dados incorretos")
            return redirect("auth")

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash("Fora da Conta de usuário")
    return redirect(url_for('pagina_incial'))


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'GET':
        return render_template('add_user.html')
    else:
        user_name        = request.form['usuario']
        user_password    = request.form['password']
        confirm_password = request.form['confirm-password']
        user_name_list   = database_helper.load_users_name()

        if user_name in user_name_list:
            flash(user_name + " já existem como usuário")
            return redirect("auth")
        if user_password != confirm_password:
            flash("Senhas incoerentes")
            return redirect("add_user")
        else:
            database_helper.save_new_user(user_name, user_password)
            flash(user_name + " salvo como usuário")
            return redirect("auth")

@app.route('/no_db')
def no_db():
    return render_template('no_data_base.html')

@app.route('/')
def pagina_incial():
    return render_template('principal.html')

@app.route('/add_defeito', methods=['GET', 'POST'])
def add_defeito():

    if request.method == 'GET':
        dados_placas = database_helper.load_boards() ## list of tuples of (board, fabric)
        return render_template('add_defeito.html', dados_placas = dados_placas)
    else:
        conn = sqlite3.connect('db/banco_de_dados')
        c = conn.cursor()
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
        session['nome_placa']   = nome_placa
        session['nome_defeito'] = defeito
        return redirect("add_desenho")

@app.route('/add_placa', methods=['GET', 'POST'])
def adicionar_placa():
    if request.method == 'GET':
        connectors = database_helper.load_connectors()
        return render_template('add_placa.html', connectors=connectors)
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
        else:
            flash('Arquivo com extensão não permitida. Apenas .png serão considerados')
            return redirect("add_placa")


        conector = database_helper.pick_connector_id(conector)
        database_helper.save_board(placa, fabricante, tipo, conector)
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
            image_b64 = request.values['imageBase64'].strip()
            image_b64 = image_b64[22:]

            decoded = base64.b64decode(image_b64)

            img_bytes = io.BytesIO(decoded)
            img = Image.open(img_bytes, mode='r')
            img.save("{0}editions/{1}_{2}.png".format(app.config['UPLOAD_FOLDER'],\
                                    session['nome_defeito'],session['nome_placa']))
            flash("Defeito {0} adicionado à placa {1}".format(session['nome_defeito'],\
                                                                session['nome_placa']))

            session.pop('nome_placa', None)
            session.pop('nome_defeito', None)

        except Exception as e:
            print('desenho')
            print(e)

        return ''

@app.route('/add_conn', methods=['GET', 'POST'])
def connector():
    if request.method == 'GET':
        return render_template('add_conn_form.html')
    else:
        session['connector_name'] = request.form['connector-name']
        return redirect("add_conn_scheema")

@app.route('/add_conn_scheema', methods=['GET', 'POST'])
def conn_scheema():
    if request.method == 'GET':
        return render_template('conn_scheema_register.html')
    else:
        values=request.form['c']
        connector_name = request.form['name']
        print("Nome do conector " + connector_name)
        coordinates = helpers.get_coordinates(values)
        commands = helpers.generate_commands(coordinates)
        #helpers.generate_url(commands)
        database_helper.save_connector(connector_name, commands)
        return ''

@app.route('/test', methods=['GET', 'POST'])
def test():
    if request.method == 'GET':
        dados_placas = database_helper.load_boards()
        return render_template("test_form.html", dados_placas=dados_placas)
    else:
        placa = request.form['placa']
        print("A placa é: " + placa)
        board_id = database_helper.pick_board_id(placa)
        connector_id = database_helper.load_connector_from_board(board_id)
        connector_commands = database_helper.load_connector_command(connector_id)
        session['connector_commands'] = connector_commands
        session['hardware_test'] = True
        session['board_name'] = placa
        return redirect("hardware_test")

@app.route('/hardware_test', methods=['GET', 'POST'])
def h_test():
    if request.method == 'GET':
        if ('hardware_test' and 'workbench_ip') in session:
            board_name = session['board_name']
            board_id = database_helper.pick_board_id(board_name)
            deffect_list = database_helper.load_deffects(board_id)

            helpers.generate_url(session['connector_commands'], session['workbench_ip'])
            #kill sessions
            session.pop('connector_commands', None)
            session.pop('hardware_test', None)
            session.pop('board_name', None)
            return render_template("hardware_test.html", board_name=board_name, deffect_list=deffect_list)
        else:
            flash('Bancada ou teste não configurado')
            return render_template("denied_access.html")
    else:
        deffect = request.form['deffect']
        board_name = request.form['board_name']
        picture_path = helpers.get_picture_path(deffect, board_name)
        print(picture_path)
        return jsonify(picture_path)

@app.route('/workbench', methods=['GET','POST'])
def work_bench():
    if request.method == 'GET':
        workbenches = database_helper.load_workbenches()
        return render_template('workbench_form.html', workbenches=workbenches)
    else:
        name = request.form['bancada-nome']
        ip = request.form['bancada-ip']
        database_helper.save_workbench(ip, name)
        return redirect("workbench")

@app.route('/workbench_setup', methods=['POST'])
def workbench_setup():
    session['workbench_name'] = request.form['bancada']
    session['workbench_ip'] = database_helper.pick_workbench_ip(request.form['bancada'])
    flash('{0} configurada como bancada principal'.format(session['workbench_name']))
    return redirect("workbench")

@app.route('/des')
def des():
    session['nome_placa'] = "asdkflhasdf"
    session['nome_defeito'] = "kwejfbqjwkrbhfdvs"
    return render_template('des.html')
