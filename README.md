# API de Movimentações Financeiras

Uma API RESTful simples para gerenciar e consultar movimentações financeiras, desenvolvida com **Flask** e **Python**, utilizando **MySQL** como banco de dados. Este projeto faz parte de um estudo sobre a criação de APIs e a integração com bancos de dados relacionais.

---

## 🚀 Tecnologias Utilizadas

* **Python 3.x:** Linguagem de programação.
* **Flask:** Micro-framework web para a criação da API.
* **MySQL:** Sistema de gerenciamento de banco de dados.
* **XAMPP:** Ambiente de desenvolvimento para o servidor web e o banco de dados.
* **`mysql-connector-python`:** Driver para conectar o Python ao MySQL.

---

## 📋 Pré-requisitos

Para rodar este projeto localmente, você precisa ter:

* **Python 3.x** instalado.
* **XAMPP** instalado e com os módulos **Apache** e **MySQL** em execução.

---

## 🛠️ Instalação e Configuração

Siga os passos abaixo para configurar o ambiente e rodar a API.

### 1. Clonar o Repositório

```bash
git clone [https://github.com/seu-usuario/seu-repositorio.git](https://github.com/seu-usuario/seu-repositorio.git)
cd seu-repositorio
````


### 2. Configurar o Banco de Dados

* Abra o painel de controle do XAMPP e inicie os módulos Apache e MySQL.

* Acesse o phpMyAdmin pelo seu navegador: `http://localhost/phpmyadmin`.

* Vá para a aba `SQL` e execute o script `SistemasCorporativos.sql` (disponível neste repositório) para criar o banco de dados, as tabelas e a `view` necessários.

### 3. Instalar as Dependências
No terminal, na pasta raiz do projeto, instale as bibliotecas Python necessárias:

```bash
py -m pip install Flask mysql-connector-python
```

### 4. Configurar a Conexão com o Banco de Dados
Abra o arquivo `api.py` e configure suas credenciais de acesso ao MySQL no bloco de variáveis, caso sejam diferentes das padrão do XAMPP:

```bash
# api.py

DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = '' # Senha padrão do XAMPP é vazia
DB_NAME = 'SistemasCorporativos'
```

### 5. Rodar a API
No terminal, execute o comando para iniciar o servidor Flask:

```bash
py api.py
```
A API estará rodando em `http://127.0.0.1:5000/movimentacoes`.

---

🖥️ Endpoints da API
Atualmente, a API possui apenas um endpoint para consulta de dados.

`GET /movimentacoes`
Retorna uma lista completa de todas as movimentações financeiras cadastradas no banco de dados, incluindo informações do correntista e, se aplicável, do beneficiário.

Exemplo de Resposta (JSON):

```JSON
[
  {
    "CorrentistaID": 1,
    "NomeCorrentista": "João Silva",
    "TipoOperacao": "Débito",
    "MovimentacaoID": 1,
    "Descricao": "Saque",
    "DataOperacao": "2025-09-26 19:30:00",
    "ValorOperacao": 200.00,
    "BeneficiarioID": null,
    "NomeBeneficiario": null
  },
  {
    "CorrentistaID": 1,
    "NomeCorrentista": "João Silva",
    "TipoOperacao": "Débito",
    "MovimentacaoID": 3,
    "Descricao": "Transferência",
    "DataOperacao": "2025-09-26 19:35:00",
    "ValorOperacao": 50.00,
    "BeneficiarioID": 2,
    "NomeBeneficiario": "Maria Souza"
  }
]
```

---

### Equipe: 
* Brunno de Melo Marques
* Emanuel Correia Tavares
