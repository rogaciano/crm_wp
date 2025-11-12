# 🚀 Guia de Instalação Rápida - CRM de Vendas

## ⚡ Setup Rápido (15 minutos)

### 1️⃣ Configurar Banco de Dados MySQL (WAMP)

```sql
-- Acesse o phpMyAdmin do WAMP (http://localhost/phpmyadmin/)
-- Ou use o console MySQL:

-- Criar banco de dados
CREATE DATABASE crm_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Verificar se foi criado
SHOW DATABASES;
```

**Usando phpMyAdmin:**
1. Abrir `http://localhost/phpmyadmin/`
2. Clicar em "Novo" (New)
3. Nome do banco: `crm_db`
4. Collation: `utf8mb4_unicode_ci`
5. Clicar em "Criar" (Create)

### 2️⃣ Configurar Backend Django

```powershell
# Navegar para backend
cd c:\projetos\crm_wp\backend

# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
.\venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt

# Criar arquivo .env
copy .env.example .env

# Editar .env (usar Notepad ou VSCode)
notepad .env
```

**Configurar o arquivo .env:**
```env
DEBUG=True
SECRET_KEY=django-insecure-change-this-in-production-12345
ALLOWED_HOSTS=localhost,127.0.0.1

# MySQL (WAMP)
DB_NAME=crm_db
DB_USER=root
DB_PASSWORD=
DB_HOST=localhost
DB_PORT=3306

CORS_ALLOWED_ORIGINS=http://localhost:8080,http://localhost:5173
```

**Nota:** Se seu WAMP tem senha no MySQL, coloque-a em `DB_PASSWORD`

```powershell
# Criar estrutura do banco de dados
python manage.py makemigrations
python manage.py migrate

# Criar dados iniciais
python manage.py shell < setup_database.py

# Iniciar servidor
python manage.py runserver
```

✅ Backend rodando em: **http://localhost:8000**

### 3️⃣ Configurar Frontend Vue.js

**Abrir novo terminal PowerShell:**

```powershell
# Navegar para frontend
cd c:\projetos\crm_wp\frontend

# Instalar dependências
npm install

# Criar arquivo .env
copy .env.example .env

# Iniciar servidor de desenvolvimento
npm run dev
```

✅ Frontend rodando em: **http://localhost:5173**

---

## 🎯 Acessar o Sistema

### Acesso Web
Abrir navegador: **http://localhost:5173**

### Usuários de Teste

| Usuário | Senha | Perfil | Descrição |
|---------|-------|--------|-----------|
| admin | admin123 | Administrador | Acesso total ao sistema |
| resp_sul | resp123 | Responsável | Gerencia Canal Sul |
| vendedor1 | vend123 | Vendedor | Vendedor do Canal Sul |
| vendedor2 | vend123 | Vendedor | Vendedor do Canal Sul |

### Painel Admin Django
**http://localhost:8000/admin/**
- Usuário: admin
- Senha: admin123

### API Docs (Swagger)
**http://localhost:8000/api/docs/**

---

## Checklist de Instalação

- [ ] WAMP instalado e rodando (MySQL ativo)
- [ ] Python 3.11+ instalado
- [ ] Node.js 18+ instalado
- [ ] Banco de dados `crm_db` criado no MySQL
- [ ] mysqlclient instalado
- [ ] Migrations executadas
- [ ] Dados iniciais criados
- [ ] Servidor rodando em http://localhost:8000
- [ ] Admin acessível em http://localhost:8000/admin/

### Checklist Frontend ✓
- [ ] Node.js instalado
- [ ] Dependências instaladas (`npm install`)
- [ ] Servidor rodando em http://localhost:5173
- [ ] Página de login aparece

---

## 🐛 Problemas Comuns

### ❌ Erro: "mysqlclient não instalado" ou erro de compilação
```powershell
# Opção 1: Instalar via pip
pip install mysqlclient

# Opção 2: Se der erro, baixar wheel pré-compilado
# Acesse: https://www.lfd.uci.edu/~gohlke/pythonlibs/#mysqlclient
# Baixe o arquivo .whl compatível com sua versão do Python
# Ex: mysqlclient-2.2.0-cp312-cp312-win_amd64.whl
pip install caminho/para/arquivo.whl
```

### ❌ Erro: "MySQL não está rodando"
- Verificar se o WAMP está rodando (ícone verde)
- Clicar no ícone do WAMP > MySQL > Service > Start/Resume Service
- Verificar no phpMyAdmin se consegue acessar

### ❌ Erro: "Port 8000 already in use"
```powershell
# Matar processo na porta 8000
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### ❌ Erro: "CORS Error" no frontend
- Verificar se backend está rodando
- Confirmar `CORS_ALLOWED_ORIGINS` no `.env` do backend

### ❌ Erro: "Module not found" no Vue
```powershell
# Reinstalar dependências
rm -r node_modules
npm install
```

---

## 📋 Comandos Úteis

### Backend
```powershell
# Ativar ambiente virtual
.\venv\Scripts\activate

# Criar novo modelo
python manage.py makemigrations
python manage.py migrate

# Criar superuser
python manage.py createsuperuser

# Shell interativo
python manage.py shell

# Resetar banco de dados
python manage.py flush
```

### Frontend
```powershell
# Desenvolvimento
npm run dev

# Build produção
npm run build

# Preview build
npm run preview

# Limpar cache
npm cache clean --force
```

---

## 🎨 Primeira Configuração no Sistema

1. **Login como Admin** (admin / admin123)
2. **Acessar "Estágios do Funil"** - Verificar estágios criados
3. **Acessar "Canais"** - Verificar canais criados
4. **Acessar "Usuários"** - Verificar usuários criados
5. **Testar Kanban** - Navegar para visão Kanban
6. **Criar Lead de Teste**
7. **Converter Lead** em Conta/Contato/Oportunidade
8. **Arrastar Oportunidade** no Kanban

---

## 📞 Suporte

Se encontrar problemas:
1. Verificar logs do console (backend e frontend)
2. Consultar este guia
3. Revisar o README.md
4. Verificar especificação em projeto.md

---

## ✅ Sistema Pronto!

Se tudo funcionou:
- ✓ Backend API rodando
- ✓ Frontend Vue.js rodando
- ✓ Banco de dados configurado
- ✓ Dados iniciais criados
- ✓ Login funcional

**Pronto para começar a vender! 🚀**
