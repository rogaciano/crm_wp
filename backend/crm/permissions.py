"""
Permissões customizadas para hierarquia de Canais
"""
from rest_framework import permissions


class HierarchyPermission(permissions.BasePermission):
    """
    Permissão baseada na hierarquia de vendas:
    - Admin: vê tudo
    - Responsável: vê dados do seu canal
    - Vendedor: vê apenas seus dados
    """
    
    def has_permission(self, request, view):
        # Usuário deve estar autenticado
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Admin tem acesso total
        if request.user.perfil == 'ADMIN':
            return True
        
        # Responsável e Vendedor precisam de canal
        if request.user.perfil in ['RESPONSAVEL', 'VENDEDOR']:
            return request.user.canal is not None
        
        return False
    
    def has_object_permission(self, request, view, obj):
        """
        Verifica se o usuário pode acessar um objeto específico
        """
        user = request.user
        
        # Admin tem acesso total
        if user.perfil == 'ADMIN':
            return True
        
        # Verifica se o objeto tem proprietario
        if not hasattr(obj, 'proprietario'):
            return False
        
        # Vendedor: só seus próprios objetos
        if user.perfil == 'VENDEDOR':
            return obj.proprietario == user
        
        # Responsável: objetos do seu canal
        if user.perfil == 'RESPONSAVEL':
            return obj.proprietario.canal == user.canal
        
        return False


class IsAdminUser(permissions.BasePermission):
    """
    Permite acesso apenas para usuários com perfil ADMIN
    """
    
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.perfil == 'ADMIN'
        )


class IsResponsavelOrAdmin(permissions.BasePermission):
    """
    Permite acesso para Responsável de Canal ou Admin
    """
    
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.perfil in ['ADMIN', 'RESPONSAVEL']
        )
