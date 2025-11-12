import os
import sys
import django
import pymysql

# Configurar pymysql como substituto do mysqlclient
pymysql.install_as_MySQLdb()
pymysql.connections.charset = 'utf8mb4'

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.contrib.auth import authenticate
from crm.models import User

print("=" * 60)
print("TESTE DE AUTENTICAÇÃO")
print("=" * 60)

# Testar autenticação
username = 'admin'
password = 'admin123'

print(f"\nTestando login com:")
print(f"  Username: {username}")
print(f"  Password: {password}")

user = authenticate(username=username, password=password)

if user:
    print(f"\n✓ AUTENTICAÇÃO BEM-SUCEDIDA!")
    print(f"  User ID: {user.id}")
    print(f"  Username: {user.username}")
    print(f"  Email: {user.email}")
    print(f"  Perfil: {user.perfil}")
    print(f"  Is Active: {user.is_active}")
    print(f"  Is Staff: {user.is_staff}")
    print(f"  Is Superuser: {user.is_superuser}")
else:
    print(f"\n✗ AUTENTICAÇÃO FALHOU!")
    print(f"\nVerificando se o usuário existe...")
    try:
        user = User.objects.get(username=username)
        print(f"  ✓ Usuário '{username}' existe no banco")
        print(f"  Email: {user.email}")
        print(f"  Is Active: {user.is_active}")
        print(f"\n  Problema: A senha está incorreta!")
        print(f"  Resetando senha...")
        user.set_password(password)
        user.save()
        print(f"  ✓ Senha resetada para: {password}")
        
        # Testar novamente
        user = authenticate(username=username, password=password)
        if user:
            print(f"\n✓ AUTENTICAÇÃO AGORA FUNCIONA!")
        else:
            print(f"\n✗ Ainda há um problema com a autenticação")
    except User.DoesNotExist:
        print(f"  ✗ Usuário '{username}' não existe no banco")

print("=" * 60)
