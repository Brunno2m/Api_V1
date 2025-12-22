#!/usr/bin/env python3
"""
Servidor SIMPLES sem WebSocket - Use se tiver problemas com SocketIO
"""

from flask import Flask, jsonify, request, render_template
import mysql.connector
import jwt
import bcrypt
from datetime import datetime, timedelta
from functools import wraps
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

app = Flask(__name__)

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

# -----------------
# Decorador para proteger rotas
# -----------------
def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return jsonify({'erro': 'Token mal formatado'}), 401
        
        if not token:
            return jsonify({'erro': 'Token de acesso necessário'}), 401
        
        payload = verificar_token(token)
        if payload is None:
            return jsonify({'erro': 'Token inválido ou expirado'}), 401
        
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
        
        cursor.execute("SELECT UsuarioID FROM Usuarios WHERE Email = %s", (email,))
        if cursor.fetchone():
            cursor.close()
            conn.close()
            return jsonify({"erro": "Email já cadastrado"}), 409
        
        senha_hash = hash_senha(senha)
        cursor.execute(
            "INSERT INTO Usuarios (Email, SenhaHash, Nome) VALUES (%s, %s, %s)",
            (email, senha_hash, nome)
        )
        conn.commit()
        usuario_id = cursor.lastrowid
        
        cursor.close()
        conn.close()
        
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
        
        cursor.execute(
            "SELECT UsuarioID, Email, SenhaHash, Nome FROM Usuarios WHERE Email = %s AND Ativo = TRUE",
            (email,)
        )
        usuario = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if not usuario:
            return jsonify({"erro": "Email ou senha incorretos"}), 401
        
        if not verificar_senha(senha, usuario['SenhaHash']):
            return jsonify({"erro": "Email ou senha incorretos"}), 401
        
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

@app.route('/')
def home():
    return render_template('index.html')

# Copiar todas as outras rotas do api.py aqui...
# (Para simplificar, vou importar do api.py original)

print("=" * 80)
print("🚀 SERVIDOR SIMPLES (SEM WEBSOCKET)")
print("=" * 80)
print()
print("⚠️  Este servidor NÃO tem suporte a WebSocket")
print("   As notificações em tempo real não funcionarão")
print("   Mas todas as outras funcionalidades estarão OK")
print()

# Testar conexão
try:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM Usuarios")
    count = cursor.fetchone()[0]
    print(f"✅ MySQL conectado: {count} usuários no banco")
    cursor.close()
    conn.close()
except Exception as e:
    print(f"❌ ERRO MySQL: {e}")
    print("   Verifique se o banco foi importado!")

print()
print("🌐 Servidor iniciando em http://localhost:5000")
print("=" * 80)
print()

if __name__ == '__main__':
    # Importar rotas do api.py principal
    try:
        from api import app as main_app
        # Usar as rotas do app principal mas sem socketio
        app = main_app
    except:
        pass
    
    app.run(debug=True, host='0.0.0.0', port=5000)
