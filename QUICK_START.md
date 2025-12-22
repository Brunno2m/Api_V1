# 🚀 Quick Start - Rodando Localmente

## O Problema

Você está no **GitHub Codespace** (nuvem) tentando acessar o **MySQL do XAMPP** (seu computador).  
Isso **não funciona** porque são máquinas diferentes!

## A Solução

**Clone o projeto para sua máquina local** onde o XAMPP está rodando.

---

## 📋 Passos Rápidos

### 1. No VS Code do seu computador (não no Codespace)

Abra o terminal (Ctrl + ') e execute:

```bash
# Clonar o repositório
git clone https://github.com/Brunno2m/Api_V1.git

# Entrar na pasta
cd Api_V1

# Instalar dependências Python
pip install -r requirements.txt
```

### 2. Criar arquivo .env

Crie um arquivo chamado `.env` na raiz do projeto com:

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=
DB_NAME=SistemasCorporativos
JWT_SECRET_KEY=sua_chave_secreta_aqui
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24
```

### 3. Importar o banco de dados

1. Abra: http://localhost/phpmyadmin
2. Crie um banco chamado: `SistemasCorporativos`
3. Selecione o banco → Importar
4. Escolha o arquivo: `database/SistemasCorporativos.sql`
5. Clique em "Executar"

### 4. Testar a conexão

```bash
python teste_xampp.py
```

Se aparecer ✅ está tudo certo!

### 5. Iniciar o servidor

```bash
python api.py
```

ou

```bash
python run_server.py
```

### 6. Acessar no navegador

Abra: **http://localhost:5000**

---

## ✅ Pronto!

A página deve carregar normalmente agora! 🎉

---

## 🔄 Fluxo de Trabalho Recomendado

- **Codespace**: Para editar código e fazer commits
- **VS Code Local**: Para rodar e testar com XAMPP

---

## 🆘 Problemas?

Execute o diagnóstico:

```bash
python diagnostico.py
```

E siga as instruções que aparecerem.
