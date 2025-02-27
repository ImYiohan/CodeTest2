/projeto
│── app.py
│── templates/
│   │── index.html
│   │── configuracoes.html
│   └── recuperacao.html
│── static/
│   └── style.css
│── usuarios.db

import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

def criar_banco():
    conexao = sqlite3.connect("usuarios.db")
    cursor = conexao.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                        nome TEXT PRIMARY KEY,
                        senha TEXT NOT NULL)''')
    
    usuarios = [
        ("Gabriel", "Sweet3733"),
        ("Camila", "679051"),
        ("Felipe", "graciler"),
        ("Erik", "solaris"),
        ("Leonardo", "licaria")
    ]
    
    cursor.executemany("INSERT OR IGNORE INTO usuarios (nome, senha) VALUES (?, ?)", usuarios)
    conexao.commit()
    conexao.close()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    nome = request.form["nome"]
    senha = request.form["senha"]
    if verificar_usuario(nome, senha):
        return redirect(url_for("configuracoes"))
    return "Nome de usuário ou senha incorretos."

def verificar_usuario(nome, senha):
    conexao = sqlite3.connect("usuarios.db")
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE nome = ? AND senha = ?", (nome, senha))
    usuario = cursor.fetchone()
    conexao.close()
    return usuario is not None

@app.route("/configuracoes")
def configuracoes():
    return render_template("configuracoes.html")

@app.route("/recuperacao", methods=["GET", "POST"])
def recuperacao():
    if request.method == "POST":
        nome = request.form["nome"]
        nova_senha = request.form["nova_senha"]
        conexao = sqlite3.connect("usuarios.db")
        cursor = conexao.cursor()
        cursor.execute("UPDATE usuarios SET senha = ? WHERE nome = ?", (nova_senha, nome))
        conexao.commit()
        conexao.close()
        return "Senha alterada com sucesso!"
    return render_template("recuperacao.html")

if __name__ == "__main__":
    criar_banco()
    app.run(debug=True)

<!DOCTYPE html>
<html>
<head>
    <title>Login</title>
</head>
<body>
    <h2>Login</h2>
    <form action="/login" method="post">
        Nome: <input type="text" name="nome" required><br>
        Senha: <input type="password" name="senha" required><br>
        <input type="submit" value="Entrar">
    </form>
    <a href="/recuperacao">Esqueceu sua senha?</a>
</body>
</html>

<!DOCTYPE html>
<html>
<head>
    <title>Configurações</title>
</head>
<body>
    <h2>Bem-vindo às Configurações</h2>
    <p>Aqui você pode modificar suas preferências.</p>
    <a href="/">Sair</a>
</body>
</html>

<!DOCTYPE html>
<html>
<head>
    <title>Recuperação de Conta</title>
</head>
<body>
    <h2>Recuperação de Conta</h2>
    <form action="/recuperacao" method="post">
        Nome: <input type="text" name="nome" required><br>
        Nova Senha: <input type="password" name="nova_senha" required><br>
        <input type="submit" value="Alterar Senha">
    </form>
</body>
</html>


















github


