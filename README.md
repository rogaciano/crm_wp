# 🚀 Sistema CRM de Vendas

> Sistema completo de CRM focado em gestão de funil de vendas com hierarquia de canais, desenvolvido com Django REST Framework e Vue.js 3.

[![Status](https://img.shields.io/badge/status-pronto-brightgreen)]()
[![Django](https://img.shields.io/badge/Django-4.2-green)]()
[![Vue.js](https://img.shields.io/badge/Vue.js-3.3-blue)]()
[![MySQL](https://img.shields.io/badge/MySQL-8.0-orange)]()

---

## 📋 Funcionalidades Principais

### 🎯 Core Features
- ✅ **Quadro Kanban Drag & Drop** - Visualização e gestão do funil de vendas
- ✅ **Conversão de Leads** - Transforme leads em Contas + Contatos + Oportunidades automaticamente
- ✅ **Gestão de Contas** - Cadastro completo de empresas com detalhes e relacionamentos
- ✅ **Gestão de Contatos** - Pessoas vinculadas às contas
- ✅ **Gestão de Oportunidades** - Negócios com valores, probabilidades e estágios
- ✅ **Gestão de Atividades** - Tarefas, ligações, reuniões, e-mails e notas
- ✅ **Sistema de Canais** - Organização por canais de vendas regionais
- ✅ **Hierarquia de Permissões** - 3 níveis de acesso (Admin, Responsável, Vendedor)

### 🔐 Hierarquia de Acesso
| Perfil | Permissões |
|--------|-----------|
| **Administrador** | Acesso total + gestão de usuários, canais e configurações do sistema |
| **Responsável de Canal** | Visualiza e gerencia dados de todos os vendedores do seu canal |
| **Vendedor** | Visualiza e gerencia apenas seus próprios dados (leads, oportunidades, etc.) |

## 🛠 Stack Tecnológica

### Backend
- **Python** 3.11+
- **Django** 4.2.7
- **Django REST Framework** 3.14.0
- **MySQL** 8.0+ (via WAMP)
- **PyMySQL** 1.1.0 (driver Python puro)
- **JWT Authentication** (djangorestframework-simplejwt)
- **DRF Spectacular** (documentação Swagger/OpenAPI)
- **Django CORS Headers** (integração frontend/backend)

### Frontend
- **Vue.js** 3.3.8 (Composition API)
- **Vue Router** 4.2.5
- **Pinia** 2.1.7 (State Management)
- **Tailwind CSS** 3.3.5
- **Vite** 5.0.2
- **Axios** 1.6.2 (HTTP client)
- **Vue Draggable Next** (Kanban drag & drop)

## 🚀 Instalação e Configuração

### Pré-requisitos
- Python 3.11+
- Node.js 18+
- WAMP (ou MySQL 8.0+)

### 1. Configurar Backend

```powershell
# Navegar para o diretório backend
cd c:\projetos\crm_wp\backend

# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual (Windows)
.\venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt

# Criar arquivo .env (copie e edite)
copy .env.example .env
# Edite o .env com suas configurações do MySQL

# Criar banco de dados MySQL
# Opção 1: Via phpMyAdmin (http://localhost/phpmyadmin/)
#   - Crie o banco: crm_db
# Opção 2: Via console MySQL:
#   CREATE DATABASE crm_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# Executar migrações
python manage.py migrate

# Criar dados iniciais (canais, estágios, usuários de teste)
python manage.py shell
# Execute o script de dados iniciais ou crie manualmente

# Criar superusuário
python manage.py createsuperuser

# Executar servidor
python manage.py runserver
```

✅ **Backend disponível em:** `http://localhost:8000`

#### Configuração do arquivo `.env`
```env
DEBUG=True
SECRET_KEY=your-secret-key-here-change-in-production
ALLOWED_HOSTS=localhost,127.0.0.1

# Database MySQL (WAMP)
DB_NAME=crm_db
DB_USER=root
DB_PASSWORD=
DB_HOST=localhost
DB_PORT=3306

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://localhost:8080
```

### 2. Configurar Frontend

```powershell
# Navegar para o diretório frontend
cd c:\projetos\crm_wp\frontend

# Instalar dependências
npm install

# Criar arquivo .env (se necessário)
copy .env.example .env

# Executar servidor de desenvolvimento
npm run dev
```

✅ **Frontend disponível em:** `http://localhost:5173`

#### Scripts disponíveis
```powershell
npm run dev      # Servidor de desenvolvimento
npm run build    # Build para produção
npm run preview  # Preview do build de produção
```

## 📊 API REST

### 📖 Documentação Interativa
- **Swagger UI:** `http://localhost:8000/api/docs/`
- **ReDoc:** `http://localhost:8000/api/schema/redoc/`
- **Django Admin:** `http://localhost:8000/admin/`

### 🔑 Autenticação
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/api/auth/login/` | Login (retorna access + refresh token JWT) |
| POST | `/api/auth/refresh/` | Renovar access token |

### 📋 Endpoints Principais

#### Leads
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/api/leads/` | Listar leads (com filtros e busca) |
| POST | `/api/leads/` | Criar novo lead |
| GET | `/api/leads/{id}/` | Detalhes do lead |
| PUT/PATCH | `/api/leads/{id}/` | Atualizar lead |
| DELETE | `/api/leads/{id}/` | Deletar lead |
| POST | `/api/leads/{id}/converter/` | **Converter lead** em Conta + Contato + Oportunidade |

#### Contas (Empresas)
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/api/contas/` | Listar contas |
| POST | `/api/contas/` | Criar conta |
| GET | `/api/contas/{id}/` | Detalhes da conta |
| GET | `/api/contas/{id}/contatos/` | Contatos vinculados |
| GET | `/api/contas/{id}/oportunidades/` | Oportunidades vinculadas |

#### Contatos (Pessoas)
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/api/contatos/` | Listar contatos |
| POST | `/api/contatos/` | Criar contato (requer conta_id) |

#### Oportunidades (Negócios)
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/api/oportunidades/` | Listar oportunidades |
| POST | `/api/oportunidades/` | Criar oportunidade |
| GET | `/api/oportunidades/kanban/` | **Visão Kanban** (agrupado por estágio) |
| PATCH | `/api/oportunidades/{id}/mudar_estagio/` | **Mover card** no Kanban |

#### Atividades
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/api/atividades/` | Listar atividades |
| POST | `/api/atividades/` | Criar atividade (tarefa, ligação, reunião, etc.) |

#### Admin (apenas ADMIN)
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET/POST | `/api/canais/` | Gestão de canais |
| GET/POST | `/api/usuarios/` | Gestão de usuários |
| GET/POST | `/api/estagios-funil/` | Configuração dos estágios do funil |

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

## 🔐 Dados de Teste

### Usuários Criados (se usar script de dados iniciais)
| Usuário | Senha | Perfil | Canal |
|---------|-------|--------|-------|
| admin | admin123 | Administrador | - |
| resp_sul | resp123 | Responsável | Canal Sul |
| vendedor1 | vend123 | Vendedor | Canal Sul |
| vendedor2 | vend123 | Vendedor | Canal Sul |

### Canais de Exemplo
- **Canal Sul**
- **Canal Norte**
- **Canal Leste**
- **Canal Oeste**

### Estágios do Funil Padrão
| Ordem | Nome | Tipo | Cor |
|-------|------|------|-----|
| 1 | Prospecção | Aberto | blue |
| 2 | Qualificação | Aberto | yellow |
| 3 | Proposta | Aberto | purple |
| 4 | Negociação | Aberto | orange |
| 5 | Fechado - Ganho | Ganho | green |
| 6 | Fechado - Perdido | Perdido | red |

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
