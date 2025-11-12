# Projeto: Sistema de CRM de Vendas Funcional

**Versão:** 1.1
**Data:** 04 de Novembro de 2025
**Analista:** Gemini

## 1. Visão Geral do Sistema

O objetivo deste projeto é desenvolver um sistema de CRM (Customer Relationship Management) focado na gestão do funil de vendas. A plataforma permitirá o cadastro e gestão de Leads, Contas (empresas), Contatos (pessoas), e Oportunidades (negócios).

O sistema será estruturado para suportar uma hierarquia de vendas baseada em **Canais**, onde cada Canal possui um **Responsável** (Gerente) que pode visualizar os dados de todos os **Vendedores** associados ao seu canal.

## 2. Stack Tecnológica

* **Backend:** Python 3+ com **Django** e **Django REST Framework (DRF)**.
* **Frontend:** **Vue.js** (como uma Single Page Application - SPA).
* **Banco de Dados:** **PostgreSQL**.
* **UI/CSS:** **Tailwind CSS**.

## 3. Perfis de Usuário e Hierarquia

O sistema terá três níveis de acesso:

1.  **Administrador:**
    * Acesso total a todos os módulos e dados de todos os canais.
    * Gerencia usuários (CRUD).
    * Gerencia Canais de Vendas (CRUD).
    * Configura os estágios do funil de vendas.

2.  **Responsável de Canal (Gerente):**
    * Acesso de Leitura/Escrita a **TODOS** os dados (Leads, Contas, Contatos, Oportunidades) que pertencem aos Vendedores do **SEU** canal.
    * Não pode ver dados de outros canais.
    * Não pode gerenciar usuários ou configurações do sistema.

3.  **Vendedor (Usuário Padrão):**
    * Acesso de Leitura/Escrita **APENAS** aos dados que criou ou que foram atribuídos a ele (`proprietario_id` = seu ID).
    * Não pode ver dados de outros Vendedores, mesmo dentro do seu canal.

## 4. Requisitos Funcionais (RF)

### Módulo 0: Autenticação e Usuários (RF-000)

* **RF-001:** O sistema deve permitir que um usuário se autentique via API (login com email e senha), retornando um token (ex: JWT).
* **RF-002:** O sistema deve implementar um fluxo de "Esqueci minha senha" via e-mail.
* **RF-003 (Admin):** O Admin deve ter uma interface para criar, editar, desativar e excluir usuários.
* **RF-004 (Admin):** Ao criar/editar um usuário, o Admin deve definir:
    * `Perfil` (Admin, Responsável de Canal, Vendedor).
    * `Canal_Associado` (Obrigatório se o perfil for Responsável ou Vendedor).

### Módulo 6: Gestão de Canais de Vendas (RF-600)

* **RF-601 (Admin):** O Admin deve ter uma interface (CRUD) para gerenciar os Canais de Vendas.
* **RF-602 (Admin):** Campos Mínimos do Canal: `Nome do Canal`.
* **RF-603 (Admin):** Ao criar/editar um Canal, o Admin deve poder designar UM `Usuário` com perfil de "Responsável" para aquele canal.

---

### Módulo 1: Gestão de Leads (RF-100)

* **Definição:** Um prospecto inicial, um contato "cru" que ainda não foi qualificado.
* **RF-101:** O usuário deve poder criar um Lead.
    * **Campos Mínimos:** `Nome`, `Email`, `Telefone`, `Fonte` (ex: "Site", "Evento"), `Status` (ex: "Novo", "Contatado"), `proprietario_id`.
* **RF-102:** O sistema deve exibir uma listagem paginada de Leads (respeitando as regras de visibilidade da hierarquia).
* **RF-103:** O usuário deve poder editar e excluir Leads (que ele tem permissão para ver).
* **RF-104 (Fluxo Crítico) Conversão de Lead:**
    * O usuário deve poder "Converter" um Lead.
    * Ao converter, a API deve criar:
        1.  Uma **Conta** (Empresa).
        2.  Um **Contato** (Pessoa), vinculado à Conta.
        3.  (Opcional) Uma **Oportunidade** inicial.
    * O Lead original deve ser marcado como `status = "Convertido"`.

### Módulo 2: Gestão de Contas (RF-200)

* **Definição:** A Conta representa uma empresa/organização.
* **RF-201:** O usuário deve poder realizar o CRUD de Contas.
    * **Campos Mínimos:** `Nome da Empresa`, `CNPJ/ID Fiscal` (opcional), `Telefone Principal`, `Website`, `Setor`, `Endereço`, `proprietario_id`.
* **RF-202:** A tela de visualização de uma Conta deve exibir listas de **Contatos** e **Oportunidades** vinculados a ela.

### Módulo 3: Gestão de Contatos (RF-300)

* **Definição:** O Contato representa uma pessoa física, vinculada a uma Conta.
* **RF-301:** O usuário deve poder realizar o CRUD de Contatos.
    * **Campos Mínimos:** `Nome`, `Email`, `Telefone`, `Cargo`, `conta_id` (FK para Conta), `proprietario_id`.
* **RF-302:** Um Contato **deve** estar associado a UMA Conta (Relação N-para-1).

### Módulo 4: Gestão de Oportunidades (Funil de Vendas) (RF-400)

* **Definição:** A Oportunidade (ou "Negócio") é uma venda em potencial.
* **RF-401:** O usuário deve poder realizar o CRUD de Oportunidades.
    * **Campos Mínimos:** `Nome da Oportunidade`, `Valor Estimado` (R$), `Data de Fechamento Esperada`, `estagio_id` (FK para Estágio), `conta_id` (FK), `contato_id` (FK opcional), `proprietario_id`.
* **RF-402 (Admin):** O Admin deve poder configurar (CRUD) os `Estágios do Funil`.
    * Campos: `Nome` (ex: "Prospecção", "Negociação"), `Ordem`.
* **RF-403 (Visão Crítica) Kanban:**
    * O frontend (Vue.js) deve exibir uma tela principal com todas as Oportunidades (visíveis) em um quadro Kanban.
    * Cada coluna do Kanban representa um `Estágio do Funil`.
    * O usuário deve poder arrastar (drag-and-drop) um card de Oportunidade de uma coluna para outra.
    * Ao soltar, o frontend deve chamar a API (PATCH) para atualizar o `estagio_id` da Oportunidade.
* **RF-404:** Oportunidades com estágio "Fechado - Ganho" ou "Fechado - Perdido" devem sair do Kanban principal.

### Módulo 5: Gestão de Atividades e Histórico (RF-500)

* **Definição:** Interações registradas com Leads, Contatos, Contas ou Oportunidades.
* **RF-501:** O usuário deve poder registrar Atividades (CRUD).
    * **Tipos de Atividades:** `Tarefa`, `Ligação`, `Reunião`, `E-mail`.
* **RF-502:** Campos de Atividade/Tarefa:
    * `Tipo`, `Título`, `Data de Vencimento` (para tarefas), `Status` ("Pendente", "Concluída"), `Descrição/Notas`.
* **RF-503 (Relação Polimórfica):** Uma Atividade deve poder ser associada a um Lead, Conta, Contato ou Oportunidade. (No Django, isso é feito via `GenericForeignKey`).
* **RF-504 (Visão Crítica) Linha do Tempo:**
    * As páginas de detalhe (Conta, Contato, Oportunidade) devem exibir uma "Linha do Tempo" (timeline) unificada, mostrando todas as atividades registradas em ordem cronológica.

## 5. Regras de Negócio de Visibilidade de Dados (CRÍTICO)

A API (Django) deve implementar filtros rigorosos em todos os *querysets* para garantir a hierarquia:

1.  **Vendedor:** SÓ pode ver registros onde `proprietario_id` == (ID do usuário logado).
2.  **Responsável de Canal:** Vê todos os registros cujo `proprietario_id` pertença a qualquer usuário que esteja no `canal_id` do Responsável.
3.  **Administrador:** Vê todos os registros (sem filtro de propriedade).

## 6. Modelo de Dados (Sugestão para `models.py`)

```python
# Esta é uma representação simplificada dos models do Django

from django.contrib.auth.models import AbstractUser
from django.db import models

class Canal(models.Model):
    nome = models.CharField(max_length=100)
    # O Responsável será um ForeignKey de 'User' apontando para cá

class User(AbstractUser):
    # Perfis
    PERFIL_VENDEDOR = 'VENDEDOR'
    PERFIL_RESPONSAVEL = 'RESPONSAVEL'
    PERFIL_ADMIN = 'ADMIN'
    PERFIL_CHOICES = [
        (PERFIL_VENDEDOR, 'Vendedor'),
        (PERFIL_RESPONSAVEL, 'Responsável de Canal'),
        (PERFIL_ADMIN, 'Administrador'),
    ]
    
    perfil = models.CharField(max_length=20, choices=PERFIL_CHOICES, default=PERFIL_VENDEDOR)
    canal = models.ForeignKey(Canal, on_delete=models.SET_NULL, null=True, blank=True, related_name='vendedores')
    
    # Adicionar um campo para 'responsavel_de' no Canal
    # Canal.responsavel = models.OneToOneField(User, ...)

class Lead(models.Model):
    nome = models.CharField(max_length=255)
    email = models.EmailField(null=True, blank=True)
    telefone = models.CharField(max_length=20, null=True, blank=True)
    fonte = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=100, default='Novo')
    proprietario = models.ForeignKey(User, on_delete=models.PROTECT)
    data_criacao = models.DateTimeField(auto_now_add=True)

class Conta(models.Model):
    nome_empresa = models.CharField(max_length=255)
    cnpj = models.CharField(max_length=20, null=True, blank=True)
    telefone_principal = models.CharField(max_length=20, null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    setor = models.CharField(max_length=100, null=True, blank=True)
    proprietario = models.ForeignKey(User, on_delete=models.PROTECT)
    data_criacao = models.DateTimeField(auto_now_add=True)

class Contato(models.Model):
    nome = models.CharField(max_length=255)
    email = models.EmailField(null=True, blank=True)
    telefone = models.CharField(max_length=20, null=True, blank=True)
    cargo = models.CharField(max_length=100, null=True, blank=True)
    conta = models.ForeignKey(Conta, on_delete=models.CASCADE, related_name='contatos')
    proprietario = models.ForeignKey(User, on_delete=models.PROTECT)
    data_criacao = models.DateTimeField(auto_now_add=True)

class EstagioFunil(models.Model):
    nome = models.CharField(max_length=100)
    ordem = models.PositiveIntegerField(default=0)
    # Ex: 'Aberto', 'Ganho', 'Perdido'
    tipo = models.CharField(max_length=20, default='Aberto')

    class Meta:
        ordering = ['ordem']

class Oportunidade(models.Model):
    nome = models.CharField(max_length=255)
    valor_estimado = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    data_fechamento_esperada = models.DateField(null=True, blank=True)
    estagio = models.ForeignKey(EstagioFunil, on_delete=models.PROTECT)
    conta = models.ForeignKey(Conta, on_delete=models.CASCADE, related_name='oportunidades')
    contato_principal = models.ForeignKey(Contato, on_delete=models.SET_NULL, null=True, blank=True)
    proprietario = models.ForeignKey(User, on_delete=models.PROTECT)
    data_criacao = models.DateTimeField(auto_now_add=True)

class Atividade(models.Model):
    # Usar ContentType framework para associação polimórfica
    # content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # object_id = models.PositiveIntegerField()
    # associado_a = GenericForeignKey('content_type', 'object_id')
    
    TIPO_TAREFA = 'TAREFA'
    TIPO_LIGACAO = 'LIGACAO'
    TIPO_REUNIAO = 'REUNIAO'
    TIPO_CHOICES = [
        (TIPO_TAREFA, 'Tarefa'),
        (TIPO_LIGACAO, 'Ligação'),
        (TIPO_REUNIAO, 'Reunião'),
    ]
    
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    titulo = models.CharField(max_length=255) # Para tarefas
    descricao = models.TextField(null=True, blank=True)
    data_vencimento = models.DateTimeField(null=True, blank=True) # Para tarefas
    status = models.CharField(max_length=20, default='Pendente') # Pendente, Concluída
    proprietario = models.ForeignKey(User, on_delete=models.PROTECT)
    data_criacao = models.DateTimeField(auto_now_add=True)