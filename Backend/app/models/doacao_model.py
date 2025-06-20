import sqlite3
from app.db.database import get_db_connection

def create_donation(data, user_id):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('BEGIN')

        titulo = data['titulo']
        descricao = data.get('descricao', '') # opcional

        cursor.execute(
            'INSERT INTO Doacao (usuario_id, titulo, descricao) VALUES (?, ?, ?)',
            (user_id, titulo, descricao)
        )
        doacao_id = cursor.lastrowid

        brinquedos_para_inserir = []
        for brinquedo in data['brinquedos']:
            brinquedo_data = (
                doacao_id,
                brinquedo['nome'],
                brinquedo.get('descricao', ''),
                brinquedo.get('foto_url', None),
                brinquedo.get('quantidade_ofertada', 1),
                brinquedo.get('categoria', None),
            )
            brinquedos_para_inserir.append(brinquedo_data)
        
        cursor.executemany(
            'INSERT INTO Brinquedo (doacao_id, nome, descricao, foto_url, quantidade_ofertada, categoria) VALUES (?, ?, ?, ?, ?, ?)',
            brinquedos_para_inserir
        )

        conn.commit()
        return doacao_id

    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            conn.close()

def get_donations_by_user_id(user_id):
    """Retorna o histórico de doações de um usuário específico."""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM Doacao WHERE usuario_id = ?", (user_id,))
        doacoes_rows = cursor.fetchall()

        doacoes = [dict(row) for row in doacoes_rows]

        for doacao in doacoes:
            cursor.execute("SELECT * FROM Brinquedo WHERE doacao_id = ?", (doacao['id'],))
            brinquedos_rows = cursor.fetchall()
            doacao['brinquedos'] = [dict(row) for row in brinquedos_rows]
        
        return doacoes
    finally:
        if conn:
            conn.close()

def get_donation_by_id(doacao_id):
    """Busca os detalhes de uma única doação pelo seu ID."""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Doacao WHERE id = ?", (doacao_id,))
        doacao = cursor.fetchone()
        if doacao:
            return dict(doacao)
        return None
    finally:
        if conn:
            conn.close()

def add_toys_to_donation(doacao_id, brinquedos_data):
    """Adiciona uma lista de brinquedos a uma doação existente."""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        brinquedos_para_inserir = []
        for brinquedo in brinquedos_data:
            brinquedo_tupla = (
                doacao_id,
                brinquedo['nome'],
                brinquedo.get('descricao', ''),
                brinquedo.get('foto_url', None),
                brinquedo.get('quantidade_ofertada', 1),
                brinquedo.get('categoria', None),
            )
            brinquedos_para_inserir.append(brinquedo_tupla)
        
        cursor.executemany(
            'INSERT INTO Brinquedo (doacao_id, nome, descricao, foto_url, quantidade_ofertada, categoria) VALUES (?, ?, ?, ?, ?, ?)',
            brinquedos_para_inserir
        )
        conn.commit()
        return True # Retorna sucesso
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            conn.close()