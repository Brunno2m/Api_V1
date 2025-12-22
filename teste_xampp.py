#!/usr/bin/env python3
"""
Teste específico para XAMPP rodando
"""

import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

print("=" * 80)
print("🧪 TESTE DE CONEXÃO COM XAMPP")
print("=" * 80)
print()

DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')
DB_NAME = os.getenv('DB_NAME', 'SistemasCorporativos')

print(f"📝 Configurações:")
print(f"   Host: {DB_HOST}")
print(f"   Usuário: {DB_USER}")
print(f"   Senha: {'(vazia)' if not DB_PASSWORD else '******'}")
print(f"   Banco: {DB_NAME}")
print()

# Teste 1: Conectar ao MySQL (sem especificar banco)
print("1️⃣  Testando conexão com MySQL...")
try:
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD
    )
    print("   ✅ MySQL está acessível!")
    conn.close()
except Exception as e:
    print(f"   ❌ ERRO: {e}")
    print()
    print("   💡 O MySQL não está rodando ou as credenciais estão erradas")
    print("      Verifique o XAMPP Control Panel")
    exit(1)

print()

# Teste 2: Verificar se o banco existe
print("2️⃣  Verificando banco de dados...")
try:
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD
    )
    cursor = conn.cursor()
    cursor.execute("SHOW DATABASES LIKE 'SistemasCorporativos'")
    result = cursor.fetchone()
    
    if result:
        print(f"   ✅ Banco '{DB_NAME}' existe!")
    else:
        print(f"   ❌ Banco '{DB_NAME}' NÃO existe!")
        print()
        print("   💡 SOLUÇÃO:")
        print("      1. Abra http://localhost/phpmyadmin")
        print("      2. Crie um banco chamado 'SistemasCorporativos'")
        print("      3. Importe o arquivo database/SistemasCorporativos.sql")
        cursor.close()
        conn.close()
        exit(1)
    
    cursor.close()
    conn.close()
except Exception as e:
    print(f"   ❌ ERRO: {e}")
    exit(1)

print()

# Teste 3: Verificar tabelas
print("3️⃣  Verificando tabelas...")
try:
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES")
    tabelas = cursor.fetchall()
    
    if len(tabelas) == 0:
        print("   ❌ Nenhuma tabela encontrada!")
        print()
        print("   💡 O banco existe mas está vazio!")
        print("      Importe o arquivo database/SistemasCorporativos.sql")
        cursor.close()
        conn.close()
        exit(1)
    else:
        print(f"   ✅ {len(tabelas)} tabelas encontradas:")
        for tabela in tabelas:
            print(f"      • {tabela[0]}")
    
    cursor.close()
    conn.close()
except Exception as e:
    print(f"   ❌ ERRO: {e}")
    exit(1)

print()

# Teste 4: Verificar dados
print("4️⃣  Verificando dados...")
try:
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM Usuarios")
    usuarios = cursor.fetchone()[0]
    print(f"   ✅ {usuarios} usuários cadastrados")
    
    cursor.execute("SELECT COUNT(*) FROM Correntistas")
    correntistas = cursor.fetchone()[0]
    print(f"   ✅ {correntistas} correntistas cadastrados")
    
    cursor.close()
    conn.close()
except Exception as e:
    print(f"   ❌ ERRO: {e}")
    print(f"   Tabela pode não existir ou estrutura incorreta")

print()
print("=" * 80)
print("✅ XAMPP ESTÁ FUNCIONANDO CORRETAMENTE!")
print("=" * 80)
print()
print("Agora você pode iniciar o servidor:")
print("   python run_server.py")
print()
print("Ou se preferir sem WebSocket:")
print("   python simple_server.py")
print()
