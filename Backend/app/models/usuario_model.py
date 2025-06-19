import sqlite3
from app.db.database import get_db_connection
from werkzeug.security import generate_password_hash

def create_user(data):
    conn = None
    try:
        nome = data['nome_completo']
        email = data['email']
        senha_hash = generate_password_hash(data['senha'])
        telefone = data.get('telefone')
        endereco = data.get('endereco')
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO Usuario (nome_completo, email, senha, telefone, endereco) VALUES (?, ?, ?, ?, ?)',
            (nome, email, senha_hash, telefone, endereco)
        )
        conn.commit()
        return cursor.lastrowid
    finally:
        if conn:
            conn.close()

def get_all_users():
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome_completo, email, telefone, endereco, data_cadastro FROM Usuario")
        usuarios = cursor.fetchall()
        return [dict(usuario) for usuario in usuarios]
    finally:
        if conn:
            conn.close()

def get_user_by_id(user_id):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome_completo, email, telefone, endereco, data_cadastro FROM Usuario WHERE id = ?", (user_id,))
        usuario = cursor.fetchone()
        if usuario:
            return dict(usuario)
        return None
    finally:
        if conn:
            conn.close()