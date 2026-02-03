# api.py
from flask import Flask, jsonify, request, render_template
from flask_socketio import SocketIO, emit, disconnect
import mysql.connector
import jwt
import bcrypt
from datetime import datetime, timedelta
from functools import wraps
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# A variável 'app' precisa ser definida antes de qualquer rota.
app = Flask(__name__)

# Configurar SocketIO para WebSocket
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# -----------------
# Configuração do banco de dados MySQL
# -----------------
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')
DB_NAME = os.getenv('DB_NAME', 'SistemasCorporativos')

# -----------------
# Configuração JWT
# -----------------
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'sua_chave_secreta_super_segura_aqui')
JWT_ALGORITHM = os.getenv('JWT_ALGORITHM', 'HS256')
JWT_EXPIRATION_HOURS = int(os.getenv('JWT_EXPIRATION_HOURS', '24'))

# Função para conectar ao banco de dados
def get_db_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

# -----------------
# Funções de Autenticação
# -----------------
def gerar_token(usuario_id, email):
    """Gera um token JWT para o usuário"""
    payload = {
        'usuario_id': usuario_id,
        'email': email,
        'exp': datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS),
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

def verificar_token(token):
    """Verifica se o token JWT é válido"""
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def hash_senha(senha):
    """Gera hash da senha"""
    return bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verificar_senha(senha, hash_senha):
    """Verifica se a senha confere com o hash"""
    return bcrypt.checkpw(senha.encode('utf-8'), hash_senha.encode('utf-8'))

def emitir_notificacao(usuario_id, tipo, mensagem, dados=None):
    """Emite notificação em tempo real para um usuário específico"""
    payload = {
        'tipo': tipo,
        'mensagem': mensagem,
        'timestamp': datetime.utcnow().isoformat(),
        'dados': dados or {}
    }
    socketio.emit('notificacao', payload, room=f'user_{usuario_id}')

# -----------------
# Decorador para proteger rotas
# -----------------
def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        
        # Verificar se o token está no header Authorization
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]  # Formato: "Bearer <token>"
            except IndexError:
                return jsonify({'erro': 'Token mal formatado'}), 401
        
        if not token:
            return jsonify({'erro': 'Token de acesso necessário'}), 401
        
        payload = verificar_token(token)
        if payload is None:
            return jsonify({'erro': 'Token inválido ou expirado'}), 401
        
        # Adicionar informações do usuário ao request
        request.usuario_atual = {
            'usuario_id': payload['usuario_id'],
            'email': payload['email']
        }
        
        return f(*args, **kwargs)
    return decorator

# -----------------
# Rotas de Autenticação
# -----------------
@app.route('/registro', methods=['POST'])
def registro():
    """Registra um novo usuário"""
    try:
        data = request.get_json()
        email = data.get('email')
        senha = data.get('senha')
        nome = data.get('nome')
        
        if not all([email, senha, nome]):
            return jsonify({"erro": "Email, senha e nome são obrigatórios"}), 400
        
        if len(senha) < 6:
            return jsonify({"erro": "Senha deve ter pelo menos 6 caracteres"}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Verificar se email já existe
        cursor.execute("SELECT UsuarioID FROM Usuarios WHERE Email = %s", (email,))
        if cursor.fetchone():
            cursor.close()
            conn.close()
            return jsonify({"erro": "Email já cadastrado"}), 409
        
        # Criar novo usuário
        senha_hash = hash_senha(senha)
        cursor.execute(
            "INSERT INTO Usuarios (Email, SenhaHash, Nome) VALUES (%s, %s, %s)",
            (email, senha_hash, nome)
        )
        conn.commit()
        usuario_id = cursor.lastrowid
        
        cursor.close()
        conn.close()
        
        # Gerar token para o novo usuário
        token = gerar_token(usuario_id, email)
        
        return jsonify({
            "mensagem": "Usuário registrado com sucesso",
            "token": token,
            "usuario": {
                "id": usuario_id,
                "email": email,
                "nome": nome
            }
        }), 201
        
    except mysql.connector.Error as ex:
        return jsonify({"erro": f"Erro ao registrar usuário: {ex}"}), 500

@app.route('/login', methods=['POST'])
def login():
    """Autentica um usuário e retorna um token JWT"""
    try:
        data = request.get_json()
        email = data.get('email')
        senha = data.get('senha')
        
        if not all([email, senha]):
            return jsonify({"erro": "Email e senha são obrigatórios"}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Buscar usuário
        cursor.execute(
            "SELECT UsuarioID, Email, SenhaHash, Nome FROM Usuarios WHERE Email = %s AND Ativo = TRUE",
            (email,)
        )
        usuario = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if not usuario:
            return jsonify({"erro": "Email ou senha incorretos"}), 401
        
        # Verificar senha
        if not verificar_senha(senha, usuario['SenhaHash']):
            return jsonify({"erro": "Email ou senha incorretos"}), 401
        
        # Gerar token
        token = gerar_token(usuario['UsuarioID'], usuario['Email'])
        
        return jsonify({
            "mensagem": "Login realizado com sucesso",
            "token": token,
            "usuario": {
                "id": usuario['UsuarioID'],
                "email": usuario['Email'],
                "nome": usuario['Nome']
            }
        }), 200
        
    except mysql.connector.Error as ex:
        return jsonify({"erro": f"Erro ao fazer login: {ex}"}), 500

@app.route('/perfil', methods=['GET'])
@token_required
def perfil():
    """Retorna informações do usuário logado"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute(
            "SELECT UsuarioID, Email, Nome, DataCriacao FROM Usuarios WHERE UsuarioID = %s",
            (request.usuario_atual['usuario_id'],)
        )
        usuario = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if not usuario:
            return jsonify({"erro": "Usuário não encontrado"}), 404
        
        return jsonify({
            "usuario": {
                "id": usuario['UsuarioID'],
                "email": usuario['Email'],
                "nome": usuario['Nome'],
                "data_criacao": usuario['DataCriacao'].isoformat()
            }
        }), 200
        
    except mysql.connector.Error as ex:
        return jsonify({"erro": f"Erro ao buscar perfil: {ex}"}), 500

# -----------------
# Rota para a página de testes (página principal)
# -----------------
@app.route('/')
def home():
    return render_template('index.html')

# -----------------
# Rota para exibir todas as movimentações (PROTEGIDA)
# -----------------
@app.route('/movimentacoes', methods=['GET'])
@token_required
def get_movimentacoes():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Buscar apenas movimentações dos correntistas do usuário logado
        cursor.execute("""
            SELECT v.* FROM vwExtrato v
            INNER JOIN Correntistas c ON v.CorrentistaID = c.CorrentistaID
            WHERE c.UsuarioID = %s
            ORDER BY v.DataOperacao DESC
        """, (request.usuario_atual['usuario_id'],))
        
        movimentacoes = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(movimentacoes)
    except mysql.connector.Error as ex:
        return jsonify({"erro": f"Erro ao conectar ou consultar o banco de dados: {ex}"}), 500

# -----------------
# Rota para exibir o extrato de movimentações de um correntista (PROTEGIDA)
# -----------------
@app.route('/extrato/<int:correntista_id>', methods=['GET'])
@token_required
def get_extrato(correntista_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Verificar se o correntista pertence ao usuário logado
        cursor.execute(
            "SELECT UsuarioID FROM Correntistas WHERE CorrentistaID = %s",
            (correntista_id,)
        )
        correntista = cursor.fetchone()
        
        if not correntista or correntista['UsuarioID'] != request.usuario_atual['usuario_id']:
            cursor.close()
            conn.close()
            return jsonify({"erro": "Correntista não encontrado ou não autorizado"}), 403
        
        cursor.execute("SELECT * FROM vwExtrato WHERE CorrentistaID = %s ORDER BY DataOperacao DESC", (correntista_id,))
        extrato = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(extrato)
    except mysql.connector.Error as ex:
        return jsonify({"erro": f"Erro ao buscar extrato: {ex}"}), 500

# -----------------
# Rota para listar correntistas do usuário logado
# -----------------
@app.route('/correntistas', methods=['GET'])
@token_required
def get_correntistas():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute(
            "SELECT CorrentistaID, NomeCorrentista, Saldo FROM Correntistas WHERE UsuarioID = %s",
            (request.usuario_atual['usuario_id'],)
        )
        correntistas = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(correntistas)
    except mysql.connector.Error as ex:
        return jsonify({"erro": f"Erro ao buscar correntistas: {ex}"}), 500

# -----------------
# Função auxiliar para verificar se correntista pertence ao usuário
# -----------------
def verificar_correntista_usuario(correntista_id, usuario_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT UsuarioID FROM Correntistas WHERE CorrentistaID = %s",
        (correntista_id,)
    )
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result and result[0] == usuario_id

# -----------------
# Rota para Operação de Pagamento (PROTEGIDA)
# -----------------
@app.route('/pagamento', methods=['POST'])
@token_required
def pagar():
    try:
        data = request.get_json()
        correntista_id = data.get('correntista_id')
        valor = data.get('valor')
        descricao = data.get('descricao')

        if not all([correntista_id, valor, descricao]):
            return jsonify({"erro": "Dados incompletos"}), 400

        if valor <= 0:
            return jsonify({"erro": "Valor deve ser positivo"}), 400

        # Verificar se o correntista pertence ao usuário logado
        if not verificar_correntista_usuario(correntista_id, request.usuario_atual['usuario_id']):
            return jsonify({"erro": "Correntista não encontrado ou não autorizado"}), 403

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.callproc('spPagar', (correntista_id, valor, descricao))
        conn.commit()
        cursor.close()
        conn.close()
        
        # Emitir notificação WebSocket
        emitir_notificacao(
            request.usuario_atual['usuario_id'],
            'pagamento',
            f'Pagamento de R$ {valor:.2f} realizado com sucesso',
            {'valor': valor, 'descricao': descricao, 'correntista_id': correntista_id}
        )

        return jsonify({"mensagem": "Pagamento realizado com sucesso"}), 201
    except mysql.connector.Error as ex:
        return jsonify({"erro": f"Erro ao realizar pagamento: {ex}"}), 500

# -----------------
# Rota para Operação de Transferência (PROTEGIDA)
# -----------------
@app.route('/transferencia', methods=['POST'])
@token_required
def transferir():
    try:
        data = request.get_json()
        origem_id = data.get('correntista_id_origem')
        destino_id = data.get('correntista_id_destino')
        valor = data.get('valor')

        if not all([origem_id, destino_id, valor]):
            return jsonify({"erro": "Dados incompletos"}), 400

        if valor <= 0:
            return jsonify({"erro": "Valor deve ser positivo"}), 400

        if origem_id == destino_id:
            return jsonify({"erro": "Não é possível transferir para a mesma conta"}), 400

        # Verificar se o correntista de origem pertence ao usuário logado
        if not verificar_correntista_usuario(origem_id, request.usuario_atual['usuario_id']):
            return jsonify({"erro": "Correntista de origem não encontrado ou não autorizado"}), 403

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.callproc('spTransferir', (origem_id, valor, destino_id))
        conn.commit()
        cursor.close()
        conn.close()
        
        # Emitir notificação WebSocket
        emitir_notificacao(
            request.usuario_atual['usuario_id'],
            'transferencia',
            f'Transferência de R$ {valor:.2f} realizada com sucesso',
            {'valor': valor, 'origem_id': origem_id, 'destino_id': destino_id}
        )

        return jsonify({"mensagem": "Transferência realizada com sucesso"}), 201
    except mysql.connector.Error as ex:
        return jsonify({"erro": f"Erro ao realizar transferência: {ex}"}), 500

# -----------------
# Rota para Operação de Saque (PROTEGIDA)
# -----------------
@app.route('/saque', methods=['POST'])
@token_required
def sacar():
    try:
        data = request.get_json()
        correntista_id = data.get('correntista_id')
        valor = data.get('valor')

        if not all([correntista_id, valor]):
            return jsonify({"erro": "Dados incompletos"}), 400

        if valor <= 0:
            return jsonify({"erro": "Valor deve ser positivo"}), 400

        # Verificar se o correntista pertence ao usuário logado
        if not verificar_correntista_usuario(correntista_id, request.usuario_atual['usuario_id']):
            return jsonify({"erro": "Correntista não encontrado ou não autorizado"}), 403

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.callproc('spSacar', (correntista_id, valor))
        conn.commit()
        cursor.close()
        conn.close()
        
        # Emitir notificação WebSocket
        emitir_notificacao(
            request.usuario_atual['usuario_id'],
            'saque',
            f'Saque de R$ {valor:.2f} realizado com sucesso',
            {'valor': valor, 'correntista_id': correntista_id}
        )

        return jsonify({"mensagem": "Saque realizado com sucesso"}), 201
    except mysql.connector.Error as ex:
        return jsonify({"erro": f"Erro ao realizar saque: {ex}"}), 500

# -----------------
# Rota para Operação de Depósito (PROTEGIDA)
# -----------------
@app.route('/deposito', methods=['POST'])
@token_required
def depositar():
    try:
        data = request.get_json()
        correntista_id = data.get('correntista_id')
        valor = data.get('valor')

        if not all([correntista_id, valor]):
            return jsonify({"erro": "Dados incompletos"}), 400

        if valor <= 0:
            return jsonify({"erro": "Valor deve ser positivo"}), 400

        # Verificar se o correntista pertence ao usuário logado
        if not verificar_correntista_usuario(correntista_id, request.usuario_atual['usuario_id']):
            return jsonify({"erro": "Correntista não encontrado ou não autorizado"}), 403

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.callproc('spDepositar', (correntista_id, valor))
        conn.commit()
        cursor.close()
        conn.close()
        
        # Emitir notificação WebSocket
        emitir_notificacao(
            request.usuario_atual['usuario_id'],
            'deposito',
            f'Depósito de R$ {valor:.2f} realizado com sucesso',
            {'valor': valor, 'correntista_id': correntista_id}
        )

        return jsonify({"mensagem": "Depósito realizado com sucesso"}), 201
    except mysql.connector.Error as ex:
        return jsonify({"erro": f"Erro ao realizar depósito: {ex}"}), 500

# -----------------
# Eventos WebSocket
# -----------------
@socketio.on('connect')
def handle_connect():
    """Evento disparado quando um cliente conecta"""
    print('Cliente conectado')
    emit('conexao', {'mensagem': 'Conectado ao servidor WebSocket'})

@socketio.on('disconnect')
def handle_disconnect():
    """Evento disparado quando um cliente desconecta"""
    print('Cliente desconectado')

@socketio.on('autenticar')
def handle_autenticar(data):
    """Autentica o usuário no WebSocket usando token JWT"""
    try:
        token = data.get('token')
        if not token:
            emit('erro', {'mensagem': 'Token não fornecido'})
            return
        
        payload = verificar_token(token)
        if payload is None:
            emit('erro', {'mensagem': 'Token inválido ou expirado'})
            disconnect()
            return
        
        # Adicionar cliente à sala do usuário
        from flask_socketio import join_room
        usuario_id = payload['usuario_id']
        join_room(f'user_{usuario_id}')
        
        emit('autenticado', {
            'mensagem': 'Autenticado com sucesso',
            'usuario_id': usuario_id,
            'email': payload['email']
        })
        
        print(f'Usuário {usuario_id} autenticado no WebSocket')
        
    except Exception as e:
        emit('erro', {'mensagem': f'Erro na autenticação: {str(e)}'})
        disconnect()

@socketio.on('solicitar_saldo')
def handle_solicitar_saldo(data):
    """Retorna o saldo atualizado de um correntista"""
    try:
        token = data.get('token')
        correntista_id = data.get('correntista_id')
        
        if not token or not correntista_id:
            emit('erro', {'mensagem': 'Token e correntista_id são obrigatórios'})
            return
        
        payload = verificar_token(token)
        if payload is None:
            emit('erro', {'mensagem': 'Token inválido'})
            return
        
        # Verificar se o correntista pertence ao usuário
        if not verificar_correntista_usuario(correntista_id, payload['usuario_id']):
            emit('erro', {'mensagem': 'Correntista não autorizado'})
            return
        
        # Buscar saldo atualizado
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT CorrentistaID, NomeCorrentista, Saldo FROM Correntistas WHERE CorrentistaID = %s",
            (correntista_id,)
        )
        correntista = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if correntista:
            emit('saldo_atualizado', correntista)
        else:
            emit('erro', {'mensagem': 'Correntista não encontrado'})
            
    except Exception as e:
        emit('erro', {'mensagem': f'Erro ao buscar saldo: {str(e)}'})

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)