-- Criar o Banco de Dados
CREATE DATABASE SistemasCorporativos;
USE SistemasCorporativos;

-- Criar a Tabela 'Correntistas'
CREATE TABLE Correntistas (
    CorrentistaID INT AUTO_INCREMENT NOT NULL,
    NomeCorrentista VARCHAR(50) NOT NULL,
    Saldo DECIMAL(15, 2) NOT NULL,
    CONSTRAINT PK_Correntistas PRIMARY KEY (CorrentistaID),
    CONSTRAINT CK_Correntistas_Saldo CHECK (Saldo >= 0)
);

-- Criar a Tabela 'Movimentacoes'
CREATE TABLE Movimentacoes (
    MovimentacaoID INT AUTO_INCREMENT NOT NULL,
    TipoOperacao CHAR(1) NOT NULL,
    CorrentistaID INT NOT NULL,
    ValorOperacao DECIMAL(15, 2) NOT NULL,
    DataOperacao DATETIME NOT NULL,
    Descricao VARCHAR(50) NOT NULL,
    CorrentistaBeneficiarioID INT,
    CONSTRAINT PK_Movimentacoes PRIMARY KEY (MovimentacaoID),
    CONSTRAINT FK_Movimentacoes_Correntistas FOREIGN KEY (CorrentistaID) REFERENCES Correntistas (CorrentistaID),
    CONSTRAINT FK_Movimentacoes_Correntistas1 FOREIGN KEY (CorrentistaBeneficiarioID) REFERENCES Correntistas (CorrentistaID),
    CONSTRAINT CK_Movimentacoes_TipoOperacao CHECK (TipoOperacao IN ('D', 'C')),
    CONSTRAINT CK_Movimentacoes_ValorOperacao CHECK (ValorOperacao > 0)
);

-- Criar a View 'vwExtrato'
CREATE VIEW vwExtrato AS
SELECT
    C.CorrentistaID,
    C.NomeCorrentista,
    CASE M.TipoOperacao
        WHEN 'C' THEN 'Crédito'
        ELSE 'Débito'
    END AS TipoOperacao,
    M.MovimentacaoID,
    M.Descricao,
    M.DataOperacao,
    M.ValorOperacao,
    B.CorrentistaID AS BeneficiarioID,
    B.NomeCorrentista AS NomeBeneficiario
FROM Correntistas AS C
INNER JOIN Movimentacoes AS M
  ON C.CorrentistaID = M.CorrentistaID
LEFT JOIN Correntistas AS B
  ON M.CorrentistaBeneficiarioID = B.CorrentistaID;

-- Criar os Procedures com validações de saldo e atualização automática
-- O MySQL usa a sintaxe DELIMITER para procedures

DELIMITER $$
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
END$$
DELIMITER ;

DELIMITER $$
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
END$$
DELIMITER ;

DELIMITER $$
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
END$$
DELIMITER ;

DELIMITER $$
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
END$$
DELIMITER ;

-- Criar a Tabela 'Usuarios' para autenticação
CREATE TABLE Usuarios (
    UsuarioID INT AUTO_INCREMENT NOT NULL,
    Email VARCHAR(100) NOT NULL UNIQUE,
    SenhaHash VARCHAR(255) NOT NULL,
    Nome VARCHAR(100) NOT NULL,
    DataCriacao DATETIME DEFAULT CURRENT_TIMESTAMP,
    Ativo BOOLEAN DEFAULT TRUE,
    CONSTRAINT PK_Usuarios PRIMARY KEY (UsuarioID)
);

-- Inserir usuário padrão para testes (senha: 123456)
INSERT INTO Usuarios (Email, SenhaHash, Nome) 
VALUES ('admin@teste.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewfTWBtqZ4H5QHKG', 'Administrador');

-- Adicionar relacionamento entre Correntistas e Usuarios (opcional)
ALTER TABLE Correntistas ADD COLUMN UsuarioID INT;
ALTER TABLE Correntistas ADD CONSTRAINT FK_Correntistas_Usuarios FOREIGN KEY (UsuarioID) REFERENCES Usuarios (UsuarioID);

-- Inserir correntistas de exemplo vinculados ao usuário admin
INSERT INTO Correntistas (NomeCorrentista, Saldo, UsuarioID) VALUES 
('João Silva', 1000.00, 1),
('Maria Santos', 1500.00, 1);