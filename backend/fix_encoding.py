"""
Script para corrigir encoding e recriar dados iniciais
Execute: python manage.py shell < fix_encoding.py
"""

from django.contrib.auth import get_user_model
from crm.models import Canal, EstagioFunil

User = get_user_model()

print("=== Corrigindo Encoding UTF-8 ===\n")

# Deletar dados antigos com encoding errado
print("Removendo dados antigos...")
EstagioFunil.objects.all().delete()
Canal.objects.all().delete()
User.objects.filter(username__in=['admin', 'resp_sul', 'vendedor1', 'vendedor2']).delete()

# Criar canais
print("\nCriando Canais...")
canais_data = [
    {"nome": "Canal Sul"},
    {"nome": "Canal Norte"},
    {"nome": "Canal Leste"},
    {"nome": "Canal Oeste"},
]

for canal_data in canais_data:
    canal = Canal.objects.create(**canal_data)
    print(f"  ✓ Canal criado: {canal.nome}")

# Criar estágios do funil
print("\nCriando Estágios do Funil...")
estagios_data = [
    {"nome": "Prospecção", "ordem": 1, "tipo": "ABERTO", "cor": "#3B82F6"},
    {"nome": "Qualificação", "ordem": 2, "tipo": "ABERTO", "cor": "#8B5CF6"},
    {"nome": "Proposta", "ordem": 3, "tipo": "ABERTO", "cor": "#EC4899"},
    {"nome": "Negociação", "ordem": 4, "tipo": "ABERTO", "cor": "#F59E0B"},
    {"nome": "Fechado - Ganho", "ordem": 5, "tipo": "GANHO", "cor": "#10B981"},
    {"nome": "Fechado - Perdido", "ordem": 6, "tipo": "PERDIDO", "cor": "#EF4444"},
]

for estagio_data in estagios_data:
    estagio = EstagioFunil.objects.create(**estagio_data)
    print(f"  ✓ Estágio criado: {estagio.nome}")

# Criar usuários de exemplo
print("\nCriando Usuários de Exemplo...")

# Admin
admin = User.objects.create(
    username="admin",
    email="admin@crm.com",
    first_name="Administrador",
    last_name="Sistema",
    perfil="ADMIN",
    is_staff=True,
    is_superuser=True,
)
admin.set_password("admin123")
admin.save()
print(f"  ✓ Admin criado: {admin.username} (senha: admin123)")

# Responsáveis
canal_sul = Canal.objects.get(nome="Canal Sul")
responsavel_sul = User.objects.create(
    username="resp_sul",
    email="resp.sul@crm.com",
    first_name="Responsável",
    last_name="Sul",
    perfil="RESPONSAVEL",
    canal=canal_sul,
)
responsavel_sul.set_password("resp123")
responsavel_sul.save()
canal_sul.responsavel = responsavel_sul
canal_sul.save()
print(f"  ✓ Responsável criado: {responsavel_sul.username} (senha: resp123)")

# Vendedores
vendedor1 = User.objects.create(
    username="vendedor1",
    email="vendedor1@crm.com",
    first_name="João",
    last_name="Silva",
    perfil="VENDEDOR",
    canal=canal_sul,
)
vendedor1.set_password("vend123")
vendedor1.save()
print(f"  ✓ Vendedor criado: {vendedor1.username} (senha: vend123)")

vendedor2 = User.objects.create(
    username="vendedor2",
    email="vendedor2@crm.com",
    first_name="Maria",
    last_name="Santos",
    perfil="VENDEDOR",
    canal=canal_sul,
)
vendedor2.set_password("vend123")
vendedor2.save()
print(f"  ✓ Vendedor criado: {vendedor2.username} (senha: vend123)")

print("\n=== Encoding corrigido! ===")
print("\nUsuários criados:")
print("  • admin / admin123 (Administrador)")
print("  • resp_sul / resp123 (Responsável de Canal)")
print("  • vendedor1 / vend123 (Vendedor)")
print("  • vendedor2 / vend123 (Vendedor)")
print("\nAcesse: http://localhost:9000/admin/")
