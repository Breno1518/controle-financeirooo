from flask import Flask, render_template, request, redirect, session
import sqlite3
import matplotlib.pyplot as plt

app = Flask(__name__)
app.secret_key = '123456'
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        usuario = request.form['usuario']
        senha = request.form['senha']

        conexao = sqlite3.connect('financeiro.db')
        cursor = conexao.cursor()

        cursor.execute(
            "SELECT * FROM usuarios WHERE usuario = ? AND senha = ?",
            (usuario, senha)
        )

        usuario_encontrado = cursor.fetchone()

        conexao.close()

        if usuario_encontrado:
            session['usuario'] = usuario
            return redirect('/')

    return render_template('login.html')
@app.route('/', methods=['GET', 'POST'])
def home():
    if 'usuario' not in session:
        return redirect('/login')

    if request.method == 'POST':
        descricao = request.form['descricao']
        valor = request.form['valor']
        tipo = request.form['tipo']

        conexao = sqlite3.connect('financeiro.db')
        cursor = conexao.cursor()

        cursor.execute(
            "INSERT INTO lancamentos (descricao, valor, tipo) VALUES (?, ?, ?)",
            (descricao, valor, tipo)
        )

        conexao.commit()
        conexao.close()

    conexao = sqlite3.connect('financeiro.db')
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM lancamentos")
    lancamentos = cursor.fetchall()

    saldo = 0
    receitas = 0
    despesas = 0

    for lancamento in lancamentos:

        if lancamento[3] == "Receita":
            saldo += lancamento[2]
            receitas += lancamento[2]

        else:
            saldo -= lancamento[2]
            despesas += lancamento[2]
    plt.figure(figsize=(5, 5))

    plt.pie(
        [receitas, despesas],
        labels=['Receitas', 'Despesas'],
        autopct='%1.1f%%'
    )

    plt.title('Receitas x Despesas')

    plt.savefig('static/grafico.png')

    plt.close()
    conexao.close()

    return render_template(
    'index.html',
    lancamentos=lancamentos,
    saldo=saldo,
    receitas=receitas,
    despesas=despesas
)
@app.route('/excluir/<int:id>')
def excluir(id):

    conexao = sqlite3.connect('financeiro.db')
    cursor = conexao.cursor()

    cursor.execute(
        "DELETE FROM lancamentos WHERE id = ?",
        (id,)
    )

    conexao.commit()
    conexao.close()

    return redirect('/')
@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):

    conexao = sqlite3.connect('financeiro.db')
    cursor = conexao.cursor()

    if request.method == 'POST':

        descricao = request.form['descricao']
        valor = request.form['valor']
        tipo = request.form['tipo']

        cursor.execute(
            """
            UPDATE lancamentos
            SET descricao = ?, valor = ?, tipo = ?
            WHERE id = ?
            """,
            (descricao, valor, tipo, id)
        )

        conexao.commit()
        conexao.close()

        return redirect('/')

    cursor.execute(
        "SELECT * FROM lancamentos WHERE id = ?",
        (id,)
    )

    lancamento = cursor.fetchone()

    conexao.close()

    return render_template(
        'editar.html',
        lancamento=lancamento
    )
@app.route('/logout')
def logout():

    session.pop('usuario', None)

    return redirect('/login')
if __name__ == '__main__':
    app.run(debug=True)