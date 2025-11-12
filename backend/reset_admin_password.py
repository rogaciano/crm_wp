#!/usr/bin/env python
"""Script para resetar a senha do usuário admin"""
import os
import sys
import django
import pymysql

# Configurar pymysql como substituto do mysqlclient
pymysql.install_as_MySQLdb()
pymysql.connections.charset = 'utf8mb4'

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

django.setup()

from crm.models import User

def reset_admin_password():
    """Reseta a senha do usuário admin"""
    try:
        # Buscar o usuário admin
        admin = User.objects.get(username='admin')
        
        # Definir nova senha
        nova_senha = 'admin123'
        admin.set_password(nova_senha)
        admin.save()
        
        print(f"✓ Senha do usuário '{admin.username}' resetada com sucesso!")
        print(f"  Username: {admin.username}")
        print(f"  Email: {admin.email}")
        print(f"  Nova senha: {nova_senha}")
        print(f"  Perfil: {admin.perfil}")
        print(f"  Is Staff: {admin.is_staff}")
        print(f"  Is Superuser: {admin.is_superuser}")
        
    except User.DoesNotExist:
        print("✗ Usuário 'admin' não encontrado!")
        print("\nCriando novo usuário admin...")
        
        # Criar novo usuário admin
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
        admin.set_password("admin123")
        admin.save()
        
        print(f"✓ Usuário admin criado com sucesso!")
        print(f"  Username: admin")
        print(f"  Email: admin@crm.com")
        print(f"  Senha: admin123")
        
    except Exception as e:
        print(f"✗ Erro ao resetar senha: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    print("=" * 50)
    print("RESET DE SENHA DO ADMIN")
    print("=" * 50)
    reset_admin_password()
    print("=" * 50)
