# 🔧 Configuração MySQL para CRM

## ✅ Alterações Realizadas

O projeto foi adaptado de PostgreSQL para **MySQL/WAMP**:

- ✅ `requirements.txt` → Agora usa `mysqlclient` em vez de `psycopg2`
- ✅ `settings.py` → Configurado para `django.db.backends.mysql`
- ✅ `.env` → Atualizado com configurações MySQL (root, porta 3306)
- ✅ Documentação atualizada

## 🚀 Próximos Passos

### 1. Instalar pymysql (driver MySQL)

```powershell
# No terminal com venv ativado:
pip install -r requirements.txt
```

**✅ Usamos PyMySQL** em vez de mysqlclient porque:
- Não precisa compilação no Windows
- Puro Python (sem dependências C)
- Totalmente compatível com Django
- Mais fácil de instalar

### 2. Criar banco de dados no WAMP

**Opção 1 - phpMyAdmin:**
1. Abrir `http://localhost/phpmyadmin/`
2. Clicar em **"Novo"** (aba lateral esquerda)
3. Nome: `crm_db`
4. Collation: `utf8mb4_unicode_ci`
5. Clicar em **"Criar"**

**Opção 2 - Console MySQL:**
```sql
CREATE DATABASE crm_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 3. Verificar configurações no .env

Seu arquivo `.env` já foi atualizado com:

```env
# Database MySQL (WAMP)
DB_NAME=crm_db
DB_USER=root
DB_PASSWORD=
DB_HOST=localhost
DB_PORT=3306
```

**⚠️ IMPORTANTE:**
- Se seu MySQL tem senha, coloque-a em `DB_PASSWORD`
- A configuração padrão do WAMP geralmente não tem senha (campo vazio)

### 4. Executar Migrações

```powershell
# Com venv ativado e banco criado:
python manage.py makemigrations
python manage.py migrate
```

### 5. Criar Dados Iniciais

```powershell
python manage.py shell < setup_database.py
```

Isso criará:
- ✅ 4 Canais de vendas
- ✅ 6 Estágios do funil
- ✅ 4 Usuários de teste (admin, resp_sul, vendedor1, vendedor2)

### 6. Iniciar Servidor

```powershell
python manage.py runserver
```

Acesse: **http://localhost:8000/admin/**
- Usuário: `admin`
- Senha: `admin123`

## 🔍 Verificar Instalação

### Checklist:
- [x] WAMP rodando (ícone verde)
- [x] MySQL ativo no WAMP
- [x] pymysql instalado (`pip list | findstr pymysql`)
- [x] Banco `crm_db` criado (verificar no phpMyAdmin)
- [x] Arquivo `.env` configurado
- [x] Migrações executadas sem erro
- [x] Dados iniciais criados
- [x] Servidor Django rodando em http://127.0.0.1:8000/
- [ ] Admin acessível

## 🐛 Problemas Comuns

### ❌ Erro: "No module named 'MySQLdb'"
```powershell
pip install mysqlclient
```

### ❌ Erro: "Can't connect to MySQL server"
- Verificar se WAMP está verde (todos os serviços ativos)
- Clicar no ícone WAMP > MySQL > Service > Start/Resume Service
- Verificar porta 3306 não está bloqueada

### ❌ Erro: "Access denied for user 'root'@'localhost'"
- Verificar senha no arquivo `.env`
- Se o MySQL tem senha, adicionar em `DB_PASSWORD`
- Padrão WAMP: sem senha (deixar vazio)

### ❌ Erro ao compilar mysqlclient
Baixe o wheel pré-compilado:
1. Acesse: https://www.lfd.uci.edu/~gohlke/pythonlibs/#mysqlclient
2. Baixe o arquivo para sua versão do Python (ex: cp312 = Python 3.12)
3. Instale: `pip install arquivo.whl`

### ❌ Erro: "Unknown database 'crm_db'"
O banco não foi criado. Crie via phpMyAdmin ou console MySQL.

### ❌ WAMP não fica verde
- Verificar se Apache/MySQL não estão em conflito com outras aplicações
- Porta 80 (Apache) e 3306 (MySQL) devem estar livres
- Verificar logs do WAMP

## 📊 Configuração MySQL Recomendada

No arquivo `my.ini` do MySQL (WAMP), verifique:

```ini
[mysqld]
default-storage-engine=INNODB
character-set-server=utf8mb4
collation-server=utf8mb4_unicode_ci
max_connections=100
```

## ✅ Tudo Pronto!

Após seguir os passos acima:
1. Backend estará rodando em `http://localhost:8000`
2. Dados iniciais estarão no banco
3. Pode continuar com o frontend: `cd ..\frontend && npm run dev`

**Próximo arquivo para ler:** `START_HERE.md`
