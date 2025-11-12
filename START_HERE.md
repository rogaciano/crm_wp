# 🎉 Sistema CRM de Vendas - PROJETO COMPLETO

## ✅ O que foi implementado?

Um **Sistema CRM completo e funcional** baseado na especificação do arquivo `projeto.md`, incluindo:

### Backend (Django + DRF)
- ✅ 7 models principais (User, Canal, Lead, Conta, Contato, Oportunidade, Atividade)
- ✅ API REST completa com JWT authentication
- ✅ Hierarquia de permissões (Admin → Responsável → Vendedor)
- ✅ Endpoints para todos os módulos
- ✅ Conversão de Lead com transação atômica
- ✅ Documentação Swagger automática

### Frontend (Vue.js 3 + Tailwind CSS)
- ✅ 11 páginas completas (Login, Kanban, Leads, Contas, etc.)
- ✅ Visão Kanban com drag-and-drop
- ✅ Navegação com sidebar e menu lateral
- ✅ State management com Pinia
- ✅ Design moderno e responsivo

### Funcionalidades Principais
- ✅ **Kanban Visual**: Arraste oportunidades entre estágios do funil
- ✅ **Conversão de Leads**: Lead → Conta + Contato + Oportunidade
- ✅ **Hierarquia de Canais**: Controle de visibilidade por perfil
- ✅ **CRUD Completo**: Todos os módulos com Create, Read, Update, Delete
- ✅ **Timeline de Atividades**: Registro de interações

---

## 🚀 Como começar?

### Passo 1: Ler a documentação
1. **`MYSQL_SETUP.md`** ← LEIA ISTO! Configuração MySQL/WAMP
2. **`SETUP_GUIDE.md`** - Guia de instalação passo a passo
3. **`README.md`** - Documentação completa do projeto
4. **`FEATURES.md`** - Lista detalhada de funcionalidades

### Passo 2: Instalar dependências
```powershell
# Backend
cd backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt

# Frontend (novo terminal)
cd frontend
npm install
```

### Passo 3: Configurar banco de dados MySQL (WAMP)
```sql
-- Via phpMyAdmin (http://localhost/phpmyadmin/)
-- Ou console MySQL:
CREATE DATABASE crm_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

**📘 Leia:** `MYSQL_SETUP.md` para detalhes completos sobre MySQL

### Passo 4: Configurar arquivos .env
```powershell
# Backend
cd backend
copy .env.example .env
# Editar .env com suas credenciais do MySQL (WAMP)

# Frontend
cd frontend
copy .env.example .env
```

### Passo 5: Executar migrações e criar dados iniciais
```powershell
cd backend
python manage.py migrate
python manage.py shell < setup_database.py
```

### Passo 6: Iniciar os servidores
```powershell
# Terminal 1 - Backend
cd backend
python manage.py runserver

# Terminal 2 - Frontend
cd frontend
npm run dev
```

### Passo 7: Acessar o sistema
- **Frontend**: http://localhost:5173
- **Login**: admin / admin123
- **API Docs**: http://localhost:8000/api/docs/

---

## 📁 Estrutura de Arquivos

```
c:\projetos\crm_wp\
│
├── 📄 START_HERE.md          ← Você está aqui!
├── 📄 SETUP_GUIDE.md         ← Guia de instalação detalhado
├── 📄 README.md              ← Documentação completa
├── 📄 FEATURES.md            ← Lista de funcionalidades
├── 📄 projeto.md             ← Especificação original
├── 📄 .gitignore
│
├── 📁 backend/               ← Django Backend
│   ├── config/              # Configurações Django
│   │   ├── settings.py      # Configurações principais
│   │   ├── urls.py          # URLs da API
│   │   └── ...
│   │
│   ├── crm/                 # App principal
│   │   ├── models.py        # Modelos de dados
│   │   ├── serializers.py   # Serializers da API
│   │   ├── views.py         # ViewSets (endpoints)
│   │   ├── permissions.py   # Permissões customizadas
│   │   ├── admin.py         # Django Admin
│   │   └── urls.py          # Rotas da API
│   │
│   ├── manage.py
│   ├── requirements.txt     # Dependências Python
│   ├── setup_database.py    # Script de dados iniciais
│   ├── .env.example
│   └── .env                 # (criar este arquivo)
│
└── 📁 frontend/             ← Vue.js Frontend
    ├── src/
    │   ├── views/           # Páginas
    │   │   ├── LoginView.vue
    │   │   ├── KanbanView.vue
    │   │   ├── LeadsView.vue
    │   │   ├── ContasView.vue
    │   │   ├── ContaDetailView.vue
    │   │   ├── ContatosView.vue
    │   │   ├── OportunidadesView.vue
    │   │   ├── AtividadesView.vue
    │   │   └── admin/       # Views admin
    │   │
    │   ├── stores/          # State (Pinia)
    │   │   ├── auth.js
    │   │   └── oportunidades.js
    │   │
    │   ├── services/
    │   │   └── api.js       # Cliente Axios
    │   │
    │   ├── layouts/
    │   │   └── MainLayout.vue
    │   │
    │   ├── router/
    │   │   └── index.js     # Vue Router
    │   │
    │   ├── assets/
    │   │   └── main.css     # Tailwind CSS
    │   │
    │   ├── App.vue
    │   └── main.js
    │
    ├── package.json
    ├── vite.config.js
    ├── tailwind.config.js
    ├── .env.example
    └── .env                 # (criar este arquivo)
```

---

## 🎯 Usuários Criados Automaticamente

Após executar `setup_database.py`:

| Usuário | Senha | Perfil | Descrição |
|---------|-------|--------|-----------|
| **admin** | admin123 | Administrador | Acesso total ao sistema |
| **resp_sul** | resp123 | Responsável | Gerencia Canal Sul |
| **vendedor1** | vend123 | Vendedor | Vendedor do Canal Sul |
| **vendedor2** | vend123 | Vendedor | Vendedor do Canal Sul |

---

## 🧪 Como testar o sistema?

### Fluxo Completo de Teste

1. **Login como admin** (admin / admin123)
2. **Verificar estágios do funil** → Admin > Estágios do Funil
3. **Criar um Lead** → Menu Leads > + Novo Lead
4. **Converter o Lead** → Botão "Converter" na listagem
5. **Ver oportunidade no Kanban** → Menu Kanban
6. **Arrastar oportunidade** entre estágios (drag & drop)
7. **Ver detalhes da conta** → Menu Contas > Clicar em uma conta
8. **Criar atividade** → Menu Atividades > + Nova Atividade

### Testar Hierarquia
1. **Login como vendedor1** (vendedor1 / vend123)
2. Verificar que vê apenas seus próprios dados
3. **Login como resp_sul** (resp_sul / resp123)
4. Verificar que vê dados de todos os vendedores do Canal Sul
5. **Login como admin** (admin / admin123)
6. Verificar acesso total a todos os dados

---

## 📊 Endpoints da API

### Autenticação
- `POST /api/auth/login/` - Login
- `POST /api/auth/refresh/` - Refresh token

### CRUD Principal
- `GET/POST /api/leads/` - Leads
- `POST /api/leads/{id}/converter/` - Converter lead
- `GET/POST /api/contas/` - Contas
- `GET/POST /api/contatos/` - Contatos
- `GET/POST /api/oportunidades/` - Oportunidades
- `GET /api/oportunidades/kanban/` - Visão Kanban
- `PATCH /api/oportunidades/{id}/mudar_estagio/` - Mover estágio
- `GET/POST /api/atividades/` - Atividades

### Admin
- `GET/POST /api/canais/` - Canais
- `GET/POST /api/usuarios/` - Usuários
- `GET/POST /api/estagios-funil/` - Estágios

**Documentação completa:** http://localhost:8000/api/docs/

---

## ⚡ Comandos Rápidos

### Backend
```powershell
# Ativar ambiente
cd backend
.\venv\Scripts\activate

# Rodar servidor
python manage.py runserver

# Criar migração
python manage.py makemigrations

# Aplicar migração
python manage.py migrate

# Shell interativo
python manage.py shell

# Criar superuser
python manage.py createsuperuser
```

### Frontend
```powershell
# Rodar dev server
cd frontend
npm run dev

# Build para produção
npm run build

# Instalar dependências
npm install
```

---

## 🐛 Problemas Comuns

### ❌ "No module named 'crm'"
```powershell
# Verificar se está no diretório correto
cd c:\projetos\crm_wp\backend
```

### ❌ "Port already in use"
```powershell
# Matar processo na porta 8000
netstat -ano | findstr :8000
taskkill /PID <número> /F
```

### ❌ Erro de conexão com PostgreSQL
- Verificar se PostgreSQL está rodando
- Confirmar credenciais no `.env`
- Verificar se o banco `crm_db` foi criado

### ❌ Erro CORS no frontend
- Verificar se backend está rodando
- Confirmar `CORS_ALLOWED_ORIGINS` no settings.py

---

## 📚 Documentos Importantes

| Arquivo | Descrição |
|---------|-----------|
| **MYSQL_SETUP.md** | 🔧 Configuração MySQL/WAMP (LEIA PRIMEIRO!) |
| **SETUP_GUIDE.md** | 🚀 Guia de instalação passo a passo (15 min) |
| **README.md** | 📖 Documentação completa do projeto |
| **FEATURES.md** | ✨ Lista detalhada de funcionalidades |
| **projeto.md** | 📋 Especificação original do sistema |

---

## ✅ Checklist de Instalação

- [ ] WAMP instalado e rodando (MySQL ativo)
- [ ] Python 3.11+ instalado
- [ ] Node.js 18+ instalado
- [ ] Banco de dados `crm_db` criado no MySQL
- [ ] Backend: ambiente virtual criado
- [ ] Backend: dependências instaladas
- [ ] Backend: arquivo .env configurado
- [ ] Backend: migrações executadas
- [ ] Backend: dados iniciais criados
- [ ] Backend: servidor rodando (porta 8000)
- [ ] Frontend: dependências instaladas
- [ ] Frontend: arquivo .env criado
- [ ] Frontend: servidor rodando (porta 5173)
- [ ] Login funcional em http://localhost:5173

---

## 🎉 Pronto para usar!

Se todas as etapas foram concluídas, você tem um **CRM completo e funcional** com:

- ✅ Backend Django robusto
- ✅ Frontend Vue.js moderno
- ✅ Kanban visual drag-and-drop
- ✅ Hierarquia de permissões
- ✅ Conversão de leads
- ✅ API REST documentada

**Próximos passos:**
1. Explore o sistema com os usuários de teste
2. Configure seus próprios canais e usuários
3. Customize conforme necessário
4. Implemente melhorias adicionais

---

## 📞 Precisa de Ajuda?

1. **Leia primeiro:** SETUP_GUIDE.md
2. **Consulte:** README.md
3. **Verifique:** FEATURES.md
4. **Revise:** projeto.md

**Boa sorte com seu CRM! 🚀**
