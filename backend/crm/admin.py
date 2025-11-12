"""
Configuração do Django Admin para CRM
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Canal, User, Lead, Conta, Contato, EstagioFunil, Oportunidade, Atividade


@admin.register(Canal)
class CanalAdmin(admin.ModelAdmin):
    list_display = ['nome', 'responsavel', 'data_criacao']
    search_fields = ['nome']
    list_filter = ['data_criacao']


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'perfil', 'canal', 'is_active']
    list_filter = ['perfil', 'canal', 'is_active', 'is_staff']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Informações CRM', {'fields': ('perfil', 'canal', 'telefone')}),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Informações CRM', {'fields': ('perfil', 'canal', 'telefone')}),
    )


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ['nome', 'email', 'telefone', 'empresa', 'status', 'fonte', 'proprietario', 'data_criacao']
    list_filter = ['status', 'fonte', 'data_criacao']
    search_fields = ['nome', 'email', 'empresa']
    readonly_fields = ['data_criacao', 'data_atualizacao']


@admin.register(Conta)
class ContaAdmin(admin.ModelAdmin):
    list_display = ['nome_empresa', 'cnpj', 'telefone_principal', 'cidade', 'proprietario', 'data_criacao']
    list_filter = ['setor', 'estado', 'data_criacao']
    search_fields = ['nome_empresa', 'cnpj', 'email']
    readonly_fields = ['data_criacao', 'data_atualizacao']


@admin.register(Contato)
class ContatoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'email', 'telefone', 'cargo', 'conta', 'proprietario', 'data_criacao']
    list_filter = ['data_criacao', 'cargo']
    search_fields = ['nome', 'email', 'cargo']
    readonly_fields = ['data_criacao', 'data_atualizacao']


@admin.register(EstagioFunil)
class EstagioFunilAdmin(admin.ModelAdmin):
    list_display = ['nome', 'ordem', 'tipo', 'cor']
    list_filter = ['tipo']
    ordering = ['ordem']


@admin.register(Oportunidade)
class OportunidadeAdmin(admin.ModelAdmin):
    list_display = [
        'nome', 'valor_estimado', 'estagio', 'conta',
        'data_fechamento_esperada', 'proprietario', 'data_criacao'
    ]
    list_filter = ['estagio', 'data_criacao', 'data_fechamento_esperada']
    search_fields = ['nome', 'conta__nome_empresa', 'descricao']
    readonly_fields = ['data_criacao', 'data_atualizacao']


@admin.register(Atividade)
class AtividadeAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'tipo', 'status', 'data_vencimento', 'proprietario', 'data_criacao']
    list_filter = ['tipo', 'status', 'data_criacao']
    search_fields = ['titulo', 'descricao']
    readonly_fields = ['data_criacao', 'data_atualizacao']
