import sqlite3

def save_connector(name, commands):
    try:
        conn = sqlite3.connect('db/banco_de_dados')
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


def save_board(name, fabric, board_type, connector):
    try:
        conn = sqlite3.connect('db/banco_de_dados')
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
        conn = sqlite3.connect('db/banco_de_dados')
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
        conn = sqlite3.connect('db/banco_de_dados')
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
        conn = sqlite3.connect('db/banco_de_dados')
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
        conn = sqlite3.connect('db/banco_de_dados')
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
        conn = sqlite3.connect('db/banco_de_dados')
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
        conn = sqlite3.connect('db/banco_de_dados')
        c = conn.cursor()
        db_command = "SELECT bancada_ip FROM Bancada WHERE bancada_nome=?"
        c.execute(db_command, (name,))
        workbench_ip = c.fetchone()[0]
        return workbench_ip
    except Exception as e:
        print()
        print("##################")
        print("Erro na func. pick_workbench_id: ")
        print(e)
        print("##################")


def load_connector_from_board(board_id):
    try:
        conn = sqlite3.connect('db/banco_de_dados')
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
        conn = sqlite3.connect('db/banco_de_dados')
        c = conn.cursor()
        db_command = "SELECT byte1, byte2, byte3, byte4, byte5, byte6, byte7, byte8 FROM Conector WHERE conector_id=?"
        c.execute(db_command, (connector_id,))
        relay_matrix_command = list(c.fetchall()[0])
        return relay_matrix_command
    except Exception as e:
        print()
        print("##################")
        print("Erro na func. load_connector_command: ")
        print(e)
        print("##################")
        return ''
def load_workbenches():
    try:
        conn = sqlite3.connect('db/banco_de_dados')
        c = conn.cursor()
        db_command = "SELECT bancada_nome FROM Bancada ORDER BY bancada_id"
        c.execute(db_command)
        workbenches = c.fetchall()
        conn.commit()
        conn.close()
        print("db: benches loaded")
        return workbenches
    except Exception as e:
        print()
        print("##################")
        print("Erro na func. load_connector_command: ")
        print(e)
        print("##################")
        return ''
