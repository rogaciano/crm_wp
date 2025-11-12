# 📐 Arquitetura do Sistema CRM - Diagramas Mermaid

## 📋 Índice
1. [Arquitetura Geral](#arquitetura-geral)
2. [Modelo de Dados (ER)](#modelo-de-dados)
3. [Fluxo de Autenticação](#fluxo-de-autenticação)
4. [Fluxo de Conversão de Lead](#fluxo-de-conversão-de-lead)
5. [Fluxo do Kanban](#fluxo-do-kanban)
6. [Hierarquia de Permissões](#hierarquia-de-permissões)
7. [Estrutura de Diretórios](#estrutura-de-diretórios)

---

## 1. Arquitetura Geral

```mermaid
graph TB
    subgraph "Frontend - Vue.js"
        A[Browser] --> B[Vue Router]
        B --> C[Views/Pages]
        C --> D[Pinia Stores]
        D --> E[API Service/Axios]
    end
    
    subgraph "Backend - Django"
        F[Django REST Framework] --> G[ViewSets]
        G --> H[Serializers]
        H --> I[Models]
        I --> J[(MySQL Database)]
        G --> K[Permissions]
        K --> L[Hierarchy Filter]
    end
    
    E -->|HTTP/REST API| F
    F -->|JWT Token| E
    
    subgraph "Autenticação"
        M[JWT Auth] --> N[Access Token]
        M --> O[Refresh Token]
    end
    
    F --> M
    
    style A fill:#e1f5ff
    style J fill:#ffe1e1
    style M fill:#fff4e1
```

---

## 2. Modelo de Dados (ER)

```mermaid
erDiagram
    CANAL ||--o{ USER : "possui vendedores"
    CANAL ||--o| USER : "tem responsável"
    
    USER ||--o{ LEAD : "proprietário"
    USER ||--o{ CONTA : "proprietário"
    USER ||--o{ CONTATO : "proprietário"
    USER ||--o{ OPORTUNIDADE : "proprietário"
    USER ||--o{ ATIVIDADE : "proprietário"
    
    LEAD ||--o| CONTA : "converte em"
    LEAD ||--o| CONTATO : "converte em"
    
    CONTA ||--o{ CONTATO : "possui"
    CONTA ||--o{ OPORTUNIDADE : "possui"
    
    OPORTUNIDADE }o--|| ESTAGIO_FUNIL : "está em"
    OPORTUNIDADE }o--o| CONTATO : "contato principal"
    
    ATIVIDADE }o--o| LEAD : "relacionada"
    ATIVIDADE }o--o| CONTA : "relacionada"
    ATIVIDADE }o--o| CONTATO : "relacionada"
    ATIVIDADE }o--o| OPORTUNIDADE : "relacionada"
    
    CANAL {
        int id PK
        string nome
        int responsavel_id FK
        datetime data_criacao
    }
    
    USER {
        int id PK
        string username
        string email
        string perfil
        int canal_id FK
        string first_name
        string last_name
        string telefone
    }
    
    LEAD {
        int id PK
        string nome
        string email
        string telefone
        string empresa
        string cargo
        string fonte
        string status
        text notas
        int proprietario_id FK
        datetime data_criacao
    }
    
    CONTA {
        int id PK
        string nome_empresa
        string cnpj
        string telefone_principal
        string email
        string website
        string setor
        text endereco
        int proprietario_id FK
        datetime data_criacao
    }
    
    CONTATO {
        int id PK
        string nome
        string email
        string telefone
        string celular
        string cargo
        string departamento
        int conta_id FK
        int proprietario_id FK
        datetime data_criacao
    }
    
    ESTAGIO_FUNIL {
        int id PK
        string nome
        int ordem
        string tipo
        string cor
    }
    
    OPORTUNIDADE {
        int id PK
        string nome
        decimal valor_estimado
        date data_fechamento_esperada
        int probabilidade
        int estagio_id FK
        int conta_id FK
        int contato_principal_id FK
        int proprietario_id FK
        datetime data_criacao
        datetime data_fechamento
    }
    
    ATIVIDADE {
        int id PK
        string tipo
        string titulo
        text descricao
        datetime data_vencimento
        string status
        int content_type_id FK
        int object_id
        int proprietario_id FK
        datetime data_criacao
    }
```

---

## 3. Fluxo de Autenticação

```mermaid
sequenceDiagram
    participant U as Usuário
    participant F as Frontend Vue
    participant A as API Django
    participant DB as MySQL
    
    U->>F: Acessa /login
    U->>F: Insere email e senha
    F->>A: POST /api/auth/login/
    A->>DB: Valida credenciais
    DB-->>A: Usuário válido
    A-->>F: JWT Token (access + refresh)
    F->>F: Armazena token no localStorage
    F->>F: Armazena dados do user na store
    F->>U: Redireciona para /kanban
    
    Note over F,A: Requisições subsequentes
    
    F->>A: GET /api/oportunidades/<br/>(Header: Authorization Bearer token)
    A->>A: Valida JWT
    A->>A: Aplica filtro de hierarquia
    A->>DB: Query com filtros
    DB-->>A: Dados filtrados
    A-->>F: JSON Response
    
    Note over F,A: Token expirado
    
    F->>A: GET /api/leads/ (token expirado)
    A-->>F: 401 Unauthorized
    F->>A: POST /api/auth/refresh/<br/>(refresh_token)
    A-->>F: Novo access_token
    F->>F: Atualiza token
    F->>A: Retry GET /api/leads/
    A-->>F: 200 OK + dados
```

---

## 4. Fluxo de Conversão de Lead

```mermaid
flowchart TD
    A[Usuário visualiza Lead] --> B{Lead já convertido?}
    B -->|Sim| C[Exibe mensagem: já convertido]
    B -->|Não| D[Clica em Converter Lead]
    
    D --> E[Frontend: POST /api/leads/:id/converter/]
    E --> F[Backend: Inicia transação]
    
    F --> G[Cria Conta]
    G --> H{Conta criada?}
    H -->|Erro| M[Rollback transação]
    H -->|Sucesso| I[Cria Contato vinculado à Conta]
    
    I --> J{Contato criado?}
    J -->|Erro| M
    J -->|Sucesso| K[Cria Oportunidade opcional]
    
    K --> L[Atualiza Lead: status = Convertido]
    L --> N[Commit transação]
    
    N --> O[Retorna IDs criados]
    O --> P[Frontend: Atualiza lista]
    P --> Q[Exibe mensagem de sucesso]
    
    M --> R[Retorna erro]
    R --> S[Frontend: Exibe erro]
    
    style G fill:#d4edda
    style I fill:#d4edda
    style K fill:#d4edda
    style L fill:#d4edda
    style M fill:#f8d7da
    style R fill:#f8d7da
```

---

## 5. Fluxo do Kanban (Drag and Drop)

```mermaid
sequenceDiagram
    participant U as Usuário
    participant K as KanbanView
    participant S as Store Pinia
    participant A as API
    participant DB as Database
    
    U->>K: Acessa /kanban
    K->>A: GET /api/oportunidades/kanban/
    A->>DB: SELECT oportunidades WHERE estagio.tipo = 'ABERTO'
    DB-->>A: Lista de oportunidades
    A-->>K: JSON agrupado por estágio
    K->>K: Renderiza colunas e cards
    
    Note over U,K: Drag and Drop
    
    U->>K: Arrasta card da coluna A
    K->>K: onDragStart(oportunidade)
    U->>K: Solta card na coluna B
    K->>K: onDrop(novo_estagio_id)
    
    K->>S: Atualiza estado local (otimista)
    K->>A: PATCH /api/oportunidades/:id/mudar_estagio/<br/>{estagio_id: novo_id}
    
    A->>A: Valida permissão
    A->>DB: UPDATE oportunidade SET estagio_id = novo_id
    DB-->>A: Sucesso
    A-->>K: 200 OK + oportunidade atualizada
    
    K->>S: Confirma atualização
    K->>U: Card permanece na nova coluna
    
    Note over K,A: Caso de erro
    
    A-->>K: 403 Forbidden ou 400 Bad Request
    K->>S: Reverte estado (rollback)
    K->>U: Card volta para coluna original
    K->>U: Exibe mensagem de erro
```

---

## 6. Hierarquia de Permissões

```mermaid
graph TD
    A[Requisição API] --> B{Usuário autenticado?}
    B -->|Não| C[401 Unauthorized]
    B -->|Sim| D{Qual perfil?}
    
    D -->|ADMIN| E[Acesso Total]
    E --> F[Retorna TODOS os dados]
    
    D -->|RESPONSAVEL| G[Filtro por Canal]
    G --> H[Busca vendedores do canal]
    H --> I[Filtra: proprietario_id IN vendedores]
    I --> J[Retorna dados do canal]
    
    D -->|VENDEDOR| K[Filtro Individual]
    K --> L[Filtra: proprietario_id = user.id]
    L --> M[Retorna apenas seus dados]
    
    style E fill:#d4edda
    style J fill:#fff3cd
    style M fill:#cfe2ff
    style C fill:#f8d7da
```

### Matriz de Permissões

```mermaid
graph LR
    subgraph "ADMIN"
        A1[Todos os Canais]
        A2[Todos os Vendedores]
        A3[Todos os Dados]
        A4[Configurações]
    end
    
    subgraph "RESPONSÁVEL"
        R1[Seu Canal]
        R2[Vendedores do Canal]
        R3[Dados do Canal]
    end
    
    subgraph "VENDEDOR"
        V1[Seus Dados]
    end
    
    A1 --> A2
    A2 --> A3
    A3 --> A4
    
    R1 --> R2
    R2 --> R3
    
    style A1 fill:#dc3545,color:#fff
    style A2 fill:#dc3545,color:#fff
    style A3 fill:#dc3545,color:#fff
    style A4 fill:#dc3545,color:#fff
    
    style R1 fill:#ffc107
    style R2 fill:#ffc107
    style R3 fill:#ffc107
    
    style V1 fill:#28a745,color:#fff
```

---

## 7. Estrutura de Diretórios

```mermaid
graph TD
    ROOT[crm_wp/] --> BACKEND[backend/]
    ROOT --> FRONTEND[frontend/]
    ROOT --> DOCS[Documentação]
    
    BACKEND --> CONFIG[config/]
    BACKEND --> CRM[crm/]
    BACKEND --> MANAGE[manage.py]
    BACKEND --> REQ[requirements.txt]
    
    CONFIG --> SETTINGS[settings.py]
    CONFIG --> URLS_B[urls.py]
    CONFIG --> WSGI[wsgi.py]
    
    CRM --> MODELS[models.py]
    CRM --> VIEWS[views.py]
    CRM --> SERIALIZERS[serializers.py]
    CRM --> PERMISSIONS[permissions.py]
    CRM --> URLS_C[urls.py]
    CRM --> ADMIN[admin.py]
    
    FRONTEND --> SRC[src/]
    FRONTEND --> PUBLIC[public/]
    FRONTEND --> PACKAGE[package.json]
    FRONTEND --> VITE[vite.config.js]
    
    SRC --> VIEWS_F[views/]
    SRC --> STORES[stores/]
    SRC --> SERVICES[services/]
    SRC --> ROUTER[router/]
    SRC --> LAYOUTS[layouts/]
    SRC --> COMPONENTS[components/]
    SRC --> ASSETS[assets/]
    
    VIEWS_F --> LOGIN[LoginView.vue]
    VIEWS_F --> KANBAN[KanbanView.vue]
    VIEWS_F --> LEADS[LeadsView.vue]
    VIEWS_F --> CONTAS[ContasView.vue]
    VIEWS_F --> ADMIN_V[admin/]
    
    STORES --> AUTH[auth.js]
    STORES --> OPORT[oportunidades.js]
    
    SERVICES --> API[api.js]
    
    DOCS --> README[README.md]
    DOCS --> PROJETO[projeto.md]
    DOCS --> FEATURES[FEATURES.md]
    DOCS --> SETUP[SETUP_GUIDE.md]
    
    style ROOT fill:#e1f5ff
    style BACKEND fill:#ffe1e1
    style FRONTEND fill:#e1ffe1
    style DOCS fill:#fff4e1
```

---

## 8. Fluxo Completo: Jornada do Vendedor

```mermaid
journey
    title Jornada Diária do Vendedor no CRM
    section Manhã
      Login no sistema: 5: Vendedor
      Visualiza Kanban: 5: Vendedor
      Verifica atividades pendentes: 4: Vendedor
    section Prospecção
      Cadastra novos Leads: 5: Vendedor
      Contata Leads via telefone: 4: Vendedor
      Registra atividade de ligação: 5: Vendedor
    section Qualificação
      Qualifica Lead: 4: Vendedor
      Converte Lead em Oportunidade: 5: Vendedor
      Cria Conta e Contato: 5: Vendedor
    section Negociação
      Move oportunidade no Kanban: 5: Vendedor
      Agenda reunião: 4: Vendedor
      Atualiza valor da oportunidade: 4: Vendedor
    section Fechamento
      Move para "Fechado - Ganho": 5: Vendedor
      Registra observações: 4: Vendedor
      Comemora a venda: 5: Vendedor
```

---

## 9. Ciclo de Vida de uma Oportunidade

```mermaid
stateDiagram-v2
    [*] --> Lead: Cadastro inicial
    
    Lead --> Qualificado: Contato realizado
    Lead --> Descartado: Não qualificado
    
    Qualificado --> Convertido: Conversão
    
    Convertido --> Conta: Cria empresa
    Convertido --> Contato: Cria pessoa
    Convertido --> Oportunidade: Cria negócio
    
    Oportunidade --> Prospecção: Estágio inicial
    Prospecção --> Qualificação: Interesse confirmado
    Qualificação --> Proposta: Necessidade identificada
    Proposta --> Negociação: Proposta enviada
    Negociação --> FechadoGanho: Cliente aceita
    Negociação --> FechadoPerdido: Cliente recusa
    
    FechadoGanho --> [*]: Venda concluída
    FechadoPerdido --> [*]: Oportunidade perdida
    Descartado --> [*]: Lead descartado
    
    note right of Oportunidade
        Visível no Kanban
        enquanto estágio = ABERTO
    end note
    
    note right of FechadoGanho
        Sai do Kanban
        Registra data de fechamento
    end note
```

---

## 10. Arquitetura de Componentes Vue

```mermaid
graph TD
    APP[App.vue] --> ROUTER[Router]
    
    ROUTER --> AUTH_LAYOUT[AuthLayout]
    ROUTER --> MAIN_LAYOUT[MainLayout]
    
    AUTH_LAYOUT --> LOGIN[LoginView]
    
    MAIN_LAYOUT --> SIDEBAR[Sidebar]
    MAIN_LAYOUT --> CONTENT[RouterView]
    
    CONTENT --> KANBAN[KanbanView]
    CONTENT --> LEADS[LeadsView]
    CONTENT --> CONTAS[ContasView]
    CONTENT --> CONTA_DETAIL[ContaDetailView]
    CONTENT --> CONTATOS[ContatosView]
    CONTENT --> OPORTUNIDADES[OportunidadesView]
    CONTENT --> ATIVIDADES[AtividadesView]
    CONTENT --> ADMIN_USERS[AdminUsersView]
    CONTENT --> ADMIN_CANAIS[AdminCanaisView]
    CONTENT --> ADMIN_ESTAGIOS[AdminEstagiosView]
    
    KANBAN --> KANBAN_COLUMN[KanbanColumn Component]
    KANBAN --> KANBAN_CARD[KanbanCard Component]
    
    LEADS --> LEAD_TABLE[LeadTable Component]
    CONTAS --> CONTA_CARD[ContaCard Component]
    
    subgraph "Stores Pinia"
        AUTH_STORE[authStore]
        OPORT_STORE[oportunidadesStore]
    end
    
    subgraph "Services"
        API_SERVICE[api.js - Axios]
    end
    
    KANBAN -.->|usa| OPORT_STORE
    LOGIN -.->|usa| AUTH_STORE
    API_SERVICE -.->|interceptors| AUTH_STORE
    
    style APP fill:#42b983
    style MAIN_LAYOUT fill:#35495e,color:#fff
    style AUTH_STORE fill:#ffd700
    style API_SERVICE fill:#ff6b6b
```

---

## 11. Pipeline de Requisição API

```mermaid
flowchart LR
    A[Vue Component] --> B[Axios Request]
    B --> C{Token existe?}
    C -->|Não| D[Redireciona /login]
    C -->|Sim| E[Adiciona Header Authorization]
    E --> F[Envia para Backend]
    
    F --> G[Django Middleware]
    G --> H[JWT Authentication]
    H --> I{Token válido?}
    I -->|Não| J[401 Unauthorized]
    I -->|Sim| K[Identifica User]
    
    K --> L[ViewSet]
    L --> M[HierarchyPermission]
    M --> N{Tem permissão?}
    N -->|Não| O[403 Forbidden]
    N -->|Sim| P[Aplica filtros]
    
    P --> Q[QuerySet filtrado]
    Q --> R[Serializer]
    R --> S[JSON Response]
    S --> T[Axios Interceptor]
    
    T --> U{Status 401?}
    U -->|Sim| V[Refresh Token]
    V --> W{Refresh OK?}
    W -->|Sim| B
    W -->|Não| D
    
    U -->|Não| X[Retorna dados]
    X --> Y[Atualiza Component]
    
    J --> D
    O --> Z[Exibe erro]
    
    style D fill:#f8d7da
    style J fill:#f8d7da
    style O fill:#f8d7da
    style Z fill:#f8d7da
    style Y fill:#d4edda
```

---

## 12. Modelo de Segurança

```mermaid
graph TB
    subgraph "Camada Frontend"
        A[Vue Router Guard] --> B{User autenticado?}
        B -->|Não| C[Redireciona /login]
        B -->|Sim| D{Rota admin?}
        D -->|Sim| E{User é admin?}
        E -->|Não| F[Redireciona /kanban]
        E -->|Sim| G[Permite acesso]
        D -->|Não| G
    end
    
    subgraph "Camada Backend"
        H[Request] --> I[JWT Middleware]
        I --> J{Token válido?}
        J -->|Não| K[401 Response]
        J -->|Sim| L[DRF Permission]
        L --> M{IsAuthenticated?}
        M -->|Não| N[403 Response]
        M -->|Sim| O[HierarchyPermission]
        O --> P{Tem acesso?}
        P -->|Não| Q[403 Response]
        P -->|Sim| R[Aplica filtros]
        R --> S[Response com dados filtrados]
    end
    
    G --> H
    
    style C fill:#f8d7da
    style F fill:#fff3cd
    style K fill:#f8d7da
    style N fill:#f8d7da
    style Q fill:#f8d7da
    style S fill:#d4edda
```

---

## 📊 Resumo da Arquitetura

### Stack Tecnológica
- **Frontend**: Vue.js 3 + Vite + Pinia + Vue Router + Tailwind CSS
- **Backend**: Django 4.2 + Django REST Framework + JWT
- **Database**: MySQL 8.0
- **Autenticação**: JWT (Access + Refresh Token)

### Principais Padrões
- **Arquitetura**: REST API + SPA
- **State Management**: Pinia (Vuex successor)
- **Permissions**: Custom HierarchyPermission
- **Relacionamentos**: GenericForeignKey para atividades polimórficas
- **Drag and Drop**: HTML5 Drag and Drop API

### Módulos Principais
1. **Autenticação** (JWT)
2. **Leads** (Prospecção)
3. **Contas** (Empresas)
4. **Contatos** (Pessoas)
5. **Oportunidades** (Negócios)
6. **Atividades** (Tarefas/Ligações/Reuniões)
7. **Kanban** (Funil Visual)
8. **Admin** (Usuários/Canais/Estágios)

---

**Documentação gerada automaticamente para o Sistema CRM de Vendas** 🚀
