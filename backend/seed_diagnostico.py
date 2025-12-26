import os
import django
import pymysql

pymysql.install_as_MySQLdb()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from crm.models import DiagnosticoPilar, DiagnosticoPergunta, DiagnosticoResposta

def seed_diagnostico():
    print("Iniciando seed de dados do diagnóstico...")
    
    # 1. Limpar dados existentes (opcional, cuidado em produção)
    DiagnosticoPilar.objects.all().delete()
    
    # 2. Criar Pilares
    p_producao = DiagnosticoPilar.objects.create(
        nome='Engenharia & Produção',
        slug='producao',
        ordem=1,
        cor='#EF4444', # Red
        descricao='Foco em fichas técnicas, controle de chão de fábrica e eficiência.'
    )
    
    p_estoque = DiagnosticoPilar.objects.create(
        nome='Estoques & Grade',
        slug='estoque',
        ordem=2,
        cor='#F59E0B', # Amber
        descricao='Gestão de matérias-primas e produtos acabados por cor/tamanho.'
    )

    p_comercial = DiagnosticoPilar.objects.create(
        nome='Comercial & Omnichannel',
        slug='comercial',
        ordem=3,
        cor='#10B981', # Emerald
        descricao='Integração entre atacado, varejo físico e e-commerce.'
    )

    p_financeiro = DiagnosticoPilar.objects.create(
        nome='Gestão Financeira',
        slug='financeiro',
        ordem=4,
        cor='#3B82F6', # Blue
        descricao='Rentabilidade, custos e fluxo de caixa.'
    )

    # 3. Perguntas e Respostas
    
    # PRODUCAO
    q1 = DiagnosticoPergunta.objects.create(
        pilar=p_producao,
        texto='Como você gerencia a ficha técnica dos seus produtos?',
        ordem=1,
        ajuda='A ficha técnica é a base para o controle de custos e estoque.'
    )
    DiagnosticoResposta.objects.create(pergunta=q1, texto='Não temos ficha técnica formalizada.', pontuacao=0, feedback='Alerta: Sem ficha técnica, seu custo é uma estimativa e o desperdício é invisível.')
    DiagnosticoResposta.objects.create(pergunta=q1, texto='Temos fichas em papel ou Excel separadas.', pontuacao=5, feedback='Melhoria: Você tem os dados, mas a falta de integração causa retrabalho.')
    DiagnosticoResposta.objects.create(pergunta=q1, texto='Fichas completas integradas no ERP (Dapic).', pontuacao=10, feedback='Excelente: Você tem a base para uma gestão industrial eficiente.')

    q2 = DiagnosticoPergunta.objects.create(
        pilar=p_producao,
        texto='Qual o seu nível de controle sobre as facções/costureiras externas?',
        ordem=2
    )
    DiagnosticoResposta.objects.create(pergunta=q2, texto='Não sei exatamente o que está com cada uma.', pontuacao=0)
    DiagnosticoResposta.objects.create(pergunta=q2, texto='Controlo por cadernos ou planilhas.', pontuacao=5)
    DiagnosticoResposta.objects.create(pergunta=q2, texto='Controle total de remessa e retorno no sistema.', pontuacao=10)

    # ESTOQUE
    q3 = DiagnosticoPergunta.objects.create(
        pilar=p_estoque,
        texto='Como é feito o controle de estoque por grade (tamanho/cor)?',
        ordem=1
    )
    DiagnosticoResposta.objects.create(pergunta=q3, texto='Controlamos apenas o saldo total do modelo.', pontuacao=0, feedback='Crítico: Isso gera vendas de itens que não existem fisicamente.')
    DiagnosticoResposta.objects.create(pergunta=q3, texto='Controle por grade, mas com furos frequentes.', pontuacao=6)
    DiagnosticoResposta.objects.create(pergunta=q3, texto='Controle total integrado com alta acuracidade.', pontuacao=10)

    # COMERCIAL
    q4 = DiagnosticoPergunta.objects.create(
        pilar=p_comercial,
        texto='Como suas vendas online se comunicam com suas lojas físicas?',
        ordem=1
    )
    DiagnosticoResposta.objects.create(pergunta=q4, texto='São operações totalmente separadas.', pontuacao=0)
    DiagnosticoResposta.objects.create(pergunta=q4, texto='Estoque unificado, mas baixa manual.', pontuacao=5)
    DiagnosticoResposta.objects.create(pergunta=q4, texto='Tudo integrado em tempo real no ERP.', pontuacao=10)

    # FINANCEIRO
    q5 = DiagnosticoPergunta.objects.create(
        pilar=p_financeiro,
        texto='Sabe exatamente o lucro líquido de cada peça vendida?',
        ordem=1
    )
    DiagnosticoResposta.objects.create(pergunta=q5, texto='Temos apenas uma ideia (mark-up).', pontuacao=0)
    DiagnosticoResposta.objects.create(pergunta=q5, texto='Calculamos custos, mas sem rateio fixo real.', pontuacao=6)
    DiagnosticoResposta.objects.create(pergunta=q5, texto='DRE exato por produto gerado pelo sistema.', pontuacao=10)

    print("Seed finalizado com sucesso!")

if __name__ == '__main__':
    seed_diagnostico()
