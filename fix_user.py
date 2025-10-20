#!/usr/bin/env python3
import mysql.connector
import bcrypt
from dotenv import load_dotenv
import os

load_dotenv()

# Configurações do banco
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')
DB_NAME = os.getenv('DB_NAME', 'SistemasCorporativos')

# Conectar ao banco
conn = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME
)

cursor = conn.cursor()

# Deletar usuário existente
cursor.execute("DELETE FROM Usuarios WHERE Email = 'admin@teste.com'")

# Gerar novo hash para senha "123456"
senha = "123456"
novo_hash = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# Inserir usuário com novo hash
cursor.execute(
    "INSERT INTO Usuarios (Email, SenhaHash, Nome) VALUES (%s, %s, %s)",
    ('admin@teste.com', novo_hash, 'Administrador')
)

conn.commit()
print("✅ Usuário recriado com sucesso!")
print(f"Email: admin@teste.com")
print(f"Senha: 123456")
print(f"Novo hash: {novo_hash}")

# Testar o hash
teste = bcrypt.checkpw("123456".encode('utf-8'), novo_hash.encode('utf-8'))
print(f"✅ Teste do hash: {'OK' if teste else 'FALHOU'}")

cursor.close()
conn.close()