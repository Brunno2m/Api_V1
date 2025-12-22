# 🚨 SOLUÇÃO DE PROBLEMAS - Página não carrega

## ❌ Problema Identificado

**MYSQL NÃO ESTÁ CONECTADO**

O diagnóstico mostrou que o MySQL não está acessível em `localhost:3306`.

---

## ✅ SOLUÇÕES PASSO A PASSO

### 🔧 Solução 1: Iniciar MySQL no XAMPP (Windows/Mac/Linux)

#### Windows:
1. Abra o **XAMPP Control Panel**
2. Clique em **Start** ao lado de **MySQL**
3. Aguarde até aparecer o fundo verde
4. Verifique se a porta está correta (3306)

#### Mac:
1. Abra o **XAMPP** (ou MAMP)
2. Clique em **Start Servers**
3. Verifique se MySQL está rodando

#### Linux:
```bash
sudo /opt/lampp/lampp startmysql
```

---

### 🔧 Solução 2: Verificar se MySQL está rodando

**Windows (CMD):**
```cmd
netstat -ano | findstr :3306
```

**Mac/Linux:**
```bash
lsof -i :3306
# ou
ps aux | grep mysql
```

Se não aparecer nada, o MySQL não está rodando.

---

### 🔧 Solução 3: Importar o Banco de Dados

1. Abra o navegador e acesse: **http://localhost/phpmyadmin**

2. Clique em **"Novo"** (ou **"New"**)

3. Nome do banco: `SistemasCorporativos`

4. Clique em **"Criar"**

5. Selecione o banco criado

6. Clique na aba **"Importar"** (ou **"Import"**)

7. Clique em **"Escolher arquivo"** e selecione:
   ```
   database/SistemasCorporativos.sql
   ```

8. Clique em **"Executar"** (ou **"Go"**)

9. Aguarde a mensagem de sucesso ✅

---

### 🔧 Solução 4: Configurar Credenciais (se necessário)

Se suas credenciais do MySQL forem diferentes, edite o arquivo `.env`:

```env
# .env
DB_HOST=localhost
DB_USER=root            # ← Seu usuário MySQL
DB_PASSWORD=            # ← Sua senha (vazia no XAMPP por padrão)
DB_NAME=SistemasCorporativos
```

---

### 🔧 Solução 5: MySQL em porta diferente

Se seu MySQL estiver em outra porta (ex: 3307):

```env
# .env
DB_HOST=localhost:3307
DB_USER=root
DB_PASSWORD=
DB_NAME=SistemasCorporativos
```

---

## 🧪 TESTAR SE FUNCIONOU

Execute o diagnóstico novamente:

```bash
python diagnostico.py
```

Se aparecer:
```
✓ Conexão com MySQL estabelecida!
✓ Banco de dados acessível
✅ TUDO PRONTO!
```

Então pode iniciar o servidor! 🎉

---

## 🚀 INICIAR O SERVIDOR

### Método 1: Com eventlet (WebSocket completo)

```bash
python api.py
```

Se aparecer erro do eventlet, use o Método 2.

### Método 2: Sem eventlet (sem WebSocket)

Crie um arquivo `run.py`:

```python
from api import app

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
```

Execute:
```bash
python run.py
```

> ⚠️ **Nota:** Sem eventlet, o WebSocket não funcionará, mas a API REST funcionará normalmente.

---

## 🌐 ACESSAR A PÁGINA

Depois que o servidor iniciar e aparecer:

```
* Running on http://0.0.0.0:5000
* Running on http://127.0.0.1:5000
```

Abra o navegador em:
- **http://localhost:5000**
- ou **http://127.0.0.1:5000**

---

## 🔍 OUTROS PROBLEMAS COMUNS

### 1. Erro: "Address already in use"

A porta 5000 está ocupada.

**Solução:**
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID [número_do_PID] /F

# Linux/Mac
lsof -ti:5000 | xargs kill -9
```

### 2. Erro: "ModuleNotFoundError"

Falta instalar dependências.

**Solução:**
```bash
pip install -r requirements.txt
```

### 3. Página carrega mas dá erro 500

Problema no banco de dados.

**Solução:**
1. Verifique se o banco foi importado corretamente
2. Execute: `python diagnostico.py`
3. Veja os logs no terminal onde rodou `python api.py`

### 4. WebSocket não conecta

**Solução:**
1. Certifique-se de que iniciou com `python api.py` (não `flask run`)
2. Verifique se o eventlet está instalado: `pip install eventlet`
3. Se persistir, use o `run.py` sem WebSocket

---

## 📋 CHECKLIST COMPLETO

Antes de iniciar o servidor, verifique:

- [ ] XAMPP está aberto e rodando
- [ ] MySQL está ativo (luz verde no XAMPP)
- [ ] Banco `SistemasCorporativos` foi criado
- [ ] Arquivo SQL foi importado
- [ ] Arquivo `.env` existe e está configurado
- [ ] Dependências instaladas (`pip install -r requirements.txt`)
- [ ] Porta 5000 está livre
- [ ] Executou `python diagnostico.py` com sucesso

---

## 🆘 ÚLTIMA TENTATIVA

Se nada funcionar, tente esta versão simplificada:

**1. Crie `simple_run.py`:**

```python
from flask import Flask, jsonify
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route('/')
def test():
    try:
        conn = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            database=os.getenv('DB_NAME', 'SistemasCorporativos')
        )
        return jsonify({"status": "OK", "message": "MySQL conectado!"})
    except Exception as e:
        return jsonify({"status": "ERROR", "message": str(e)}), 500

if __name__ == '__main__':
    print("Servidor de teste iniciando em http://localhost:5000")
    app.run(debug=True, port=5000)
```

**2. Execute:**
```bash
python simple_run.py
```

**3. Acesse:** http://localhost:5000

Se ver `{"status": "OK", "message": "MySQL conectado!"}`, o problema está no eventlet.

---

## 💬 PRECISA DE MAIS AJUDA?

Execute o diagnóstico e me envie o resultado completo:

```bash
python diagnostico.py > diagnostico.txt
```

Depois abra `diagnostico.txt` e me mostre o conteúdo.

---

**Última atualização:** 22/12/2025
