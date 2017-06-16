from application import db, Placa


def create_board(board_number):
    placa = Placa('nome');
    placa.id = board_number
    placa.nome_placa = "Placa "+str(board_number)
    db.session.add(board_number)

[create_board(i) for i in range(50)]

db.session.commit()
