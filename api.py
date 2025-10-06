# api.py
from flask import Flask, jsonify, request, render_template
import mysql.connector

# A variável 'app' precisa ser definida antes de qualquer rota.
app = Flask(__name__)

# -----------------
# Configuração do banco de dados MySQL
# Altere essas informações para as suas configurações
# -----------------
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = '' 
DB_NAME = 'SistemasCorporativos'

# Função para conectar ao banco de dados
def get_db_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

# -----------------
# Rota para a página de testes (página principal)
# -----------------
@app.route('/')
def home():
    return render_template('index.html')

# -----------------
# Rota para exibir todas as movimentações
# -----------------
@app.route('/movimentacoes', methods=['GET'])
def get_movimentacoes():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM vwExtrato")
        movimentacoes = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(movimentacoes)
    except mysql.connector.Error as ex:
        return jsonify({"erro": f"Erro ao conectar ou consultar o banco de dados: {ex}"}), 500

# -----------------
# Rota para exibir o extrato de movimentações de um correntista
# -----------------
@app.route('/extrato/<int:correntista_id>', methods=['GET'])
def get_extrato(correntista_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM vwExtrato WHERE CorrentistaID = %s", (correntista_id,))
        extrato = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(extrato)
    except mysql.connector.Error as ex:
        return jsonify({"erro": f"Erro ao buscar extrato: {ex}"}), 500

# -----------------
# Rota para Operação de Pagamento
# -----------------
@app.route('/pagamento', methods=['POST'])
def pagar():
    try:
        data = request.get_json()
        correntista_id = data.get('correntista_id')
        valor = data.get('valor')
        descricao = data.get('descricao')

        if not all([correntista_id, valor, descricao]):
            return jsonify({"erro": "Dados incompletos"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.callproc('spPagar', (correntista_id, valor, descricao))
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"mensagem": "Pagamento realizado com sucesso"}), 201
    except mysql.connector.Error as ex:
        return jsonify({"erro": f"Erro ao realizar pagamento: {ex}"}), 500

# -----------------
# Rota para Operação de Transferência
# -----------------
@app.route('/transferencia', methods=['POST'])
def transferir():
    try:
        data = request.get_json()
        origem_id = data.get('correntista_id_origem')
        destino_id = data.get('correntista_id_destino')
        valor = data.get('valor')

        if not all([origem_id, destino_id, valor]):
            return jsonify({"erro": "Dados incompletos"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.callproc('spTransferir', (origem_id, valor, destino_id))
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"mensagem": "Transferência realizada com sucesso"}), 201
    except mysql.connector.Error as ex:
        return jsonify({"erro": f"Erro ao realizar transferência: {ex}"}), 500

# -----------------
# Rota para Operação de Saque
# -----------------
@app.route('/saque', methods=['POST'])
def sacar():
    try:
        data = request.get_json()
        correntista_id = data.get('correntista_id')
        valor = data.get('valor')

        if not all([correntista_id, valor]):
            return jsonify({"erro": "Dados incompletos"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.callproc('spSacar', (correntista_id, valor))
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"mensagem": "Saque realizado com sucesso"}), 201
    except mysql.connector.Error as ex:
        return jsonify({"erro": f"Erro ao realizar saque: {ex}"}), 500

# -----------------
# Rota para Operação de Depósito
# -----------------
@app.route('/deposito', methods=['POST'])
def depositar():
    try:
        data = request.get_json()
        correntista_id = data.get('correntista_id')
        valor = data.get('valor')

        if not all([correntista_id, valor]):
            return jsonify({"erro": "Dados incompletos"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.callproc('spDepositar', (correntista_id, valor))
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"mensagem": "Depósito realizado com sucesso"}), 201
    except mysql.connector.Error as ex:
        return jsonify({"erro": f"Erro ao realizar depósito: {ex}"}), 500

if __name__ == '__main__':
    app.run(debug=True)