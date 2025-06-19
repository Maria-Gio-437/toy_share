from flask import Blueprint, request, jsonify
from app.models import usuario_model

usuarios_bp = Blueprint('usuarios_bp', __name__)

@usuarios_bp.route('/usuarios', methods=['POST'])
def cadastrar_usuario():
    dados = request.get_json()

    if not dados or not 'nome_completo' in dados or not 'email' in dados or not 'senha' in dados:
        return jsonify({'erro': 'Dados obrigatórios não fornecidos'}), 400
    
    try:
        novo_usuario_id = usuario_model.create_user(dados)
        return jsonify({
            'mensagem': 'Usuário cadastrado com sucesso!',
            'usuario_id': novo_usuario_id
        }), 201
    except Exception as e:
        return jsonify({'erro': f'Não foi possível criar o usuário: {e}'}), 409


@usuarios_bp.route('/usuarios', methods=['GET'])
def listar_usuarios():
    try:
        usuarios = usuario_model.get_all_users()
        return jsonify(usuarios), 200
    except Exception as e:
        return jsonify({'erro': f'Ocorreu um erro no servidor: {e}'}), 500


@usuarios_bp.route('/usuarios/<int:id>', methods=['GET'])
def buscar_usuario(id):
    try:
        usuario = usuario_model.get_user_by_id(id)
        if usuario is None:
            return jsonify({'erro': 'Usuário não encontrado'}), 404
        
        return jsonify(usuario), 200
    except Exception as e:
        return jsonify({'erro': f'Ocorreu um erro no servidor: {e}'}), 500