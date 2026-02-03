# 🏦 API de Movimentações Financeiras com JWT

API RESTful segura para gerenciar operações bancárias (depósitos, saques, transferências e pagamentos) com autenticação JWT, WebSocket em tempo real e interface web moderna.

## ✨ Principais Recursos

- 🔐 **Autenticação JWT** com tokens expiráveis
- 💰 **Operações bancárias completas** (depósito, saque, transferência, pagamento)
- 🔌 **WebSocket** para notificações em tempo real
- 🎨 **Interface web moderna** e responsiva
- 🛡️ **Segurança**: bcrypt, validação de dados, controle de acesso por usuário
- 📊 **Dashboard interativo** com visualização de saldos e extratos
- 🧪 **Testador de API integrado**

---

## 🚀 Tecnologias

- **Backend**: Python 3.x, Flask 3.1.2, Flask-SocketIO 5.3.6
- **Banco de Dados**: MySQL 8.x
- **Autenticação**: PyJWT 2.8.0, bcrypt 4.1.2
- **Frontend**: HTML5, CSS3, JavaScript (Socket.IO client)
- **Outros**: python-dotenv, mysql-connector-python

---

## 📋 Pré-requisitos

- Python 3.x instalado
- MySQL instalado (XAMPP, WAMP, ou MySQL standalone)
- Git (opcional, para clonar o repositório)

---

## ⚙️ Instalação e Configuração

### 1️⃣ Clonar o Repositório

```bash
git clone https://github.com/Brunno2m/Api_V1.git
cd Api_V1
```

Ou baixe o ZIP e extraia em uma pasta local.

### 2️⃣ Configurar o MySQL

#### Iniciar o MySQL
- **XAMPP**: Abra o Control Panel → Start **MySQL**
- **Outros**: Certifique-se que o serviço MySQL está rodando

#### Criar o Banco de Dados
1. Acesse: `http://localhost/phpmyadmin` (ou seu phpMyAdmin)
2. Clique em **"Novo"** / **"New"**
3. Nome: `SistemasCorporativos`
4. Cotejamento: `utf8mb4_general_ci`
5. Clique em **"Criar"**

#### Importar as Tabelas e Procedures
1. Selecione o banco `SistemasCorporativos` no menu lateral
2. Clique na aba **"Importar"**
3. Escolha o arquivo: `database/SistemasCorporativos.sql`
4. Clique em **"Executar"**
5. Aguarde: ✅ **"Importação finalizada com êxito"**

### 3️⃣ Instalar Dependências Python

```bash
# Recomendado: usar ambiente virtual
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# Instalar dependências
pip install -r requirements.txt
```

### 4️⃣ Configurar Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
# Configurações do Banco de Dados
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=root
DB_NAME=SistemasCorporativos

# Configurações JWT
JWT_SECRET_KEY=sua_chave_secreta_super_segura_aqui_mude_em_producao
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24
```

**⚠️ Notas:**
- Para XAMPP padrão, `DB_PASSWORD` geralmente é vazio ou `root`
- Se o MySQL estiver em porta diferente: `DB_HOST=localhost:3307`
- **Altere a `JWT_SECRET_KEY` em produção!**

### 5️⃣ Iniciar o Servidor

```bash
python api.py
```

ou

```bash
python run_server.py
```

Aguarde a mensagem:
```
✅ MySQL conectado
🌐 Acesse em seu navegador:
   • http://localhost:5000
```

### 6️⃣ Acessar a Aplicação

Abra o navegador em: **http://localhost:5000**

---

## 🔑 Credenciais de Teste

- **Email:** `admin@teste.com`
- **Senha:** `senha123`

Correntistas demo:
- **João Silva** (ID: 1) - Saldo: R$ 1.000,00
- **Maria Santos** (ID: 2) - Saldo: R$ 1.500,00

---

## 📡 Endpoints da API

### Endpoints Públicos

| Método | Endpoint | Descrição | Parâmetros |
|--------|----------|-----------|------------|
| POST | `/login` | Autenticar usuário | `{"email": "string", "senha": "string"}` |
| POST | `/registro` | Registrar novo usuário | `{"nome": "string", "email": "string", "senha": "string"}` |

### Endpoints Protegidos (Requerem JWT)

**Header obrigatório:** `Authorization: Bearer <token>`

| Método | Endpoint | Descrição | Parâmetros |
|--------|----------|-----------|------------|
| GET | `/perfil` | Dados do usuário logado | - |
| GET | `/correntistas` | Listar correntistas | - |
| GET | `/movimentacoes` | Listar movimentações | - |
| GET | `/extrato/<id>` | Extrato de correntista | - |
| POST | `/deposito` | Realizar depósito | `{"correntista_id": int, "valor": float}` |
| POST | `/saque` | Realizar saque | `{"correntista_id": int, "valor": float}` |
| POST | `/pagamento` | Realizar pagamento | `{"correntista_id": int, "valor": float, "descricao": "string"}` |
| POST | `/transferencia` | Realizar transferência | `{"correntista_id_origem": int, "correntista_id_destino": int, "valor": float}` |

---

## 🔌 WebSocket - Notificações em Tempo Real

### Recursos
- ✅ Notificações instantâneas de operações bancárias
- ✅ Atualização automática de saldos
- ✅ Dashboard atualizado em tempo real
- ✅ Autenticação JWT via WebSocket

### Eventos do Cliente → Servidor

#### `autenticar`
```javascript
socket.emit('autenticar', { token: 'seu-token-jwt' });
```

#### `solicitar_saldo`
```javascript
socket.emit('solicitar_saldo', {
    token: 'seu-token-jwt',
    correntista_id: 1
});
```

### Eventos do Servidor → Cliente

#### `conexao`
Confirmação de conexão estabelecida.

#### `notificacao`
```javascript
socket.on('notificacao', function(data) {
    // data.tipo: 'deposito' | 'saque' | 'transferencia' | 'pagamento'
    // data.mensagem: Mensagem descritiva
    // data.timestamp: Data/hora
    // data.dados: Dados adicionais
});
```

#### `saldo_atualizado`
```javascript
socket.on('saldo_atualizado', function(data) {
    // data.CorrentistaID
    // data.NomeCorrentista
    // data.Saldo
});
```

### Indicador Visual
🟢 **Verde** - Conectado (notificações ativas)  
🔴 **Vermelho** - Desconectado (modo offline)

---

## 🧪 Como Testar

### Via Interface Web (Recomendado)
1. Acesse `http://localhost:5000`
2. Faça login com `admin@teste.com` / `senha123`
3. Use o **Dashboard** para operações bancárias
4. Use o **Testador de API** para testar endpoints

### Via cURL

**Login:**
```bash
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@teste.com", "senha": "senha123"}'
```

**Resposta:**
```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "usuario": {"id": 1, "nome": "Admin", "email": "admin@teste.com"}
}
```

**Listar correntistas:**
```bash
curl -X GET http://localhost:5000/correntistas \
  -H "Authorization: Bearer SEU_TOKEN_AQUI"
```

---

## 🐛 Solução de Problemas

### ❌ Erro: "Can't connect to MySQL server"

**Causas possíveis:**
1. MySQL não está rodando
2. Porta incorreta (padrão: 3306)
3. Credenciais incorretas no `.env`

**Soluções:**
```bash
# Verificar se MySQL está rodando
# Windows (PowerShell)
Get-Service MySQL80

# Linux/Mac
sudo systemctl status mysql

# Verificar porta do MySQL
netstat -ano | findstr :3306  # Windows
lsof -i :3306  # Linux/Mac
```

- Verifique as credenciais no `.env`
- Se MySQL estiver em porta diferente: `DB_HOST=localhost:3307`
- Para XAMPP: abra Control Panel e clique em **Start** ao lado de MySQL

### ❌ Erro: "Table 'sistemascorporativos.usuarios' doesn't exist"

**Causa:** Banco não foi importado corretamente.

**Solução:**
1. Acesse phpMyAdmin
2. Selecione o banco `SistemasCorporativos`
3. Aba **SQL** → Execute o script `database/SistemasCorporativos.sql`

### ❌ Erro: "PROCEDURE sistemascorporativos.spDepositar does not exist"

**Causa:** Stored procedures não foram criadas.

**Solução:**
Execute o script SQL completo no phpMyAdmin ou use:
```bash
python check_procedures.py
```

As procedures necessárias:
- `spDepositar` - Depósitos
- `spSacar` - Saques
- `spPagar` - Pagamentos
- `spTransferir` - Transferências

### ❌ Erro: "Address already in use" (Porta 5000 ocupada)

**Windows:**
```powershell
# Encontrar processo
Get-NetTCPConnection -LocalPort 5000 | Select-Object OwningProcess

# Matar processo (substitua PID)
Stop-Process -Id PID -Force
```

**Linux/Mac:**
```bash
lsof -ti:5000 | xargs kill -9
```

### ❌ Erro: "ModuleNotFoundError"

**Solução:**
```bash
pip install -r requirements.txt
```

### ❌ Login retorna "Email ou senha incorretos" (mesmo com credenciais corretas)

**Causa:** Hash de senha incorreto ou usuário não existe.

**Solução:**
```bash
# Execute o script de correção
python update_password.py

# Ou verifique o login
python debug_login.py
```

### ❌ WebSocket não conecta

**Soluções:**
1. Certifique-se de iniciar com `python api.py` (não `flask run`)
2. Verifique console do navegador (F12 → Console/Network → WS)
3. Firewall pode estar bloqueando - libere porta 5000

### ❌ Erro 500 na interface

**Solução:**
1. Verifique terminal onde rodou `python api.py` para ver logs
2. Verifique se todas as tabelas e procedures foram criadas
3. Verifique credenciais do banco no `.env`

---

## 🛡️ Segurança Implementada

- ✅ **Autenticação JWT obrigatória** para endpoints protegidos
- ✅ **Hash bcrypt** para senhas (salt automático)
- ✅ **Controle de acesso por usuário** (isolamento de dados)
- ✅ **Validação de entrada** em todas as operações
- ✅ **Tokens com expiração** configurável (padrão: 24h)
- ✅ **Variáveis de ambiente** para dados sensíveis
- ✅ **Verificação de propriedade** de recursos
- ✅ **CORS configurável** (padrão: todas as origens)

**⚠️ Produção:**
- Altere `JWT_SECRET_KEY` para valor único e seguro
- Configure `cors_allowed_origins` com domínios específicos
- Desative debug mode: `debug=False`
- Use HTTPS
- Configure rate limiting

---

## 📁 Estrutura do Projeto

```
Api_V1/
├── api.py                      # Aplicação principal
├── run_server.py              # Script para iniciar servidor
├── simple_server.py           # Servidor simplificado (sem WebSocket)
├── requirements.txt           # Dependências Python
├── .env                       # Variáveis de ambiente (criar manualmente)
├── .gitignore                 # Arquivos ignorados pelo Git
├── database/
│   └── SistemasCorporativos.sql   # Schema do banco de dados
├── templates/
│   └── index.html             # Interface web
├── update_password.py         # Script para atualizar senha
├── debug_login.py            # Script de debug de login
└── check_procedures.py       # Verificar stored procedures
```

---

## 🎨 Interface Web

### Recursos da Interface
- 🏦 **Dashboard bancário** com cards informativos
- 💰 **Modais interativos** para operações financeiras
- 📊 **Visualização de extratos** em tempo real
- 🔄 **Testador de API** integrado para desenvolvedores
- 📱 **Design responsivo** (desktop e mobile)
- 🎨 **Tema moderno** com gradientes e Font Awesome icons
- 🔐 **Gerenciamento automático** de sessão JWT
- 🔔 **Notificações visuais** de feedback
- 🟢 **Indicador de conexão** WebSocket

---

## 📦 Stored Procedures

Todas as procedures incluem:
- ✅ Validação de saldo antes de débitos
- ✅ Atualização automática de saldos
- ✅ Tratamento de erros com mensagens claras
- ✅ Verificação de existência de beneficiários

### `spDepositar(p_CorrentistaID, p_Valor, p_Descricao)`
Credita valor na conta.

### `spSacar(p_CorrentistaID, p_Valor, p_Descricao)`
Debita valor da conta (valida saldo).

### `spPagar(p_CorrentistaID, p_Valor, p_Descricao)`
Realiza pagamento (debita e registra descrição).

### `spTransferir(p_CorrentistaOrigem, p_CorrentistaDestino, p_Valor)`
Transfere valor entre contas (valida saldo e existência).

---

## 👥 Desenvolvedores

- **Brunno de Melo Marques**
- **Emanuel Correia Tavares**

---

## 📄 Licença

Este é um projeto acadêmico/demonstração. Use como referência para aprendizado.

---

## 🔗 Repositório

**GitHub:** [https://github.com/Brunno2m/Api_V1](https://github.com/Brunno2m/Api_V1)

---

## 📝 Notas Técnicas

### SocketIO
- **Modo assíncrono:** `threading` (compatível com Python 3.14+)
- **Eventlet descontinuado:** Não use versões > 0.35.2 para compatibilidade

### MySQL
- **Encoding:** UTF-8 (utf8mb4_general_ci)
- **TipoOperacao:** CHAR(1) - 'C' (Crédito) ou 'D' (Débito)
- **Descricao:** VARCHAR(50) - truncado automaticamente

### JWT
- **Algoritmo:** HS256
- **Expiração padrão:** 24 horas
- **Header:** `Authorization: Bearer <token>`

---

**Última atualização:** Fevereiro 2026  
**Versão:** 1.0
