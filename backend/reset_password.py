from crm.models import User

# Buscar ou criar o usuário admin
try:
    admin = User.objects.get(username='admin')
    print(f"Usuário encontrado: {admin.username}")
except User.DoesNotExist:
    print("Criando novo usuário admin...")
    admin = User.objects.create(
        username="admin",
        email="admin@crm.com",
        first_name="Administrador",
        last_name="Sistema",
        perfil="ADMIN",
        is_staff=True,
        is_superuser=True,
        is_active=True
    )

# Resetar a senha
admin.set_password("admin123")
admin.save()

print("=" * 50)
print("SENHA RESETADA COM SUCESSO!")
print("=" * 50)
print(f"Username: {admin.username}")
print(f"Email: {admin.email}")
print(f"Senha: admin123")
print(f"Perfil: {admin.perfil}")
print(f"Is Active: {admin.is_active}")
print(f"Is Staff: {admin.is_staff}")
print(f"Is Superuser: {admin.is_superuser}")
print("=" * 50)
