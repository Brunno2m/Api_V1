# API de Movimentações Financeiras com Autenticação JWT

Uma API RESTful segura para gerenciar e consultar movimentações financeiras, desenvolvida com **Flask** e **Python**, utilizando **MySQL** como banco de dados e **JWT** para autenticação. Este projeto demonstra a implementação de APIs seguras com controle de acesso baseado em tokens.

---

## 🚀 Tecnologias Utilizadas

* **Python 3.x:** Linguagem de programação.
* **Flask:** Micro-framework web para a criação da API.
* **MySQL:** Sistema de gerenciamento de banco de dados.
* **JWT (JSON Web Tokens):** Sistema de autenticação stateless.
* **bcrypt:** Hash seguro para senhas.
* **python-dotenv:** Gerenciamento de variáveis de ambiente.
* **XAMPP:** Ambiente de desenvolvimento para o servidor web e o banco de dados.
* **`mysql-connector-python`:** Driver para conectar o Python ao MySQL.

---

## � Funcionalidades de Segurança

* **Autenticação JWT:** Todos os endpoints protegidos requerem token válido.
* **Hash de senhas:** Senhas são criptografadas com bcrypt.
* **Controle de acesso:** Usuários só podem acessar seus próprios dados.
* **Validação de entrada:** Verificação de dados antes do processamento.
* **Variáveis de ambiente:** Configurações sensíveis protegidas.

---

## �📋 Pré-requisitos

Para rodar este projeto localmente, você precisa ter:

* **Python 3.x** instalado.
* **XAMPP** instalado e com os módulos **Apache** e **MySQL** em execução.

---

## 🛠️ Instalação e Configuração

Siga os passos abaixo para configurar o ambiente e rodar a API.

### 1. Clonar o Repositório

```bash
git clone https://github.com/Brunno2m/Api_V1.git
cd Api_V1
```

### 2. Configurar o Banco de Dados

* Abra o painel de controle do XAMPP e inicie os módulos Apache e MySQL.

* Acesse o phpMyAdmin pelo seu navegador: `http://localhost/phpmyadmin`.

* Vá para a aba `SQL` e execute o script `SistemasCorporativos.sql` (disponível neste repositório) para criar o banco de dados, as tabelas, procedures e dados de exemplo.

### 3. Instalar as Dependências
No terminal, na pasta raiz do projeto, instale as bibliotecas Python necessárias:

```bash
pip install -r requirements.txt
```

### 4. Configurar Variáveis de Ambiente
Crie um arquivo `.env` na raiz do projeto com suas configurações:

```env
# Configurações do Banco de Dados
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=
DB_NAME=SistemasCorporativos

# Configurações JWT
JWT_SECRET_KEY=sua_chave_secreta_super_segura_aqui_mude_em_producao
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24
```

**⚠️ IMPORTANTE:** Altere a `JWT_SECRET_KEY` para uma chave segura e única em produção!

### 5. Rodar a API
No terminal, execute o comando para iniciar o servidor Flask:

```bash
python api.py
```

**Nota:** Se estiver usando ambiente virtual (recomendado), use o caminho completo:
```bash
# Windows
.venv/Scripts/python.exe api.py

# Linux/Mac
.venv/bin/python api.py
```

A API estará rodando em `http://127.0.0.1:5000`.

---

## 🔑 Autenticação

### Credenciais Padrão para Testes
- **Email:** `admin@teste.com`
- **Senha:** `123456`

---

## 🖥️ Endpoints da API

### 1. Endpoints de Autenticação (Públicos)

| Endpoint | Método | Descrição | Parâmetros |
| :--- | :--- | :--- | :--- |
| `/registro` | `POST` | Registra um novo usuário | `{"nome": "string", "email": "string", "senha": "string"}` |
| `/login` | `POST` | Autentica usuário e retorna JWT | `{"email": "string", "senha": "string"}` |

### 2. Endpoints Protegidos (Requerem Token JWT)

**Cabeçalho obrigatório:** `Authorization: Bearer <seu_token_jwt>`

| Endpoint | Método | Descrição | Parâmetros |
| :--- | :--- | :--- | :--- |
| `/perfil` | `GET` | Retorna dados do usuário logado | - |
| `/correntistas` | `GET` | Lista correntistas do usuário | - |
| `/movimentacoes` | `GET` | Lista todas as movimentações do usuário | - |
| `/extrato/<id>` | `GET` | Extrato de um correntista específico | - |
| `/deposito` | `POST` | Realiza depósito | `{"correntista_id": int, "valor": float}` |
| `/saque` | `POST` | Realiza saque | `{"correntista_id": int, "valor": float}` |
| `/pagamento` | `POST` | Realiza pagamento | `{"correntista_id": int, "valor": float, "descricao": "string"}` |
| `/transferencia` | `POST` | Realiza transferência | `{"correntista_id_origem": int, "correntista_id_destino": int, "valor": float}` |

---

## 📱 Interface Web

A aplicação inclui uma interface web completa com:

* **Sistema de login/registro**
* **Dashboard do usuário logado**
* **Testador de endpoints integrado**
* **Gerenciamento de sessão automático**

Acesse `http://127.0.0.1:5000` após iniciar o servidor.

---

## 🔒 Segurança Implementada

1. **Tokens JWT com expiração configurável**
2. **Hash bcrypt para senhas**
3. **Validação de propriedade de recursos**
4. **Sanitização de dados de entrada**
5. **Proteção contra acesso não autorizado**
6. **Configurações sensíveis em variáveis de ambiente**

---

## 🧪 Como Testar

### 1. Via Interface Web
1. Acesse `http://127.0.0.1:5000`
2. Faça login com `admin@teste.com` / `123456`
3. Teste todos os endpoints através da interface

### 2. Via cURL/Postman

**Login:**
```bash
curl -X POST http://127.0.0.1:5000/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@teste.com", "senha": "123456"}'
```

**Usar endpoints protegidos:**
```bash
curl -X GET http://127.0.0.1:5000/correntistas \
  -H "Authorization: Bearer SEU_TOKEN_AQUI"
```

---

## �️ Troubleshooting (Solução de Problemas)

### **Problema: "Table 'sistemascorporativos.usuarios' doesn't exist"**
**Causa:** A tabela de usuários não foi criada no banco de dados.

**Solução:**
1. Acesse phpMyAdmin: `http://localhost/phpmyadmin`
2. Selecione o banco `SistemasCorporativos`
3. Vá na aba "SQL" e execute o script completo `database/SistemasCorporativos.sql`

### **Problema: "Email ou senha incorretos" (mesmo com credenciais corretas)**
**Causa:** Hash da senha incorreto no banco de dados.

**Solução:**
Execute o script de correção:
```bash
python update_password.py
```
Este script atualiza o hash da senha do usuário admin para funcionar corretamente.

**Script de debug completo disponível:**
```bash
python debug_login.py
```
Este script verifica a conexão com o banco, usuário existente e oferece opção de recriar o hash da senha.

### **Problema: Erro de conexão com MySQL**
**Possíveis causas e soluções:**

1. **XAMPP não está rodando:**
   - Abra o XAMPP Control Panel
   - Inicie os serviços Apache e MySQL

2. **Credenciais incorretas no arquivo `.env`:**
   - Verifique se `DB_USER`, `DB_PASSWORD` e `DB_NAME` estão corretos
   - Para XAMPP padrão: usuário `root`, senha vazia

3. **Nome do banco incorreto:**
   - Certifique-se que o banco se chama exatamente `SistemasCorporativos`
   - Verifique case-sensitivity (maiúsculas/minúsculas)

### **Problema: Erro ao instalar dependências**
**Solução:**
```bash
# Certifique-se de estar usando o Python correto
pip install -r requirements.txt

# Ou especificamente para o ambiente virtual
.venv/Scripts/pip install -r requirements.txt
```

### **Problema: Porta 5000 já está em uso**
**Solução:**
Modifique a porta no final do arquivo `api.py`:
```python
if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Use porta diferente
```

---

## �🛡️ Melhorias de Segurança Implementadas

Comparado à versão anterior, esta versão inclui:

- ✅ **Autenticação JWT obrigatória**
- ✅ **Controle de acesso por usuário**
- ✅ **Hash seguro de senhas**
- ✅ **Validação robusta de entrada**
- ✅ **Configurações via variáveis de ambiente**
- ✅ **Verificação de propriedade de recursos**
- ✅ **Interface web com gerenciamento de sessão**

---

### Equipe: 
* Brunno de Melo Marques
* Emanuel Correia Tavares
