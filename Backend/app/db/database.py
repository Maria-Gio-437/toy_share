import sqlite3

# Rota para o banco de dados
DATABASE_URL = 'database.sqlite'

def get_db_connection():
    """Cria e retorna uma conexão com o banco de dados."""
    conn = sqlite3.connect(DATABASE_URL)
    conn.row_factory = sqlite3.Row
    return conn