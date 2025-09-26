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

-- Criar os Procedures (Opcional, mas útil para o sistema)
-- O MySQL usa a sintaxe DELIMITER para procedures

DELIMITER $$
CREATE PROCEDURE spDepositar(
    IN p_CorrentistaID INT,
    IN p_ValorDeposito DECIMAL(15, 2)
)
BEGIN
    INSERT INTO Movimentacoes(TipoOperacao, CorrentistaID, ValorOperacao, DataOperacao, Descricao)
    VALUES ('C', p_CorrentistaID, p_ValorDeposito, NOW(), 'Depósito em conta');
END$$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE spSacar(
    IN p_CorrentistaID INT,
    IN p_ValorSaque DECIMAL(15, 2)
)
BEGIN
    INSERT INTO Movimentacoes(TipoOperacao, CorrentistaID, ValorOperacao, DataOperacao, Descricao)
    VALUES ('D', p_CorrentistaID, p_ValorSaque, NOW(), 'Saque');
END$$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE spPagar(
    IN p_CorrentistaID INT,
    IN p_ValorOperacao DECIMAL(15, 2),
    IN p_Descricao VARCHAR(50)
)
BEGIN
    INSERT INTO Movimentacoes(TipoOperacao, CorrentistaID, ValorOperacao, DataOperacao, Descricao)
    VALUES ('D', p_CorrentistaID, p_ValorOperacao, NOW(), CONCAT('Pagamento: ', p_Descricao));
END$$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE spTransferir(
    IN p_CorrentistaID INT,
    IN p_ValorOperacao DECIMAL(15, 2),
    IN p_CorrentistaBeneficiarioID INT
)
BEGIN
    INSERT INTO Movimentacoes(TipoOperacao, CorrentistaID, ValorOperacao, DataOperacao, Descricao, CorrentistaBeneficiarioID)
    VALUES ('D', p_CorrentistaID, p_ValorOperacao, NOW(), 'Transferência', p_CorrentistaBeneficiarioID);
END$$
DELIMITER ;