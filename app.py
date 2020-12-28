from flask import Flask, request, render_template, redirect, url_for

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__) # Inicializa a aplicação
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

db = SQLAlchemy(app)

class Compra(db.Model):
    __tablename__ = 'compra'

    _id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    nome = db.Column(db.String)
    quantidade = db.Column(db.Integer)
    preco = db.Column(db.Integer)
    pmedio = db.Column(db.Integer)

    def __init__(self, nome, quantidade, preco, pmedio):
        self.nome = nome
        self.quantidade = quantidade
        self.preco = preco
        self.pmedio = pmedio

class Estoque(db.Model):
    __tablename__ = 'estoque'

    nome = db.Column(db.String,primary_key=True)
    quantidade = db.Column(db.Integer)
    preco = db.Column(db.Integer)
    pmedio = db.Column(db.Integer)

    def __init__(self, nome, quantidade, preco, pmedio):
        self.nome = nome
        self.quantidade = quantidade
        self.preco = preco
        self.pmedio = pmedio
db.create_all()

data = []
@app.route("/index") # Nova rota
def index():
    return render_template("index.html")

@app.route("/comprar") # Nova rota
def comprar():
    return render_template("comprar.html",data=data)


@app.route("/cadastrar", methods=['GET','POST']) # Nova rota
def cadastrar():
    erro = None
    if request.method == "POST":
        nome = request.form.get("nome")

        if nome:
            if nome not in data:
                data.append(nome)
            else:
                erro="Produto ja cadastrado"

    return render_template("cadastrar.html", erro=erro)

@app.route("/compra", methods=['GET','POST']) # Nova rota
def compra():
    pmedio = None

    if request.method == "POST":
        nome = request.form.get("comp_select")
        quantidade = request.form.get("quantidade")
        preco = request.form.get("preço")

        if nome and quantidade and preco:
            preco = float(preco)
            quantidade = int(quantidade)
            pmedio = preco/quantidade

            p = Compra(nome, quantidade, preco, pmedio)
            db.session.add(p)
            db.session.commit()

            e = Estoque(nome, quantidade, preco, pmedio)

            if db.session.query(db.exists().where(Estoque.nome == e.nome)).scalar():
                e.quantidade += Estoque.quantidade
                e.preco += Estoque.preco
                e.pmedio = e.preco/e.quantidade

                estoque =Estoque.query.filter_by(nome=e.nome).first()

                db.session.delete(estoque)
                db.session.add(e)
                db.session.commit()
            else:
                db.session.add(e)
                db.session.commit()

    return redirect(url_for('index'))

@app.route("/estoque") # Nova rota
def estoque():
    estoque = Estoque.query.all()
    return render_template("estoque.html", estoque=estoque)

@app.route("/historico") # Nova rota
def historico():
    compras = Compra.query.all()
    return render_template("historico.html", compras=compras)

if __name__ == '__main__':
  app.run() # Executa a aplicação
