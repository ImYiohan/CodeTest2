import os
import sqlite3
import secrets
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "super_secret_key"

# Caminho do banco de dados
DB_PATH = os.path.join(os.getcwd(), "usuarios.db")

def criar_banco():
    conexao = sqlite3.connect(DB_PATH)
    cursor = conexao.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                        nome TEXT PRIMARY KEY,
                        senha TEXT NOT NULL)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS tokens (
                        nome TEXT PRIMARY KEY,
                        token TEXT NOT NULL)''')
    
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

def verificar_usuario(nome, senha):
    conexao = sqlite3.connect(DB_PATH)
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE nome = ? AND senha = ?", (nome, senha))
    usuario = cursor.fetchone()
    conexao.close()
    return usuario is not None

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    nome = request.form["nome"]
    senha = request.form["senha"]
    if verificar_usuario(nome, senha):
        return redirect(url_for("configuracoes"))
    flash("Nome de usuário ou senha incorretos.")
    return redirect(url_for("index"))

@app.route("/configuracoes")
def configuracoes():
    return render_template("configuracoes.html")

@app.route("/recuperacao", methods=["GET", "POST"])
def recuperacao():
    if request.method == "POST":
        nome = request.form["nome"]
        conexao = sqlite3.connect(DB_PATH)
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE nome = ?", (nome,))
        usuario = cursor.fetchone()
        if usuario:
            token = secrets.token_hex(8)
            cursor.execute("INSERT OR REPLACE INTO tokens (nome, token) VALUES (?, ?)", (nome, token))
            conexao.commit()
            flash(f"Use este token para redefinir sua senha: {token}")
        else:
            flash("Usuário não encontrado.")
        conexao.close()
        return redirect(url_for("recuperacao"))
    return render_template("recuperacao.html")

@app.route("/reset_senha", methods=["POST"])
def reset_senha():
    nome = request.form["nome"]
    token = request.form["token"]
    nova_senha = request.form["nova_senha"]
    
    conexao = sqlite3.connect(DB_PATH)
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM tokens WHERE nome = ? AND token = ?", (nome, token))
    token_valido = cursor.fetchone()
    
    if token_valido:
        cursor.execute("UPDATE usuarios SET senha = ? WHERE nome = ?", (nova_senha, nome))
        cursor.execute("DELETE FROM tokens WHERE nome = ?", (nome,))
        conexao.commit()
        flash("Senha redefinida com sucesso!")
    else:
        flash("Token inválido ou expirado.")
    
    conexao.close()
    return redirect(url_for("index"))

if __name__ == "__main__":
    criar_banco()
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
