#!/usr/bin/env python3
# Script para debugar e corrigir o problema de login

import mysql.connector
import bcrypt
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente
load_dotenv()

# Configurações do banco
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')
DB_NAME = os.getenv('DB_NAME', 'SistemasCorporativos')

def conectar_banco():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

def verificar_usuario():
    """Verifica se o usuário admin existe no banco"""
    try:
        conn = conectar_banco()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT * FROM Usuarios WHERE Email = 'admin@teste.com'")
        usuario = cursor.fetchone()
        
        if usuario:
            print("✅ Usuário encontrado no banco:")
            print(f"   ID: {usuario['UsuarioID']}")
            print(f"   Email: {usuario['Email']}")
            print(f"   Nome: {usuario['Nome']}")
            print(f"   Hash da senha: {usuario['SenhaHash'][:50]}...")
            return usuario
        else:
            print("❌ Usuário admin@teste.com NÃO encontrado no banco!")
            return None
            
    except Exception as e:
        print(f"❌ Erro ao verificar usuário: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

def testar_senha():
    """Testa se a senha 123456 confere com o hash"""
    usuario = verificar_usuario()
    
    if not usuario:
        return False
    
    senha = "123456"
    hash_armazenado = usuario['SenhaHash']
    
    try:
        # Tentar verificar a senha
        resultado = bcrypt.checkpw(senha.encode('utf-8'), hash_armazenado.encode('utf-8'))
        
        if resultado:
            print("✅ Senha está correta!")
            return True
        else:
            print("❌ Senha NÃO confere com o hash!")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao verificar senha: {e}")
        return False

def recriar_usuario():
    """Recria o usuário com novo hash"""
    print("\n🔧 Recriando usuário admin...")
    
    try:
        conn = conectar_banco()
        cursor = conn.cursor()
        
        # Deletar usuário existente
        cursor.execute("DELETE FROM Usuarios WHERE Email = 'admin@teste.com'")
        
        # Gerar novo hash
        senha = "123456"
        novo_hash = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        # Inserir usuário com novo hash
        cursor.execute(
            "INSERT INTO Usuarios (Email, SenhaHash, Nome) VALUES (%s, %s, %s)",
            ('admin@teste.com', novo_hash, 'Administrador')
        )
        
        conn.commit()
        print("✅ Usuário recriado com sucesso!")
        print(f"   Novo hash: {novo_hash[:50]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao recriar usuário: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    print("🔍 Debugando problema de login...\n")
    
    # Verificar conexão com banco
    try:
        conn = conectar_banco()
        print("✅ Conexão com banco OK")
        conn.close()
    except Exception as e:
        print(f"❌ Erro de conexão: {e}")
        exit(1)
    
    # Verificar usuário
    usuario = verificar_usuario()
    
    if usuario:
        # Testar senha
        senha_ok = testar_senha()
        
        if not senha_ok:
            resposta = input("\n❓ Deseja recriar o usuário com novo hash? (s/n): ")
            if resposta.lower() == 's':
                recriar_usuario()
                print("\n🔄 Teste novamente o login na aplicação!")
    else:
        print("\n🔧 Criando usuário admin...")
        recriar_usuario()