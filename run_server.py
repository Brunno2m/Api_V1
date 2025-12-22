#!/usr/bin/env python3
"""
Servidor alternativo SEM eventlet - para evitar problemas de compatibilidade
Use este arquivo se tiver problemas com o api.py
"""

from flask import Flask, jsonify, request, render_template
from flask_socketio import SocketIO
import mysql.connector
import jwt
import bcrypt
from datetime import datetime, timedelta
from functools import wraps
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

print("=" * 80)
print("🚀 INICIANDO SERVIDOR - API V1")
print("=" * 80)
print()

# Importar a aplicação
try:
    from api import app, socketio
    print("✅ API importada com sucesso")
except Exception as e:
    print(f"❌ Erro ao importar API: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

# Testar conexão com MySQL antes de iniciar
print()
print("🔍 Testando conexão com MySQL...")
try:
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_USER = os.getenv('DB_USER', 'root')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')
    DB_NAME = os.getenv('DB_NAME', 'SistemasCorporativos')
    
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    print(f"✅ MySQL conectado: {DB_USER}@{DB_HOST}/{DB_NAME}")
    
    cursor = conn.cursor()
    
    # Verificar se as tabelas existem
    cursor.execute("SHOW TABLES")
    tabelas = cursor.fetchall()
    print(f"✅ {len(tabelas)} tabelas encontradas no banco")
    
    # Verificar usuários
    cursor.execute("SELECT COUNT(*) FROM Usuarios")
    count = cursor.fetchone()[0]
    print(f"✅ {count} usuários cadastrados")
    
    cursor.close()
    conn.close()
    
except mysql.connector.Error as e:
    print(f"❌ ERRO MySQL: {e}")
    print()
    print("💡 SOLUÇÕES:")
    print("   1. Verifique se o MySQL está rodando no XAMPP")
    print("   2. Importe o arquivo database/SistemasCorporativos.sql")
    print("   3. Verifique as credenciais no arquivo .env")
    exit(1)

print()
print("=" * 80)
print("✅ SERVIDOR PRONTO!")
print("=" * 80)
print()
print("🌐 Acesse em seu navegador:")
print("   • http://localhost:5000")
print("   • http://127.0.0.1:5000")
print()
print("⚠️  Para parar o servidor, pressione CTRL+C")
print()
print("=" * 80)
print()

if __name__ == '__main__':
    # Usar gevent em vez de eventlet (mais compatível)
    try:
        socketio.run(
            app, 
            debug=True, 
            host='0.0.0.0', 
            port=5000,
            allow_unsafe_werkzeug=True  # Para desenvolvimento
        )
    except Exception as e:
        print(f"\n❌ Erro ao iniciar servidor: {e}")
        print("\n💡 Tente instalar gevent: pip install gevent")
        print("   Ou use: python simple_server.py")
