# api.py
from flask import Flask, jsonify
import mysql.connector

# -----------------
# Configuração do banco de dados MySQL (XAMPP)
# Altere essas informações para as suas configurações
# -----------------
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = '' 
DB_NAME = 'SistemasCorporativos'

app = Flask(__name__)

# -----------------
# Rota da API para buscar as movimentações
# -----------------
@app.route('/movimentacoes', methods=['GET'])
def get_movimentacoes():
    try:
        # Conecta ao banco de dados MySQL
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        
        cursor = conn.cursor(dictionary=True)
        
        # Executa a consulta na view
        cursor.execute("SELECT * FROM vwExtrato")
        
        # Pega todos os resultados (já como uma lista de dicionários)
        movimentacoes = cursor.fetchall()

        # Fecha a conexão
        cursor.close()
        conn.close()

        # Retorna a lista de movimentações como um JSON
        return jsonify(movimentacoes)

    except mysql.connector.Error as ex:
        # Se a conexão falhar, retorne um erro amigável
        return jsonify({"erro": f"Erro ao conectar ou consultar o banco de dados: {ex}"}), 500

# -----------------
# Inicia o servidor Flask
# -----------------
if __name__ == '__main__':
    app.run(debug=True)