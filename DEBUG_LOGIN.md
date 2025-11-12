# 🔍 Guia de Debug - Problema de Login

## Status Atual
✅ Backend rodando em: http://localhost:8000
✅ Frontend rodando em: http://localhost:5173
✅ API de login funcionando
✅ Endpoint /usuarios/me/ funcionando
✅ Senha resetada: admin / admin123

## Problema
O login não passa da tela, mesmo sem dar erro.

## Logs Adicionados
Adicionei logs detalhados no arquivo `frontend/src/stores/auth.js` para rastrear o problema.

## Como Debugar

### 1. Abra o Console do Navegador
1. Acesse: http://localhost:5173
2. Pressione F12 para abrir o DevTools
3. Vá na aba "Console"

### 2. Tente Fazer Login
- **Username:** admin
- **Password:** admin123

### 3. Verifique os Logs no Console
Você deve ver logs como:
```
🔐 Tentando fazer login... {username: "admin"}
✅ Login bem-sucedido, tokens recebidos
📡 Buscando dados do usuário...
📡 fetchUser: Importando API...
📡 fetchUser: Fazendo requisição para /usuarios/me/
📡 fetchUser: Resposta recebida: {id: 1, username: "admin", ...}
✅ Dados do usuário carregados: {id: 1, username: "admin", ...}
```

### 4. Possíveis Problemas

#### A) Se aparecer erro de CORS:
```
Access to XMLHttpRequest at 'http://localhost:8000/api/auth/login/' 
from origin 'http://localhost:5173' has been blocked by CORS policy
```
**Solução:** Verifique se o backend tem CORS configurado corretamente.

#### B) Se aparecer erro 401 ou 403 no /usuarios/me/:
```
❌ Failed to fetch user: Error: Request failed with status code 401
```
**Solução:** O token JWT pode estar inválido ou expirado.

#### C) Se aparecer erro de rede:
```
❌ Login failed: Network Error
```
**Solução:** Verifique se o backend está rodando.

#### D) Se não aparecer NENHUM log:
O JavaScript pode estar com erro de sintaxe. Verifique a aba "Console" por erros.

### 5. Verificar Network Tab
1. Abra a aba "Network" no DevTools
2. Tente fazer login
3. Verifique as requisições:
   - POST http://localhost:8000/api/auth/login/ - deve retornar 200
   - GET http://localhost:8000/api/usuarios/me/ - deve retornar 200

### 6. Verificar LocalStorage
1. No DevTools, vá em "Application" > "Local Storage" > "http://localhost:5173"
2. Verifique se existem as chaves:
   - `access_token`
   - `refresh_token`

## Testes Manuais via API

### Teste 1: Login
```bash
cd backend
.\venv\Scripts\activate
python test_api_login.py
```

### Teste 2: Buscar Usuário
```bash
python test_me_endpoint.py
```

### Teste 3: Autenticação Django
```bash
python test_login.py
```

## Próximos Passos

Depois de verificar os logs no console do navegador, me informe:
1. Quais logs aparecem no console?
2. Há algum erro na aba Network?
3. Os tokens são salvos no LocalStorage?
4. Para onde o navegador tenta redirecionar após o login?

## Comandos para Reiniciar os Servidores

### Backend
```bash
cd backend
.\venv\Scripts\activate
python manage.py runserver
```

### Frontend
```bash
cd frontend
npm run dev
```
