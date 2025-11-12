# Sistema CRM de Vendas

Sistema completo de CRM focado em gestão de funil de vendas com hierarquia de canais.

## 📋 Funcionalidades

### Principais
- **Quadro Kanban** para visualização do funil de vendas
- **Gestão de Leads** com conversão para Contas/Contatos/Oportunidades
- **Gestão de Contas** (empresas)
- **Gestão de Contatos** (pessoas)
- **Gestão de Oportunidades** (negócios)
- **Gestão de Atividades** (tarefas, ligações, reuniões, e-mails)

### Hierarquia de Acesso
1. **Administrador**: Acesso total + gerenciamento de usuários, canais e configurações
2. **Responsável de Canal**: Visualiza e gerencia dados de todos os vendedores do seu canal
3. **Vendedor**: Visualiza e gerencia apenas seus próprios dados

## 🛠 Stack Tecnológica

### Backend
- Python 3.11+
- Django 4.2
- Django REST Framework
- MySQL (WAMP)
- JWT Authentication

### Frontend
- Vue.js 3
- Vue Router
- Pinia (State Management)
- Tailwind CSS
- Vite

## 🚀 Instalação e Configuração

### Pré-requisitos
- Python 3.11+
- Node.js 18+
- WAMP (ou MySQL 8.0+)

### 1. Configurar Backend

```powershell
# Navegar para o diretório backend
cd backend

# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual (Windows)
.\venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt

# Copiar arquivo de configuração
copy .env.example .env

# Editar .env com suas configurações (DB_NAME, DB_USER, DB_PASSWORD, etc.)

# Criar banco de dados MySQL (WAMP)
# Acesse http://localhost/phpmyadmin/
# Crie o banco: crm_db
# Ou via console MySQL: CREATE DATABASE crm_db;

# Executar migrações
python manage.py makemigrations
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser

# Executar servidor
python manage.py runserver
```

O backend estará disponível em: `http://localhost:8000`

### 2. Configurar Frontend

```powershell
# Navegar para o diretório frontend
cd frontend

# Instalar dependências
npm install

# Copiar arquivo de configuração
copy .env.example .env

# Executar servidor de desenvolvimento
npm run dev
```

O frontend estará disponível em: `http://localhost:5173`

## 📊 Endpoints da API

Documentação interativa disponível em:
- Swagger UI: `http://localhost:8000/api/docs/`
- ReDoc: `http://localhost:8000/api/schema/`

### Principais Endpoints

#### Autenticação
- `POST /api/auth/login/` - Login (retorna JWT token)
- `POST /api/auth/refresh/` - Refresh token

#### Módulos
- `GET/POST /api/leads/` - Leads
- `POST /api/leads/{id}/converter/` - Converter lead
- `GET/POST /api/contas/` - Contas
- `GET /api/contas/{id}/contatos/` - Contatos da conta
- `GET /api/contas/{id}/oportunidades/` - Oportunidades da conta
- `GET/POST /api/contatos/` - Contatos
- `GET/POST /api/oportunidades/` - Oportunidades
- `GET /api/oportunidades/kanban/` - Visão Kanban
- `PATCH /api/oportunidades/{id}/mudar_estagio/` - Mover no Kanban
- `GET/POST /api/atividades/` - Atividades

#### Admin (apenas para perfil ADMIN)
- `GET/POST /api/canais/` - Canais
- `GET/POST /api/usuarios/` - Usuários
- `GET/POST /api/estagios-funil/` - Estágios do funil

## 🎯 Fluxo de Uso

### 1. Configuração Inicial (Admin)
1. Login como admin
2. Criar Canais de Vendas
3. Criar Usuários (Responsáveis e Vendedores) e associá-los aos Canais
4. Configurar Estágios do Funil

### 2. Operação Diária (Vendedor/Responsável)
1. Cadastrar Leads (prospectos iniciais)
2. Converter Leads em Contas + Contatos + Oportunidades
3. Gerenciar Oportunidades no Kanban (arrastar entre estágios)
4. Registrar Atividades (ligações, reuniões, tarefas)
5. Acompanhar evolução das vendas

## 🔐 Dados Iniciais para Teste

Após criar o superusuário, você pode criar:

### Canais de Exemplo
- Canal Sul
- Canal Norte
- Canal Leste

### Estágios do Funil Padrão
1. Prospecção (Aberto)
2. Qualificação (Aberto)
3. Proposta (Aberto)
4. Negociação (Aberto)
5. Fechado - Ganho (Ganho)
6. Fechado - Perdido (Perdido)

## 📁 Estrutura do Projeto

```
crm_wp/
├── backend/
│   ├── config/          # Configurações Django
│   ├── crm/            # App principal
│   │   ├── models.py   # Modelos de dados
│   │   ├── serializers.py
│   │   ├── views.py    # ViewSets da API
│   │   ├── permissions.py
│   │   └── urls.py
│   ├── manage.py
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── views/      # Páginas
│   │   ├── stores/     # Estado (Pinia)
│   │   ├── services/   # API client
│   │   ├── layouts/    # Layouts
│   │   ├── router/     # Vue Router
│   │   └── assets/     # CSS/Assets
│   ├── package.json
│   └── vite.config.js
│
└── projeto.md          # Especificação original
```

## 🔧 Desenvolvimento

### Backend
```powershell
# Criar novas migrações após alterar models
python manage.py makemigrations

# Aplicar migrações
python manage.py migrate

# Criar admin customizado
python manage.py createsuperuser

# Acessar shell Django
python manage.py shell
```

### Frontend
```powershell
# Modo desenvolvimento
npm run dev

# Build para produção
npm run build

# Preview do build
npm run preview
```

## 📝 Próximas Melhorias

- [ ] Modais de criação/edição completos
- [ ] Upload de arquivos/documentos
- [ ] Dashboard com gráficos e métricas
- [ ] Notificações em tempo real
- [ ] Export de relatórios (CSV, PDF)
- [ ] Integração com e-mail
- [ ] Histórico de alterações
- [ ] Filtros avançados
- [ ] Busca global

## 🐛 Troubleshooting

### Erro de conexão com banco de dados
- Verifique se o PostgreSQL está rodando
- Confirme as credenciais no arquivo `.env`
- Crie o banco de dados se não existir

### Erro CORS no frontend
- Verifique se o backend está rodando
- Confirme a configuração `CORS_ALLOWED_ORIGINS` no `settings.py`

### Erro de autenticação
- Verifique se o token JWT está sendo enviado no header
- Confirme se o token não expirou

## 📄 Licença

Este projeto é privado e proprietário.

## 👥 Contato

Para dúvidas ou suporte, entre em contato com a equipe de desenvolvimento.
