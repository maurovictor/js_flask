from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)



class Placa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_placa = db.Column(db.String(100), unique=True)

    def __init__(self, placa):
        self.nome_placa = placa

    def __repr__(self):
        return 'Placa '

db.create_all()

@app.route('/')
def pagina_teste():
    return render_template('principal.html')
