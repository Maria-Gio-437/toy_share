from flask import Blueprint, request, jsonify, current_app
import datetime
import jwt
from werkzeug.security import check_password_hash # Importe esta função
from app.models import usuario_model
from app.utils.decorators import token_required # Importe nosso decorator!

usuarios_bp = Blueprint('usuarios_bp', __name__)

@usuarios_bp.route('/login', methods=['POST'])
def login():
    auth = request.get_json()

    if not auth or not auth.get('email') or not auth.get('senha'):
        return jsonify({'mensagem': 'Email e senha são obrigatórios!'}), 400

    user = usuario_model.get_user_by_email(auth.get('email'))

    if not user:
        return jsonify({'mensagem': 'Credenciais inválidas!'}), 401

    # Compara a senha enviada com o hash salvo no banco
    if check_password_hash(user['senha'], auth.get('senha')):
        # Se a senha estiver correta, gera o token
        token = jwt.encode({
            'user_id': user['id'],
            'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=24) # Token expira em 24 horas
        }, current_app.config['SECRET_KEY'], algorithm="HS256")

        return jsonify({'token': token}), 200

    return jsonify({'mensagem': 'Credenciais inválidas!'}), 401


@usuarios_bp.route('/perfil', methods=['GET'])
@token_required # Aplicamos o decorator aqui!
def ver_perfil(current_user):
    return jsonify(current_user), 200

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