from functools import wraps
from flask import request, jsonify, current_app
import jwt
from app.models import usuario_model

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # O token é enviado no header 'Authorization' no formato 'Bearer <token>'
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            token_parts = auth_header.split()
            if len(token_parts) == 2 and token_parts[0].lower() == 'bearer':
                token = token_parts[1]

        if not token:
            return jsonify({'mensagem': 'Token não fornecido!'}), 401

        try:
            # Decodifica o token usando a mesma SECRET_KEY
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            # Busca o usuário no banco de dados para garantir que ele existe
            current_user = usuario_model.get_user_by_id(data['user_id'])
            if current_user is None:
                return jsonify({'mensagem': 'Token inválido!'}), 401
        except jwt.ExpiredSignatureError:
            return jsonify({'mensagem': 'Token expirou!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'mensagem': 'Token inválido!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated