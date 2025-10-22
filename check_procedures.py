"""
Script para verificar e criar as stored procedures necessárias
"""
import mysql.connector
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente
load_dotenv()

def conectar_banco():
    """Conecta ao banco de dados"""
    try:
        conexao = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            database=os.getenv('DB_NAME', 'SistemasCorporativos')
        )
        return conexao
    except mysql.connector.Error as e:
        print(f"Erro ao conectar: {e}")
        return None

def verificar_procedures():
    """Verifica quais procedures existem"""
    conexao = conectar_banco()
    if not conexao:
        return
    
    cursor = conexao.cursor()
    
    try:
        # Verificar procedures existentes
        cursor.execute("""
            SELECT ROUTINE_NAME 
            FROM INFORMATION_SCHEMA.ROUTINES 
            WHERE ROUTINE_SCHEMA = %s AND ROUTINE_TYPE = 'PROCEDURE'
        """, (os.getenv('DB_NAME', 'SistemasCorporativos'),))
        
        procedures = cursor.fetchall()
        print("Procedures existentes:")
        for proc in procedures:
            print(f"  - {proc[0]}")
        
        procedures_necessarias = ['spDepositar', 'spSacar', 'spPagar', 'spTransferir']
        procedures_existentes = [proc[0] for proc in procedures]
        
        procedures_faltando = [proc for proc in procedures_necessarias if proc not in procedures_existentes]
        
        if procedures_faltando:
            print(f"\nProcedures faltando: {procedures_faltando}")
            return procedures_faltando
        else:
            print("\nTodas as procedures necessárias existem!")
            return []
            
    except mysql.connector.Error as e:
        print(f"Erro ao verificar procedures: {e}")
        return []
    finally:
        cursor.close()
        conexao.close()

def criar_procedures():
    """Cria as stored procedures necessárias"""
    conexao = conectar_banco()
    if not conexao:
        return False
    
    cursor = conexao.cursor()
    
    procedures = [
        """
        CREATE PROCEDURE spDepositar(
            IN p_CorrentistaID INT,
            IN p_ValorDeposito DECIMAL(15, 2)
        )
        BEGIN
            -- Inserir movimentação de crédito
            INSERT INTO Movimentacoes(TipoOperacao, CorrentistaID, ValorOperacao, DataOperacao, Descricao)
            VALUES ('C', p_CorrentistaID, p_ValorDeposito, NOW(), 'Depósito em conta');
            
            -- Atualizar saldo do correntista
            UPDATE Correntistas 
            SET Saldo = Saldo + p_ValorDeposito 
            WHERE CorrentistaID = p_CorrentistaID;
        END
        """,
        """
        CREATE PROCEDURE spSacar(
            IN p_CorrentistaID INT,
            IN p_ValorSaque DECIMAL(15, 2)
        )
        BEGIN
            -- Verificar se há saldo suficiente
            DECLARE saldo_atual DECIMAL(15, 2);
            SELECT Saldo INTO saldo_atual FROM Correntistas WHERE CorrentistaID = p_CorrentistaID;
            
            IF saldo_atual >= p_ValorSaque THEN
                -- Inserir movimentação de débito
                INSERT INTO Movimentacoes(TipoOperacao, CorrentistaID, ValorOperacao, DataOperacao, Descricao)
                VALUES ('D', p_CorrentistaID, p_ValorSaque, NOW(), 'Saque');
                
                -- Atualizar saldo do correntista
                UPDATE Correntistas 
                SET Saldo = Saldo - p_ValorSaque 
                WHERE CorrentistaID = p_CorrentistaID;
            ELSE
                SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Saldo insuficiente para realizar o saque';
            END IF;
        END
        """,
        """
        CREATE PROCEDURE spPagar(
            IN p_CorrentistaID INT,
            IN p_ValorOperacao DECIMAL(15, 2),
            IN p_Descricao VARCHAR(50)
        )
        BEGIN
            -- Verificar se há saldo suficiente
            DECLARE saldo_atual DECIMAL(15, 2);
            SELECT Saldo INTO saldo_atual FROM Correntistas WHERE CorrentistaID = p_CorrentistaID;
            
            IF saldo_atual >= p_ValorOperacao THEN
                -- Inserir movimentação de débito
                INSERT INTO Movimentacoes(TipoOperacao, CorrentistaID, ValorOperacao, DataOperacao, Descricao)
                VALUES ('D', p_CorrentistaID, p_ValorOperacao, NOW(), CONCAT('Pagamento: ', p_Descricao));
                
                -- Atualizar saldo do correntista
                UPDATE Correntistas 
                SET Saldo = Saldo - p_ValorOperacao 
                WHERE CorrentistaID = p_CorrentistaID;
            ELSE
                SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Saldo insuficiente para realizar o pagamento';
            END IF;
        END
        """,
        """
        CREATE PROCEDURE spTransferir(
            IN p_CorrentistaID INT,
            IN p_ValorOperacao DECIMAL(15, 2),
            IN p_CorrentistaBeneficiarioID INT
        )
        BEGIN
            DECLARE saldo_atual DECIMAL(15, 2);
            DECLARE beneficiario_existe INT DEFAULT 0;
            
            -- Verificar se há saldo suficiente
            SELECT Saldo INTO saldo_atual FROM Correntistas WHERE CorrentistaID = p_CorrentistaID;
            
            -- Verificar se o beneficiário existe
            SELECT COUNT(*) INTO beneficiario_existe FROM Correntistas WHERE CorrentistaID = p_CorrentistaBeneficiarioID;
            
            IF beneficiario_existe = 0 THEN
                SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Correntista beneficiário não encontrado';
            ELSEIF saldo_atual >= p_ValorOperacao THEN
                -- Débito do pagador
                INSERT INTO Movimentacoes(TipoOperacao, CorrentistaID, ValorOperacao, DataOperacao, Descricao, CorrentistaBeneficiarioID)
                VALUES ('D', p_CorrentistaID, p_ValorOperacao, NOW(), 'Transferência', p_CorrentistaBeneficiarioID);
                
                -- Crédito do beneficiário
                INSERT INTO Movimentacoes(TipoOperacao, CorrentistaID, ValorOperacao, DataOperacao, Descricao, CorrentistaBeneficiarioID)
                VALUES ('C', p_CorrentistaBeneficiarioID, p_ValorOperacao, NOW(), 'Transferência recebida', p_CorrentistaID);
                
                -- Atualizar saldo do pagador
                UPDATE Correntistas 
                SET Saldo = Saldo - p_ValorOperacao 
                WHERE CorrentistaID = p_CorrentistaID;
                
                -- Atualizar saldo do beneficiário
                UPDATE Correntistas 
                SET Saldo = Saldo + p_ValorOperacao 
                WHERE CorrentistaID = p_CorrentistaBeneficiarioID;
            ELSE
                SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Saldo insuficiente para realizar a transferência';
            END IF;
        END
        """
    ]
    
    procedure_names = ['spDepositar', 'spSacar', 'spPagar', 'spTransferir']
    
    try:
        for i, procedure_sql in enumerate(procedures):
            procedure_name = procedure_names[i]
            
            # Remover procedure se existir
            cursor.execute(f"DROP PROCEDURE IF EXISTS {procedure_name}")
            print(f"Removendo procedure existente: {procedure_name}")
            
            # Criar nova procedure
            cursor.execute(procedure_sql)
            print(f"Criando procedure: {procedure_name}")
            
        conexao.commit()
        print("\nTodas as procedures foram criadas com sucesso!")
        return True
        
    except mysql.connector.Error as e:
        print(f"Erro ao criar procedures: {e}")
        conexao.rollback()
        return False
    finally:
        cursor.close()
        conexao.close()

if __name__ == "__main__":
    print("=== Verificador e Criador de Stored Procedures ===\n")
    
    procedures_faltando = verificar_procedures()
    
    if procedures_faltando:
        resposta = input(f"\nDeseja criar as procedures faltando? (s/n): ").lower()
        if resposta == 's':
            if criar_procedures():
                print("\n✅ Procedures criadas com sucesso!")
                print("Agora você pode testar as operações no dashboard.")
            else:
                print("\n❌ Erro ao criar procedures.")
        else:
            print("Operação cancelada.")
    else:
        print("\n✅ Sistema está funcionando corretamente!")