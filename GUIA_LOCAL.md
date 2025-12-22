# 🖥️ GUIA PARA RODAR LOCALMENTE COM XAMPP

## ⚠️ IMPORTANTE: Este projeto está em um Codespace (ambiente remoto)

Para rodar **localmente** no seu computador com XAMPP, siga estes passos:

---

## 📥 PASSO 1: Baixar o Projeto para seu Computador

### Opção A: Clonar via Git
```bash
git clone https://github.com/Brunno2m/Api_V1.git
cd Api_V1
```

### Opção B: Baixar ZIP
1. Acesse: https://github.com/Brunno2m/Api_V1
2. Clique em **Code** → **Download ZIP**
3. Extraia o arquivo em uma pasta (ex: `C:\projetos\Api_V1`)
4. Abra o terminal/CMD nesta pasta

---

## 🔧 PASSO 2: Configurar o XAMPP

### 1. Iniciar o XAMPP

1. Abra o **XAMPP Control Panel**
2. Clique em **Start** ao lado de:
   - ✅ **Apache**
   - ✅ **MySQL**
3. Aguarde até os dois ficarem com fundo **verde**

### 2. Verificar a Porta do MySQL

Se o MySQL não iniciar na porta 3306, pode estar em 3307 ou outra.

**Para verificar:**
- Clique em **Config** ao lado de MySQL
- Veja a linha `port=` no arquivo `my.ini`
- Anote a porta (ex: 3306 ou 3307)

---

## 💾 PASSO 3: Importar o Banco de Dados

### 1. Acessar o phpMyAdmin

Abra o navegador e vá para:
```
http://localhost/phpmyadmin
```

ou

```
http://localhost:8080/phpmyadmin
```

### 2. Criar o Banco de Dados

1. Clique em **"Novo"** (ou **"New"**) no menu lateral
2. Nome do banco: `SistemasCorporativos`
3. Cotejamento: `utf8mb4_general_ci`
4. Clique em **"Criar"**

### 3. Importar as Tabelas

1. Selecione o banco `SistemasCorporativos` no menu lateral
2. Clique na aba **"Importar"** (ou **"Import"**)
3. Clique em **"Escolher arquivo"**
4. Navegue até a pasta do projeto
5. Selecione: `database/SistemasCorporativos.sql`
6. Clique em **"Executar"** (ou **"Go"**)
7. Aguarde a mensagem: ✅ **"Importação finalizada com êxito"**

---

## 🐍 PASSO 4: Instalar Python e Dependências

### 1. Verificar se Python está instalado

Abra o **CMD** ou **Terminal** e digite:

```bash
python --version
```

Se não tiver Python instalado:
- Baixe em: https://www.python.org/downloads/
- ✅ **IMPORTANTE:** Marque a opção **"Add Python to PATH"**

### 2. Instalar as Dependências

No terminal, dentro da pasta do projeto:

```bash
pip install -r requirements.txt
```

Aguarde a instalação de todos os pacotes.

---

## ⚙️ PASSO 5: Configurar o Arquivo .env

### 1. Criar o arquivo .env

Na pasta raiz do projeto, crie um arquivo chamado `.env` (sem extensão)

**Windows:** Use o Bloco de Notas e salve como `.env` (selecione "Todos os arquivos")

### 2. Adicionar as Configurações

Cole este conteúdo no arquivo `.env`:

```env
# Configurações do Banco de Dados MySQL
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=
DB_NAME=SistemasCorporativos

# Configurações JWT
JWT_SECRET_KEY=sua_chave_secreta_super_segura_aqui
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24
```

**Se seu MySQL estiver em outra porta:**
```env
DB_HOST=localhost:3307
```

**Se você configurou senha no MySQL:**
```env
DB_PASSWORD=sua_senha_aqui
```

---

## ✅ PASSO 6: Testar a Conexão

Execute o teste para verificar se está tudo OK:

```bash
python teste_xampp.py
```

**Resultado esperado:**
```
✅ MySQL está acessível!
✅ Banco 'SistemasCorporativos' existe!
✅ 5 tabelas encontradas
✅ XAMPP ESTÁ FUNCIONANDO CORRETAMENTE!
```

Se aparecer algum erro, leia a mensagem e corrija conforme indicado.

---

## 🚀 PASSO 7: Iniciar o Servidor

### Opção 1: Com WebSocket (Recomendado)

```bash
python run_server.py
```

### Opção 2: Sem WebSocket (Se der erro)

```bash
python simple_server.py
```

### Opção 3: Servidor Original

```bash
python api.py
```

**Aguarde aparecer:**
```
✅ MySQL conectado
🌐 Acesse em seu navegador:
   • http://localhost:5000
```

---

## 🌐 PASSO 8: Acessar a Aplicação

1. Abra seu navegador favorito (Chrome, Edge, Firefox...)

2. Digite na barra de endereços:
   ```
   http://localhost:5000
   ```

3. A página deve carregar mostrando a tela de login! 🎉

---

## 🐛 PROBLEMAS COMUNS

### ❌ "Porta 5000 já está em uso"

**Windows (CMD):**
```cmd
netstat -ano | findstr :5000
taskkill /PID [número] /F
```

**PowerShell:**
```powershell
Get-Process -Id (Get-NetTCPConnection -LocalPort 5000).OwningProcess | Stop-Process
```

### ❌ "ModuleNotFoundError: No module named 'flask'"

```bash
pip install -r requirements.txt
```

### ❌ "Access denied for user 'root'@'localhost'"

Você tem senha no MySQL. Edite o `.env`:
```env
DB_PASSWORD=sua_senha_aqui
```

### ❌ "Can't connect to MySQL server"

1. Verifique se o MySQL está rodando (verde no XAMPP)
2. Tente mudar a porta no `.env`:
   ```env
   DB_HOST=localhost:3307
   ```
3. Verifique se não tem firewall bloqueando

### ❌ Página carrega mas dá erro 500

Execute o diagnóstico:
```bash
python diagnostico.py
```

Veja os erros e corrija conforme indicado.

---

## 📋 CHECKLIST FINAL

Antes de iniciar, certifique-se:

- [ ] XAMPP está aberto
- [ ] Apache e MySQL estão **VERDES** no XAMPP
- [ ] Banco `SistemasCorporativos` foi criado
- [ ] Arquivo `.sql` foi importado com sucesso
- [ ] Arquivo `.env` foi criado com as configurações
- [ ] Python está instalado
- [ ] Dependências foram instaladas (`pip install -r requirements.txt`)
- [ ] Teste `python teste_xampp.py` passou ✅
- [ ] Porta 5000 está livre

---

## 🎯 ESTRUTURA ESPERADA

Sua pasta deve estar assim:

```
Api_V1/
├── api.py
├── run_server.py
├── simple_server.py
├── teste_xampp.py
├── diagnostico.py
├── requirements.txt
├── .env                    ← Você criou este
├── database/
│   └── SistemasCorporativos.sql
└── templates/
    └── index.html
```

---

## 💡 DICA PRO

### Criar Usuário de Teste

Depois que o servidor estiver rodando:

1. Acesse http://localhost:5000
2. Clique em **"Registre-se"**
3. Preencha:
   - Nome: Teste
   - Email: teste@teste.com
   - Senha: 123456
4. Clique em **"Registrar"**
5. Pronto! Você está logado 🎉

---

## 🆘 AINDA COM PROBLEMAS?

Execute o diagnóstico completo:

```bash
python diagnostico.py > resultado.txt
```

Abra o arquivo `resultado.txt` e veja o que está errado.

---

## 📞 SUPORTE

Se precisar de ajuda, envie:

1. Sistema operacional (Windows, Mac, Linux)
2. Versão do Python (`python --version`)
3. Resultado do `python teste_xampp.py`
4. Mensagem de erro completa (se houver)

---

**Última atualização:** 22/12/2025  
**Testado em:** Windows 10/11 com XAMPP 8.2
