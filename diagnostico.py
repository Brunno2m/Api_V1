#!/usr/bin/env python3
"""
Script de diagnóstico para identificar problemas ao rodar a API
"""

import sys
import os

print("=" * 80)
print("🔍 DIAGNÓSTICO DO SISTEMA - API V1")
print("=" * 80)
print()

# 1. Verificar Python
print("1️⃣  PYTHON")
print("-" * 80)
print(f"✓ Versão: {sys.version}")
print(f"✓ Executável: {sys.executable}")
print()

# 2. Verificar dependências
print("2️⃣  DEPENDÊNCIAS")
print("-" * 80)

dependencias = {
    'flask': 'Flask',
    'flask_socketio': 'Flask-SocketIO',
    'mysql.connector': 'MySQL Connector',
    'jwt': 'PyJWT',
    'bcrypt': 'bcrypt',
    'dotenv': 'python-dotenv',
    'eventlet': 'eventlet'
}

problemas = []
for modulo, nome in dependencias.items():
    try:
        __import__(modulo)
        print(f"✓ {nome}")
    except ImportError as e:
        print(f"❌ {nome} - NÃO INSTALADO")
        problemas.append(nome)

if problemas:
    print()
    print("⚠️  Instale as dependências faltantes:")
    print(f"   pip install {' '.join(problemas.lower())}")
    
print()

# 3. Verificar arquivo .env
print("3️⃣  CONFIGURAÇÃO (.env)")
print("-" * 80)

if os.path.exists('.env'):
    print("✓ Arquivo .env encontrado")
    from dotenv import load_dotenv
    load_dotenv()
    
    vars_env = ['DB_HOST', 'DB_USER', 'DB_NAME']
    for var in vars_env:
        valor = os.getenv(var, 'NÃO DEFINIDA')
        if valor != 'NÃO DEFINIDA':
            print(f"  ✓ {var}: {valor}")
        else:
            print(f"  ⚠️  {var}: usando padrão")
else:
    print("⚠️  Arquivo .env NÃO encontrado")
    print("   Criando .env com valores padrão...")
    
    with open('.env', 'w') as f:
        f.write("""# Configurações do Banco de Dados MySQL
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=
DB_NAME=SistemasCorporativos

# Configurações JWT
JWT_SECRET_KEY=sua_chave_secreta_super_segura_aqui
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24
""")
    print("   ✓ Arquivo .env criado!")

print()

# 4. Testar conexão com MySQL
print("4️⃣  CONEXÃO COM MYSQL")
print("-" * 80)

try:
    from dotenv import load_dotenv
    load_dotenv()
    
    import mysql.connector
    
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_USER = os.getenv('DB_USER', 'root')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')
    DB_NAME = os.getenv('DB_NAME', 'SistemasCorporativos')
    
    print(f"Tentando conectar em {DB_USER}@{DB_HOST}/{DB_NAME}...")
    
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    
    print("✓ Conexão com MySQL estabelecida!")
    
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM Usuarios")
    count = cursor.fetchone()[0]
    print(f"✓ Banco de dados acessível ({count} usuários cadastrados)")
    
    cursor.close()
    conn.close()
    
except mysql.connector.Error as e:
    print(f"❌ ERRO ao conectar com MySQL: {e}")
    print()
    print("💡 SOLUÇÕES:")
    print("   1. Verifique se o XAMPP está rodando")
    print("   2. Verifique se o MySQL está ativo no XAMPP")
    print("   3. Verifique as credenciais no arquivo .env")
    print("   4. Importe o arquivo database/SistemasCorporativos.sql no phpMyAdmin")
    problemas.append("MySQL")
except Exception as e:
    print(f"❌ ERRO: {e}")
    problemas.append("MySQL")

print()

# 5. Testar carregamento da API
print("5️⃣  CARREGAMENTO DA API")
print("-" * 80)

try:
    from api import app, socketio
    print("✓ API carregada com sucesso")
    print(f"✓ SocketIO configurado: {socketio is not None}")
    
    # Contar rotas
    rotas = len([r for r in app.url_map.iter_rules() if r.endpoint != 'static'])
    print(f"✓ {rotas} rotas disponíveis")
    
except Exception as e:
    print(f"❌ ERRO ao carregar API: {e}")
    import traceback
    traceback.print_exc()
    problemas.append("API")

print()

# 6. Verificar porta
print("6️⃣  PORTA 5000")
print("-" * 80)

import socket

def check_port(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', port))
    sock.close()
    return result == 0

if check_port(5000):
    print("⚠️  Porta 5000 já está em uso")
    print("   Solução: Pare o servidor que está usando a porta 5000")
    print("   Comando: lsof -ti:5000 | xargs kill -9")
else:
    print("✓ Porta 5000 disponível")

print()

# Resumo
print("=" * 80)
if problemas:
    print("❌ PROBLEMAS ENCONTRADOS:")
    for problema in set(problemas):
        print(f"   • {problema}")
    print()
    print("Corrija os problemas acima e tente novamente.")
else:
    print("✅ TUDO PRONTO!")
    print()
    print("Para iniciar o servidor:")
    print("   python api.py")
    print()
    print("Depois acesse:")
    print("   http://localhost:5000")

print("=" * 80)
