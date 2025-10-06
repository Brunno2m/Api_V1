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
git clone [https://github.com/Brunno2m/Api_V1.git](https://github.com/Brunno2m/Api_V1.git)
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
A API estará rodando em `http://127.0.0.1:5000`.

---

🖥️ Endpoints da API
A API foi expandida para incluir endpoints de leitura e de operações bancárias.

1. Endpoints de Leitura (`GET`)


| Endpoint | Descrição | Exemplo de Resposta |
| :--- | :--- | :--- |
| `/movimentacoes` | Retorna uma lista completa de todas as movimentações financeiras cadastradas. | `[ ... ]` |
| `/extrato/<correntista_id>` | Exibe o extrato de um correntista específico, filtrando por ID. | `[ ... ]` |

2. Endpoints de Operação (`POST`)

Estes endpoints permitem realizar operações bancárias. Eles esperam um corpo de requisição no formato JSON.

`/deposito`
* Descrição: Realiza um depósito na conta de um correntista.

* Corpo da Requisição: `{"correntista_id": 1, "valor": 100.00}`

`/saque`
* Descrição: Realiza um saque da conta de um correntista.

* Corpo da Requisição: `{"correntista_id": 1, "valor": 50.00}`

`/pagamento`
* Descrição: Realiza um pagamento a partir da conta de um correntista.

* Corpo da Requisição: `{"correntista_id": 1, "valor": 25.00, "descricao": "Conta de luz"}`

`/transferencia`
* Descrição: Realiza uma transferência entre contas de correntistas.

* Corpo da Requisição: `{"correntista_id_origem": 1, "correntista_id_destino": 2, "valor": 15.00}`

---

### Equipe: 
* Brunno de Melo Marques
* Emanuel Correia Tavares
