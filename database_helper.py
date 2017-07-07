import sqlite3

def save_connector(name, commands):
    conn = sqlite3.connect('db/banco_de_dados')
    c = conn.cursor()
    db_command = "INSERT INTO Conector (nome_conector, byte1, byte2, byte3, byte4, byte5, byte6, byte7, byte8) VALUES('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}')"\
            .format(name, commands[0], commands[1], commands[2], commands[3], commands[4], commands[5], commands[6], commands[7])
    c.execute(db_command)
    conn.commit()
    conn.close()
    print("db: "+ name + " saved..")

def load_boards():
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

def load_connectors():
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
