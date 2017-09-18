import sqlite3, os
from werkzeug.security import generate_password_hash, check_password_hash

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, 'db/banco_de_dados')
def save_new_user(name, password):
    password = generate_password_hash(password)
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        db_command = "INSERT INTO Usuario (usuario_nome, usuario_senha, adm) VALUES('{0}', '{1}', '{2}')"\
                            .format(name, password, 0)
        c.execute(db_command)
        conn.commit()
        conn.close()
        print("db:: " + name + " saved as a user")
        return ''
    except Exception as e:
        print()
        print("##################")
        print("Erro na func. save_new_user: ")
        print(e)
        print("##################")

def load_hashed_password(user):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    db_command = "SELECT usuario_senha FROM Usuario WHERE usuario_nome=?"
    c.execute(db_command, (user,))
    hashed_password = c.fetchone()[0]
    conn.commit()
    conn.close()
    return hashed_password
def load_users_name():
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        db_command = "SELECT usuario_nome FROM Usuario ORDER BY usuario_id"
        c.execute(db_command)
        users_names = c.fetchall()
        users_names = [users_names[i][0] for i in range(len(users_names))]
        conn.commit()
        conn.close()
        print("db:: loaded User Names")
        return users_names
    except Exception as e:
        print()
        print("##################")
        print("Erro na func. load_users_name: ")
        print(e)
        print("##################")


def save_connector(name, commands):
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        db_command = "INSERT INTO Conector (nome_conector, byte1, byte2, byte3, byte4, byte5, byte6, byte7, byte8) VALUES('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}')"\
                .format(name, commands[0], commands[1], commands[2], commands[3], commands[4], commands[5], commands[6], commands[7])
        c.execute(db_command)
        conn.commit()
        conn.close()
        print("db:: connector "+ name + " saved..")
    except Exception as e:
        print()
        print("##################")
        print("Erro na func. save_connector: ")
        print(e)
        print("##################")

def load_role(user):
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        db_command = "SELECT adm FROM Usuario WHERE usuario_nome=?"
        c.execute(db_command,(user,))
        role = c.fetchone()[0]
        role = bool(role)
        conn.commit()
        conn.close()
        return role
    except Exception as e:
        raise


def save_board(name, fabric, board_type, connector):
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        db_command = "INSERT INTO Placas (nome_placa, fabricante, tipo, conector) VALUES('{0}', '{1}', '{2}', '{3}')"\
                .format(name, fabric, board_type, connector)
        c.execute(db_command)
        conn.commit()
        conn.close()
        print("db:: board "+ name + " saved..")
    except Exception as e:
        print()
        print("##################")
        print("Erro na func. save_board: ")
        print(e)
        print("##################")

def save_workbench(ip, name):
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        db_command = "INSERT INTO Bancada (bancada_ip, bancada_nome) VALUES ('{0}', '{1}')"\
                                    .format(ip, name)
        c.execute(db_command)
        conn.commit()
        conn.close()
        print("db:: workbench "+ name +" saved..")
    except Exception as e:
        print()
        print("##################")
        print("Erro na func. work_bench: ")
        print(e)
        print("##################")



def load_boards():
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        db_command_1 = "SELECT nome_placa FROM Placas ORDER BY placa_id"
        db_command_2 = "SELECT fabricante FROM Placas ORDER BY placa_id"

        c.execute(db_command_1)
        placas_raw = c.fetchall()

        c.execute(db_command_2)
        fabricantes_raw = c.fetchall()

        conn.commit()
        conn.close()
        placas      = [placas_raw[x][0] for x in range(len(placas_raw))]
        fabricantes = [fabricantes_raw[x][0] for x in range(len(fabricantes_raw))]
        print("db: boards loaded from DB")
        return list(zip(placas, fabricantes))
    except Exception as e:
        print()
        print("##################")
        print("Erro na func. load_boards: ")
        print(e)
        print("##################")


def load_connectors():
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        db_command = "SELECT nome_conector FROM Conector ORDER BY conector_id"
        c.execute(db_command)
        connectors_raw = c.fetchall()
        print(connectors_raw)
        conn.commit()
        conn.close()
        connectors = [connectors_raw[x][0] for x in range(len(connectors_raw))]
        print("db: connectors loaded from DB")
        return connectors
    except Exception as e:
        print()
        print("##################")
        print("Erro na func. load_connectors: ")
        print(e)
        print("##################")


def pick_connector_id(connector_name):
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        db_command = "SELECT conector_id FROM Conector WHERE nome_conector=?"
        c.execute(db_command, (connector_name,))
        connector_id = c.fetchone()[0]
        conn.commit()
        conn.close()
        return connector_id
    except Exception as e:
        print()
        print("##################")
        print("Erro na func. pick_connector_id: ")
        print(e)
        print("##################")

def pick_board_id(board_name):
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        db_command = "SELECT placa_id FROM Placas WHERE nome_placa=?"
        c.execute(db_command, (board_name,))
        ## Retrieve board_id
        board_id = c.fetchone()[0]
        ##
        conn.commit()
        conn.close()
        return board_id
    except Exception as e:
        print()
        print("##################")
        print("Erro na func. pick_board_id: ")
        print(e)
        print("##################")

def pick_workbench_ip(name):
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        db_command = "SELECT bancada_ip FROM Bancada WHERE bancada_nome=?"
        c.execute(db_command, (name,))
        workbench_ip = c.fetchone()[0]
        conn.commit()
        conn.close()
        return workbench_ip
    except Exception as e:
        print()
        print("##################")
        print("Erro na func. pick_workbench_id: ")
        print(e)
        print("##################")

def pick_board_name(board_id):
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        db_command = "SELECT nome_placa FROM Placas WHERE placa_id=?"
        c.execute(db_command, (board_id,))
        board_name = c.fetchone()[0]
        conn.commit()
        conn.close()
        return board_name
    except Exception as e:
        print()
        print("##################")
        print("Erro na func. pick_board_name: ")
        print(e)
        print("##################")

def pick_board_id_from_deffect(deffect):
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        db_command = "SELECT placa_id FROM Placas WHERE nome_placa=?"
        c.execute(db_command, (deffect,))
        board_id = c.fetchone()[0]
        conn.commit()
        conn.close()
        return board_name
    except Exception as e:
        print()
        print("##################")
        print("Erro na func. pick_board_name: ")
        print(e)
        print("##################")

def load_connector_from_board(board_id):
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        db_command = "SELECT conector FROM Placas where placa_id=?"
        c.execute(db_command, (board_id,))
        connector = c.fetchone()[0]
        conn.commit()
        conn.close()
        return connector
    except Exception as e:
        print()
        print("##################")
        print("Erro na func. load_connector_from_board: ")
        print(e)
        print("##################")



def load_connector_command(connector_id):
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        db_command = "SELECT byte1, byte2, byte3, byte4, byte5, byte6, byte7, byte8 FROM Conector WHERE conector_id=?"
        c.execute(db_command, (connector_id,))
        relay_matrix_command = list(c.fetchall()[0])
        conn.commit()
        conn.close()
        return relay_matrix_command
    except Exception as e:
        print()
        print("##################")
        print("Erro na func. load_connector_command: ")
        print(e)
        print("##################")
        return ''
def load_available_workbenches():
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        db_command = "SELECT bancada_nome FROM Bancada WHERE bancada_ocupada = 0 ORDER BY bancada_id"
        c.execute(db_command)
        workbenches = c.fetchall()
        conn.commit()
        conn.close()
        workbenches = [item[0] for item in workbenches]
        print("db: benches loaded")
        return workbenches
    except Exception as e:
        print()
        print("##################")
        print("Erro na func. load_connector_command: ")
        print(e)
        print("##################")
        return ''

def load_busy_workbenches():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    db_command = "SELECT bancada_nome FROM Bancada WHERE bancada_ocupada >= 1 ORDER BY bancada_id"
    c.execute(db_command)
    workbenches = c.fetchall()
    conn.commit()
    conn.close()
    workbenches = [item[0] for item in workbenches]
    print("db: benches loaded")
    return workbenches


def load_deffects(board_id):
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        db_command = "SELECT nome_defeito FROM Defeitos WHERE placa=?"
        c.execute(db_command, (board_id,))
        deffects = c.fetchall()
        deffects = [deffects[i][0] for i in range(len(deffects))]
        conn.commit()
        conn.close()
        return deffects
    except Exception as e:
        print()
        print("##################")
        print("Erro na func. load_deffects: ")
        print(e)
        print("##################")
        return ''

def pick_deffect_docs(deffect_name):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    db_command_1 = "SELECT descricao FROM Defeitos WHERE nome_defeito=?"
    db_command_2 = "SELECT conserto FROM Defeitos WHERE nome_defeito=?"

    c.execute(db_command_1, (deffect_name,))
    description = c.fetchone()[0]
    c.execute(db_command_2, (deffect_name,))
    fixing = c.fetchone()[0]

    conn.commit()
    conn.close()
    return [description, fixing]

def load_board_rows():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    db_command_1 = "SELECT * FROM Placas"
    c.execute(db_command_1,)
    rows = c.fetchall()
    #take only the value of connector id
    b_connectors = [ i[4] for i in rows ] # b_connectors = board_connectors, not dab_connectors
    #Create a request for every connector
    b_conn_name_req = ["SELECT nome_conector FROM Conector WHERE conector_id={}".format(i) for i in b_connectors]

    b_conn_names = []
    for req in b_conn_name_req:
        c.execute(req)
        b_conn_name = c.fetchone()[0]
        b_conn_names.append(b_conn_name)

    rows = [list(i) for i in rows]
    for i in range(len(rows)):
        rows[i][4] = b_conn_names[i]

    return rows

def delete_board_rows(board_ids_list=()):
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
    except Exception as e:
        print("-----")
        print("")
        print("Problems while trying to connect to sqlite3 DB")
        print("")
        print("-----")
    try:
        if len(board_ids_list) == 1:
            board_ids_list = "("+ board_ids_list[0] +")"

        db_command = "DELETE FROM Placas WHERE placa_id IN{}".format(board_ids_list)
        print(db_command)
        c.execute(db_command)
        conn.commit()
        conn.close()
    except Exception as e:
        print("-----")
        print("")
        print("Problems while trying to delete rows from Placas' table")
        print(e)
        print("")
        print("-----")

def set_workbench_as_busy(workbench_name):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    db_command = "UPDATE Bancada SET bancada_ocupada=1 WHERE bancada_nome=?"
    c.execute(db_command, (workbench_name,))
    conn.commit()
    conn.close()
def set_workbench_as_free(workbench_name):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    db_command = "UPDATE Bancada SET bancada_ocupada=0 WHERE bancada_nome=?"
    c.execute(db_command, (workbench_name,))
    conn.commit()
    conn.close()
