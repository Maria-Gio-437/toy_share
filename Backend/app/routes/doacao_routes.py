from flask import Blueprint, request, jsonify
from app.models import doacao_model
from app.utils.decorators import token_required

doacoes_bp = Blueprint('doacoes_bp', __name__)

@doacoes_bp.route('/doacoes', methods=['POST'])
@token_required 
def criar_doacao(current_user):
    dados = request.get_json()

    if not dados or 'titulo' not in dados or 'brinquedos' not in dados or not isinstance(dados['brinquedos'], list):
        return jsonify({'erro': 'Dados inválidos. É necessário um título e uma lista de brinquedos.'}), 400

    try:
        user_id = current_user['id']
        doacao_id = doacao_model.create_donation(dados, user_id)
        
        return jsonify({
            'mensagem': 'Doação criada com sucesso!',
            'doacao_id': doacao_id
        }), 201

    except Exception as e:
        return jsonify({'erro': f'Ocorreu um erro ao criar a doação: {e}'}), 500

@doacoes_bp.route('/doacoes', methods=['GET'])
@token_required # Protege a rota! O usuário só pode ver suas próprias doações.
def ver_minhas_doacoes(current_user):
    """
    Endpoint para o usuário logado ver seu histórico de doações.
    """
    try:
        user_id = current_user['id']
        historico = doacao_model.get_donations_by_user_id(user_id)
        return jsonify(historico), 200
    except Exception as e:
        return jsonify({'erro': f'Ocorreu um erro ao buscar o histórico: {e}'}), 500

@doacoes_bp.route('/doacoes/<int:doacao_id>/brinquedos', methods=['POST'])
@token_required # Rota protegida
def adicionar_brinquedos_a_doacao(current_user, doacao_id):
    """
    Endpoint para adicionar um ou mais brinquedos a uma doação existente.
    """
    # 1. Verificar se a doação existe
    doacao = doacao_model.get_donation_by_id(doacao_id)
    if not doacao:
        return jsonify({'erro': 'Doação não encontrada.'}), 404

    # 2. Verificar se o usuário logado é o dono da doação
    if doacao['usuario_id'] != current_user['id']:
        return jsonify({'erro': 'Acesso negado. Você não é o dono desta doação.'}), 403 # 403 Forbidden

    # 3. Pegar os dados dos novos brinquedos da requisição
    dados = request.get_json()
    if not dados or 'brinquedos' not in dados or not isinstance(dados['brinquedos'], list) or not dados['brinquedos']:
        return jsonify({'erro': 'Dados inválidos. É necessário fornecer uma lista de brinquedos.'}), 400

    # 4. Chamar o modelo para adicionar os brinquedos
    try:
        doacao_model.add_toys_to_donation(doacao_id, dados['brinquedos'])
        return jsonify({'mensagem': 'Brinquedos adicionados com sucesso à doação!'}), 200 # 200 OK
    except Exception as e:
        return jsonify({'erro': f'Ocorreu um erro ao adicionar os brinquedos: {e}'}), 500
    
@doacoes_bp.route('/doacoes/<int:doacao_id>/brinquedos', methods=['POST'])
@token_required # Rota protegida
def adicionar_brinquedos_a_doacao(current_user, doacao_id):
    """
    Endpoint para adicionar um ou mais brinquedos a uma doação existente.
    """
    # 1. Verificar se a doação existe
    doacao = doacao_model.get_donation_by_id(doacao_id)
    if not doacao:
        return jsonify({'erro': 'Doação não encontrada.'}), 404

    # 2. Verificar se o usuário logado é o dono da doação
    if doacao['usuario_id'] != current_user['id']:
        return jsonify({'erro': 'Acesso negado. Você não é o dono desta doação.'}), 403 # 403 Forbidden

    # 3. Pegar os dados dos novos brinquedos da requisição
    dados = request.get_json()
    if not dados or 'brinquedos' not in dados or not isinstance(dados['brinquedos'], list) or not dados['brinquedos']:
        return jsonify({'erro': 'Dados inválidos. É necessário fornecer uma lista de brinquedos.'}), 400

    # 4. Chamar o modelo para adicionar os brinquedos
    try:
        doacao_model.add_toys_to_donation(doacao_id, dados['brinquedos'])
        return jsonify({'mensagem': 'Brinquedos adicionados com sucesso à doação!'}), 200 # 200 OK
    except Exception as e:
        return jsonify({'erro': f'Ocorreu um erro ao adicionar os brinquedos: {e}'}), 500