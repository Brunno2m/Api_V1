# 🔌 WebSocket - Guia de Implementação

## 📋 Visão Geral

Este projeto agora possui suporte completo a **WebSocket** usando **Flask-SocketIO** para comunicação em tempo real entre servidor e cliente.

## ✨ Funcionalidades Implementadas

### 🔔 Notificações em Tempo Real
Todas as operações bancárias agora emitem notificações instantâneas:
- ✅ **Depósitos** - Notificação quando um depósito é realizado
- ✅ **Saques** - Notificação quando um saque é processado
- ✅ **Transferências** - Notificação de transferências realizadas
- ✅ **Pagamentos** - Confirmação de pagamentos efetuados

### 📊 Atualização Automática
- Dashboard atualiza automaticamente após cada operação
- Saldos são atualizados em tempo real
- Movimentações aparecem instantaneamente na interface

### 🔐 Segurança
- Autenticação JWT via WebSocket
- Verificação de token para todos os eventos
- Isolamento de dados por usuário (rooms)

## 🛠️ Tecnologias Utilizadas

- **Flask-SocketIO 5.3.6** - Integração WebSocket com Flask
- **python-socketio 5.11.0** - Biblioteca Socket.IO para Python
- **eventlet 0.35.2** - Servidor assíncrono para WebSocket
- **Socket.IO Client 4.5.4** - Cliente JavaScript (CDN)

## 🚀 Como Usar

### 1. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 2. Iniciar o Servidor

```bash
python api.py
```

O servidor iniciará em `http://0.0.0.0:5000` com suporte WebSocket ativado.

### 3. Acessar a Interface

Abra o navegador em `http://localhost:5000`

## 📡 Eventos WebSocket

### Eventos do Cliente → Servidor

#### `autenticar`
Autentica o cliente usando token JWT.

```javascript
socket.emit('autenticar', { token: 'seu-token-jwt' });
```

**Resposta:**
```javascript
socket.on('autenticado', function(data) {
    // data.mensagem: "Autenticado com sucesso"
    // data.usuario_id: ID do usuário
    // data.email: Email do usuário
});
```

#### `solicitar_saldo`
Solicita o saldo atualizado de uma conta específica.

```javascript
socket.emit('solicitar_saldo', {
    token: 'seu-token-jwt',
    correntista_id: 1
});
```

**Resposta:**
```javascript
socket.on('saldo_atualizado', function(data) {
    // data.CorrentistaID: ID da conta
    // data.NomeCorrentista: Nome do titular
    // data.Saldo: Saldo atual
});
```

### Eventos do Servidor → Cliente

#### `conexao`
Confirmação de conexão estabelecida.

```javascript
socket.on('conexao', function(data) {
    console.log(data.mensagem); // "Conectado ao servidor WebSocket"
});
```

#### `notificacao`
Notificação de operação bancária realizada.

```javascript
socket.on('notificacao', function(data) {
    // data.tipo: 'deposito' | 'saque' | 'transferencia' | 'pagamento'
    // data.mensagem: Mensagem descritiva
    // data.timestamp: Data/hora da operação
    // data.dados: Dados adicionais (valor, descrição, etc.)
});
```

#### `saldo_atualizado`
Saldo de uma conta foi atualizado.

```javascript
socket.on('saldo_atualizado', function(data) {
    // Atualizar interface com novo saldo
});
```

#### `erro`
Erro durante processamento de evento.

```javascript
socket.on('erro', function(data) {
    console.error(data.mensagem);
});
```

## 🔧 Estrutura do Código

### Backend (`api.py`)

```python
from flask_socketio import SocketIO, emit, disconnect, join_room

# Inicializar SocketIO
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

# Função para emitir notificações
def emitir_notificacao(usuario_id, tipo, mensagem, dados=None):
    payload = {
        'tipo': tipo,
        'mensagem': mensagem,
        'timestamp': datetime.utcnow().isoformat(),
        'dados': dados or {}
    }
    socketio.emit('notificacao', payload, room=f'user_{usuario_id}')

# Eventos WebSocket
@socketio.on('connect')
def handle_connect():
    emit('conexao', {'mensagem': 'Conectado ao servidor WebSocket'})

@socketio.on('autenticar')
def handle_autenticar(data):
    # Autenticar e adicionar à sala do usuário
    join_room(f'user_{usuario_id}')

# Iniciar servidor
if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
```

### Frontend (`index.html`)

```javascript
// Inicializar conexão
socket = io({
    transports: ['websocket', 'polling'],
    reconnection: true
});

// Eventos
socket.on('connect', function() {
    console.log('Conectado!');
    if (authToken) {
        socket.emit('autenticar', { token: authToken });
    }
});

socket.on('notificacao', function(data) {
    mostrarNotificacao(data.mensagem, 'success');
    carregarDashboard(); // Atualizar interface
});
```

## 🎯 Fluxo de Notificações

1. **Usuário realiza uma operação** (ex: depósito)
2. **Backend processa** a operação no banco de dados
3. **Backend emite notificação** via WebSocket
4. **Frontend recebe** a notificação em tempo real
5. **Interface atualiza** automaticamente (saldo, movimentações)
6. **Notificação visual** é exibida ao usuário

## 🔍 Indicador de Conexão

A interface exibe um indicador visual do status da conexão WebSocket:

- 🟢 **Verde** - Conectado (notificações em tempo real ativas)
- 🔴 **Vermelho** - Desconectado (modo offline)

Localização: Canto inferior direito da tela

## 📦 Dependências Atualizadas

```txt
# requirements.txt
Flask==3.1.2
flask-socketio==5.3.6
python-socketio==5.11.0
eventlet==0.35.2
mysql-connector-python==9.4.0
PyJWT==2.8.0
bcrypt==4.1.2
python-dotenv==1.0.0
```

## 🐛 Troubleshooting

### WebSocket não conecta

1. Verificar se o servidor está rodando com `socketio.run()` (não `app.run()`)
2. Verificar firewall/portas bloqueadas
3. Verificar console do navegador para erros

### Notificações não aparecem

1. Verificar autenticação WebSocket após login
2. Verificar console do navegador (tab Network → WS)
3. Verificar se o token JWT está válido

### Reconexão automática falha

O Socket.IO tenta reconectar automaticamente até 5 vezes. Após isso, recarregue a página.

## 📝 Notas Importantes

- ⚠️ **Eventlet está deprecated** - Considere migrar para outro async framework no futuro
- 🔒 **CORS está aberto** (`cors_allowed_origins="*"`) - Restringir em produção
- 🚀 **Debug mode ativo** - Desativar em produção (`debug=False`)

## 🎉 Próximas Melhorias

- [ ] Notificações de múltiplos usuários em transferências
- [ ] Histórico de notificações
- [ ] Sons de notificação personalizados
- [ ] Chat em tempo real entre usuários
- [ ] Indicador de usuários online

## 📚 Referências

- [Flask-SocketIO Documentation](https://flask-socketio.readthedocs.io/)
- [Socket.IO Client Documentation](https://socket.io/docs/v4/client-api/)
- [Eventlet Documentation](https://eventlet.readthedocs.io/)

---

**Desenvolvido com ❤️ usando Flask-SocketIO**
