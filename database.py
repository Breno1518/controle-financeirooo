import sqlite3

conexao = sqlite3.connect('financeiro.db')

cursor = conexao.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS lancamentos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    descricao TEXT NOT NULL,
    valor REAL NOT NULL,
    tipo TEXT NOT NULL
)
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario TEXT NOT NULL UNIQUE,
    senha TEXT NOT NULL
)
''')
conexao.commit()
conexao.close()

print("Banco criado com sucesso!")