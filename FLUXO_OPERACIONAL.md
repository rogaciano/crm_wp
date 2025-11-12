# 🔄 Fluxo Operacional do Sistema CRM

Este documento descreve os fluxos operacionais do dia a dia do sistema CRM, mostrando como cada perfil de usuário interage com o sistema.

---

## 1. Fluxo Completo de Vendas

```mermaid
flowchart TD
    START([Início: Novo Prospecto]) --> A[Cadastrar Lead]
    
    A --> B[Lead: Status Novo]
    B --> C{Primeiro Contato}
    
    C -->|Sucesso| D[Lead: Status Contatado]
    C -->|Sem resposta| E[Agendar nova tentativa]
    E --> C
    
    D --> F{Lead Qualificado?}
    F -->|Não| G[Lead: Status Descartado]
    F -->|Sim| H[Lead: Status Qualificado]
    
    H --> I[Converter Lead]
    I --> J[Cria Conta Empresa]
    I --> K[Cria Contato Pessoa]
    I --> L[Cria Oportunidade]
    
    L --> M[Oportunidade: Prospecção]
    M --> N[Registrar Atividades]
    
    N --> O{Interesse Confirmado?}
    O -->|Não| P[Oportunidade: Perdido]
    O -->|Sim| Q[Oportunidade: Qualificação]
    
    Q --> R[Identificar Necessidades]
    R --> S[Oportunidade: Proposta]
    
    S --> T[Elaborar Proposta]
    T --> U[Enviar Proposta]
    U --> V[Oportunidade: Negociação]
    
    V --> W{Cliente Decidiu?}
    W -->|Objeções| X[Tratar Objeções]
    X --> V
    W -->|Recusou| Y[Oportunidade: Perdido]
    W -->|Aceitou| Z[Oportunidade: Ganho]
    
    Z --> AA[Registrar Data Fechamento]
    AA --> AB([Fim: Venda Concluída])
    
    G --> AC([Fim: Lead Descartado])
    P --> AD([Fim: Oportunidade Perdida])
    Y --> AD
    
    style START fill:#e1f5ff
    style AB fill:#d4edda
    style AC fill:#f8d7da
    style AD fill:#f8d7da
    style Z fill:#28a745,color:#fff
```

---

## 2. Operações por Perfil de Usuário

### 2.1 Fluxo do Administrador

```mermaid
flowchart TD
    ADMIN[Administrador Login] --> CONFIG[Configuração Inicial]
    
    CONFIG --> C1[Criar Canais]
    CONFIG --> C2[Criar Usuários]
    CONFIG --> C3[Configurar Estágios]
    
    C1 --> C1A[Canal Sul]
    C1 --> C1B[Canal Norte]
    C1 --> C1C[Canal Leste]
    
    C2 --> C2A[Criar Responsáveis]
    C2 --> C2B[Criar Vendedores]
    C2A --> C2C[Associar ao Canal]
    C2B --> C2C
    
    C3 --> C3A[Prospecção]
    C3 --> C3B[Qualificação]
    C3 --> C3C[Proposta]
    C3 --> C3D[Negociação]
    
    CONFIG --> MONITOR[Monitoramento]
    MONITOR --> M1[Ver Todos os Canais]
    MONITOR --> M2[Ver Todos os Vendedores]
    MONITOR --> M3[Ver Todas as Oportunidades]
    
    style ADMIN fill:#dc3545,color:#fff
    style CONFIG fill:#ffc107
    style MONITOR fill:#17a2b8,color:#fff
```

### 2.2 Fluxo do Responsável de Canal

```mermaid
flowchart TD
    RESP[Responsável Login] --> DASH[Dashboard do Canal]
    
    DASH --> V1[Ver Vendedores do Canal]
    DASH --> V2[Ver Leads do Canal]
    DASH --> V3[Ver Oportunidades do Canal]
    
    V1 --> A1[Acompanhar Performance]
    V2 --> A2[Revisar Qualificação]
    V3 --> A3[Monitorar Funil]
    
    A1 --> R1[Identificar Gargalos]
    A2 --> R2[Orientar Vendedores]
    A3 --> R3[Ajustar Estratégias]
    
    R1 --> REPORT[Gerar Relatórios]
    R2 --> REPORT
    R3 --> REPORT
    
    style RESP fill:#ffc107
    style DASH fill:#17a2b8,color:#fff
```

### 2.3 Fluxo do Vendedor

```mermaid
flowchart TD
    VEND[Vendedor Login] --> KANBAN[Visualizar Kanban]
    
    KANBAN --> CHECK[Verificar Oportunidades]
    CHECK --> PRIOR[Priorizar Ações]
    
    PRIOR --> PROSP[Prospecção]
    PRIOR --> QUAL[Qualificação]
    PRIOR --> NEG[Negociação]
    
    PROSP --> P1[Cadastrar Leads]
    PROSP --> P2[Fazer Ligações]
    PROSP --> P3[Enviar E-mails]
    
    P1 --> P4[Registrar Atividade]
    P2 --> P4
    P3 --> P4
    
    QUAL --> Q1[Converter Lead]
    Q1 --> Q2[Criar Oportunidade]
    Q2 --> Q3[Agendar Reunião]
    
    NEG --> N1[Atualizar Kanban]
    NEG --> N2[Enviar Proposta]
    NEG --> N3[Negociar Valores]
    
    style VEND fill:#28a745,color:#fff
    style KANBAN fill:#17a2b8,color:#fff
```

---

## 3. Fluxo de Conversão de Lead

```mermaid
sequenceDiagram
    actor Vendedor
    participant Frontend
    participant API
    participant DB
    
    Vendedor->>Frontend: Clica em "Converter Lead"
    Frontend->>API: POST /api/leads/{id}/converter/
    
    API->>DB: BEGIN TRANSACTION
    
    API->>DB: INSERT Conta
    Note right of DB: Empresa XYZ
    DB-->>API: Conta ID: 101
    
    API->>DB: INSERT Contato
    Note right of DB: João Silva<br/>conta_id: 101
    DB-->>API: Contato ID: 201
    
    API->>DB: INSERT Oportunidade
    Note right of DB: conta_id: 101<br/>contato_id: 201<br/>estagio: Prospecção
    DB-->>API: Oportunidade ID: 301
    
    API->>DB: UPDATE Lead status = Convertido
    DB-->>API: OK
    
    API->>DB: COMMIT TRANSACTION
    
    API-->>Frontend: 200 OK + IDs criados
    Frontend-->>Vendedor: ✅ Lead convertido!
```

---

## 4. Fluxo do Kanban (Drag and Drop)

```mermaid
sequenceDiagram
    actor Usuário
    participant Kanban
    participant Store
    participant API
    participant DB
    
    Usuário->>Kanban: Acessa /kanban
    Kanban->>API: GET /api/oportunidades/kanban/
    API->>DB: SELECT oportunidades
    DB-->>API: Lista de oportunidades
    API-->>Kanban: JSON agrupado por estágio
    Kanban->>Kanban: Renderiza colunas e cards
    
    Note over Usuário,Kanban: Drag and Drop
    
    Usuário->>Kanban: Arrasta card
    Usuário->>Kanban: Solta em nova coluna
    
    Kanban->>Store: Atualiza estado (otimista)
    Kanban->>API: PATCH /oportunidades/{id}/mudar_estagio/
    
    API->>DB: UPDATE oportunidade
    DB-->>API: Sucesso
    API-->>Kanban: 200 OK
    
    Kanban->>Store: Confirma atualização
    Kanban->>Usuário: Card na nova coluna
```

---

## 5. Fluxo de Prospecção

```mermaid
flowchart TD
    START([Vendedor inicia prospecção]) --> A[Acessa módulo Leads]
    
    A --> B[Clica em Novo Lead]
    B --> C[Preenche Formulário]
    
    C --> D[Nome: João Silva]
    C --> E[Email: joao@empresa.com]
    C --> F[Telefone: 11 99999-9999]
    C --> G[Empresa: Empresa XYZ]
    
    D --> H[Salvar Lead]
    E --> H
    F --> H
    G --> H
    
    H --> I[Lead criado: Status Novo]
    I --> J[Registrar Atividade: Ligação]
    
    J --> K{Conseguiu contato?}
    K -->|Não| L[Agendar nova tentativa]
    K -->|Sim| M[Atualizar: Contatado]
    
    M --> N{Demonstrou interesse?}
    N -->|Não| O[Atualizar: Descartado]
    N -->|Sim| P[Atualizar: Qualificado]
    
    P --> Q[Próximo: Converter Lead]
    
    style START fill:#e1f5ff
    style I fill:#fff3cd
    style M fill:#d1ecf1
    style P fill:#d4edda
    style O fill:#f8d7da
```

---

## 6. Fluxo de Fechamento

```mermaid
flowchart TD
    START([Oportunidade em Negociação]) --> A{Cliente decidiu?}
    
    A -->|Ainda negociando| B[Continuar follow-up]
    A -->|Decidiu| C{Qual decisão?}
    
    B --> B1[Registrar atividade]
    B1 --> B2[Agendar próximo contato]
    B2 --> WAIT[Aguardar resposta]
    WAIT --> A
    
    C -->|Aceitou| GANHO[Mover para Fechado - Ganho]
    C -->|Recusou| PERDIDO[Mover para Fechado - Perdido]
    
    GANHO --> G1[Arrastar card no Kanban]
    G1 --> G2[Sistema registra data_fechamento]
    G2 --> G3[Atualizar valor final]
    G3 --> G4[Card sai do Kanban]
    G4 --> G5[Oportunidade arquivada como Ganho]
    
    PERDIDO --> P1[Arrastar card no Kanban]
    P1 --> P2[Sistema registra data_fechamento]
    P2 --> P3[Selecionar motivo da perda]
    P3 --> P4[Card sai do Kanban]
    P4 --> P5[Oportunidade arquivada como Perdido]
    
    G5 --> END([Ciclo completo])
    P5 --> END
    
    style GANHO fill:#28a745,color:#fff
    style PERDIDO fill:#dc3545,color:#fff
    style G5 fill:#d4edda
    style P5 fill:#f8d7da
```

---

## 7. Fluxo de Atividades

```mermaid
flowchart LR
    START([Registrar Atividade]) --> TYPE{Tipo}
    
    TYPE -->|Tarefa| TASK[Criar Tarefa]
    TYPE -->|Ligação| CALL[Registrar Ligação]
    TYPE -->|Reunião| MEET[Agendar Reunião]
    TYPE -->|E-mail| EMAIL[Registrar E-mail]
    
    TASK --> T1[Definir título]
    T1 --> T2[Definir data vencimento]
    T2 --> T3[Associar a entidade]
    T3 --> SAVE[Salvar]
    
    CALL --> C1[Registrar data/hora]
    C1 --> C2[Resultado da ligação]
    C2 --> C3[Adicionar notas]
    C3 --> SAVE
    
    MEET --> M1[Definir data/hora]
    M1 --> M2[Definir local]
    M2 --> M3[Adicionar agenda]
    M3 --> SAVE
    
    EMAIL --> E1[Registrar assunto]
    E1 --> E2[Adicionar conteúdo]
    E2 --> SAVE
    
    SAVE --> TIMELINE[Adicionar à Timeline]
    TIMELINE --> END([Atividade registrada])
    
    style START fill:#e1f5ff
    style TIMELINE fill:#17a2b8,color:#fff
    style END fill:#28a745,color:#fff
```

---

## 8. Matriz de Permissões

| Operação | Admin | Responsável | Vendedor |
|----------|-------|-------------|----------|
| Criar Canais | ✅ | ❌ | ❌ |
| Criar Usuários | ✅ | ❌ | ❌ |
| Configurar Estágios | ✅ | ❌ | ❌ |
| Ver todos os dados | ✅ | ❌ | ❌ |
| Ver dados do canal | ✅ | ✅ | ❌ |
| Ver próprios dados | ✅ | ✅ | ✅ |
| Criar Leads | ✅ | ✅ | ✅ |
| Converter Leads | ✅ | ✅ | ✅ |
| Criar Oportunidades | ✅ | ✅ | ✅ |
| Mover no Kanban | ✅ | ✅ | ✅ |
| Registrar Atividades | ✅ | ✅ | ✅ |

---

## 9. Fluxo de Dados entre Módulos

```mermaid
flowchart LR
    LEAD[Lead] -->|Conversão| CONTA[Conta]
    LEAD -->|Conversão| CONTATO[Contato]
    LEAD -->|Conversão| OPORT[Oportunidade]
    
    CONTA -->|Possui| CONTATO
    CONTA -->|Possui| OPORT
    
    CONTATO -->|Contato Principal| OPORT
    
    OPORT -->|Está em| ESTAGIO[Estágio Funil]
    
    LEAD -.->|Atividades| ATIV[Atividades]
    CONTA -.->|Atividades| ATIV
    CONTATO -.->|Atividades| ATIV
    OPORT -.->|Atividades| ATIV
    
    USER[Usuário] -->|Proprietário| LEAD
    USER -->|Proprietário| CONTA
    USER -->|Proprietário| CONTATO
    USER -->|Proprietário| OPORT
    
    CANAL[Canal] -->|Possui| USER
    
    style LEAD fill:#fff3cd
    style CONTA fill:#d1ecf1
    style CONTATO fill:#d1ecf1
    style OPORT fill:#d4edda
    style ATIV fill:#e2e3e5
```

---

**Documentação de Fluxos Operacionais - Sistema CRM** 🚀
