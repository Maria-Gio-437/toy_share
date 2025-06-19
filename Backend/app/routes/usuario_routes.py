from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
import sqlite3

from app.db.database import get_db_connection # Import para lidar com conexão com o banco de dados

usuarios_bp = Blueprint('usuarios_bp', __name__)

@usuarios_bp.route('/usuarios', methods=['POST'])
def cadastrar_usuario():
    dados = request.get_json()

    # Validação dos campos obrigatórios
    if not dados or not 'nome_completo' in dados or not 'email' in dados or not 'senha' in dados:
        return jsonify({'erro': 'Dados obrigatórios (nome_completo, email, senha) não fornecidos'}), 400

    # Extração dos dados (obrigatórios e opcionais)
    nome = dados['nome_completo']
    email = dados['email']
    senha = dados['senha']
    
    # .get() para campos opcionais. Se a chave não existir no JSON, o valor será None.
    telefone = dados.get('telefone')
    endereco = dados.get('endereco')

    senha_hash = generate_password_hash(senha)

    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            'INSERT INTO Usuario (nome_completo, email, senha, telefone, endereco) VALUES (?, ?, ?, ?, ?)',
            (nome, email, senha_hash, telefone, endereco)
        )
        
        conn.commit()
        
        novo_usuario_id = cursor.lastrowid
        
        return jsonify({
            'mensagem': 'Usuário cadastrado com sucesso!',
            'usuario_id': novo_usuario_id
        }), 201

    except sqlite3.IntegrityError:
        return jsonify({'erro': 'Este e-mail já está cadastrado'}), 409
        
    except Exception as e:
        return jsonify({'erro': f'Ocorreu um erro no servidor: {e}'}), 500

    finally:
        if conn:
            conn.close()

@usuarios_bp.route('/usuarios', methods=['GET'])
def listar_usuarios():
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome_completo, email, telefone, endereco, data_cadastro FROM Usuario")
        usuarios = cursor.fetchall()
        
        lista_de_usuarios = [dict(usuario) for usuario in usuarios]
                
        return jsonify(lista_de_usuarios), 200

    except Exception as e:
        return jsonify({'erro': f'Ocorreu um erro no servidor: {e}'}), 500
    finally:
        if conn:
            conn.close()

            
@usuarios_bp.route('/usuarios/<int:id>', methods=['GET'])
def buscar_usuario(id):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, nome_completo, email, telefone, endereco, data_cadastro FROM Usuario WHERE id = ?", (id,))
        usuario = cursor.fetchone()
        
        if usuario is None:
            return jsonify({'erro': 'Usuário não encontrado'}), 404
        
        return jsonify(dict(usuario)), 200

    except Exception as e:
        return jsonify({'erro': f'Ocorreu um erro no servidor: {e}'}), 500
    finally:
        if conn:
            conn.close()