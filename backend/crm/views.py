"""
Views da API do CRM
"""
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend

from .models import Canal, User, Lead, Conta, Contato, EstagioFunil, Oportunidade, Atividade
from .serializers import (
    CanalSerializer, UserSerializer, LeadSerializer, ContaSerializer,
    ContatoSerializer, EstagioFunilSerializer, OportunidadeSerializer,
    OportunidadeKanbanSerializer, AtividadeSerializer, LeadConversaoSerializer
)
from .permissions import HierarchyPermission, IsAdminUser


class CanalViewSet(viewsets.ModelViewSet):
    """ViewSet para Canais (apenas Admin)"""
    queryset = Canal.objects.all()
    serializer_class = CanalSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nome']
    ordering_fields = ['nome', 'data_criacao']


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet para Usuários (apenas Admin)"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['perfil', 'canal', 'is_active']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering_fields = ['username', 'date_joined']
    
    @action(detail=False, methods=['get'], permission_classes=[HierarchyPermission])
    def me(self, request):
        """Retorna informações do usuário logado"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class LeadViewSet(viewsets.ModelViewSet):
    """ViewSet para Leads"""
    serializer_class = LeadSerializer
    permission_classes = [HierarchyPermission]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'fonte']
    search_fields = ['nome', 'email', 'empresa']
    ordering_fields = ['nome', 'data_criacao']
    
    def get_queryset(self):
        """Aplica filtros de hierarquia"""
        user = self.request.user
        
        if user.perfil == 'ADMIN':
            return Lead.objects.all()
        elif user.perfil == 'RESPONSAVEL':
            return Lead.objects.filter(proprietario__canal=user.canal)
        else:  # VENDEDOR
            return Lead.objects.filter(proprietario=user)
    
    @action(detail=True, methods=['post'])
    def converter(self, request, pk=None):
        """Converte um Lead em Conta, Contato e opcionalmente Oportunidade"""
        lead = self.get_object()
        
        # Verifica se o lead já foi convertido
        if lead.status == Lead.STATUS_CONVERTIDO:
            return Response(
                {'error': 'Lead já foi convertido'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = LeadConversaoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            with transaction.atomic():
                # Cria a Conta
                conta = Conta.objects.create(
                    nome_empresa=lead.empresa or f"Empresa de {lead.nome}",
                    telefone_principal=lead.telefone,
                    email=lead.email,
                    proprietario=lead.proprietario
                )
                
                # Cria o Contato
                contato = Contato.objects.create(
                    nome=lead.nome,
                    email=lead.email,
                    telefone=lead.telefone,
                    cargo=lead.cargo,
                    conta=conta,
                    proprietario=lead.proprietario
                )
                
                # Cria Oportunidade se solicitado
                oportunidade = None
                if serializer.validated_data.get('criar_oportunidade', False):
                    # Busca o primeiro estágio do funil
                    primeiro_estagio = EstagioFunil.objects.filter(
                        tipo=EstagioFunil.TIPO_ABERTO
                    ).first()
                    
                    if primeiro_estagio:
                        nome_oportunidade = serializer.validated_data.get(
                            'nome_oportunidade',
                            f"Oportunidade - {lead.nome}"
                        )
                        
                        oportunidade = Oportunidade.objects.create(
                            nome=nome_oportunidade,
                            valor_estimado=serializer.validated_data.get('valor_estimado'),
                            conta=conta,
                            contato_principal=contato,
                            estagio=primeiro_estagio,
                            proprietario=lead.proprietario
                        )
                
                # Marca o lead como convertido
                lead.status = Lead.STATUS_CONVERTIDO
                lead.save()
                
                return Response({
                    'message': 'Lead convertido com sucesso',
                    'conta_id': conta.id,
                    'contato_id': contato.id,
                    'oportunidade_id': oportunidade.id if oportunidade else None
                }, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class ContaViewSet(viewsets.ModelViewSet):
    """ViewSet para Contas"""
    serializer_class = ContaSerializer
    permission_classes = [HierarchyPermission]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['setor', 'estado']
    search_fields = ['nome_empresa', 'cnpj', 'email']
    ordering_fields = ['nome_empresa', 'data_criacao']
    
    def get_queryset(self):
        user = self.request.user
        
        if user.perfil == 'ADMIN':
            return Conta.objects.all()
        elif user.perfil == 'RESPONSAVEL':
            return Conta.objects.filter(proprietario__canal=user.canal)
        else:
            return Conta.objects.filter(proprietario=user)
    
    @action(detail=True, methods=['get'])
    def contatos(self, request, pk=None):
        """Lista contatos da conta"""
        conta = self.get_object()
        contatos = conta.contatos.all()
        serializer = ContatoSerializer(contatos, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def oportunidades(self, request, pk=None):
        """Lista oportunidades da conta"""
        conta = self.get_object()
        oportunidades = conta.oportunidades.all()
        serializer = OportunidadeSerializer(oportunidades, many=True, context={'request': request})
        return Response(serializer.data)


class ContatoViewSet(viewsets.ModelViewSet):
    """ViewSet para Contatos"""
    serializer_class = ContatoSerializer
    permission_classes = [HierarchyPermission]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['conta', 'cargo']
    search_fields = ['nome', 'email', 'cargo']
    ordering_fields = ['nome', 'data_criacao']
    
    def get_queryset(self):
        user = self.request.user
        
        if user.perfil == 'ADMIN':
            return Contato.objects.all()
        elif user.perfil == 'RESPONSAVEL':
            return Contato.objects.filter(proprietario__canal=user.canal)
        else:
            return Contato.objects.filter(proprietario=user)


class EstagioFunilViewSet(viewsets.ModelViewSet):
    """ViewSet para Estágios do Funil (Admin para CRUD, todos podem ler)"""
    queryset = EstagioFunil.objects.all()
    serializer_class = EstagioFunilSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['ordem']
    
    def get_permissions(self):
        """Admin pode modificar, outros só podem ler"""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [HierarchyPermission()]


class OportunidadeViewSet(viewsets.ModelViewSet):
    """ViewSet para Oportunidades"""
    serializer_class = OportunidadeSerializer
    permission_classes = [HierarchyPermission]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['estagio', 'conta']
    search_fields = ['nome', 'conta__nome_empresa']
    ordering_fields = ['nome', 'valor_estimado', 'data_fechamento_esperada', 'data_criacao']
    
    def get_queryset(self):
        user = self.request.user
        
        if user.perfil == 'ADMIN':
            return Oportunidade.objects.all()
        elif user.perfil == 'RESPONSAVEL':
            return Oportunidade.objects.filter(proprietario__canal=user.canal)
        else:
            return Oportunidade.objects.filter(proprietario=user)
    
    @action(detail=False, methods=['get'])
    def kanban(self, request):
        """Retorna oportunidades abertas agrupadas por estágio para visão Kanban"""
        queryset = self.get_queryset().filter(
            estagio__tipo=EstagioFunil.TIPO_ABERTO
        ).select_related('conta', 'contato_principal', 'estagio', 'proprietario')
        
        serializer = OportunidadeKanbanSerializer(queryset, many=True)
        
        # Agrupa por estágio
        estagios = EstagioFunil.objects.filter(tipo=EstagioFunil.TIPO_ABERTO)
        kanban_data = []
        
        for estagio in estagios:
            oportunidades = [
                opp for opp in serializer.data
                if opp['estagio'] == estagio.id
            ]
            kanban_data.append({
                'estagio': EstagioFunilSerializer(estagio).data,
                'oportunidades': oportunidades
            })
        
        return Response(kanban_data)
    
    @action(detail=True, methods=['patch'])
    def mudar_estagio(self, request, pk=None):
        """Muda o estágio de uma oportunidade (usado no drag-and-drop do Kanban)"""
        oportunidade = self.get_object()
        novo_estagio_id = request.data.get('estagio_id')
        
        if not novo_estagio_id:
            return Response(
                {'error': 'estagio_id é obrigatório'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            novo_estagio = EstagioFunil.objects.get(id=novo_estagio_id)
            oportunidade.estagio = novo_estagio
            
            # Se mudou para estágio fechado, registra a data
            if novo_estagio.tipo in [EstagioFunil.TIPO_GANHO, EstagioFunil.TIPO_PERDIDO]:
                from django.utils import timezone
                oportunidade.data_fechamento_real = timezone.now().date()
            
            oportunidade.save()
            
            serializer = self.get_serializer(oportunidade)
            return Response(serializer.data)
        
        except EstagioFunil.DoesNotExist:
            return Response(
                {'error': 'Estágio não encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )


class AtividadeViewSet(viewsets.ModelViewSet):
    """ViewSet para Atividades"""
    serializer_class = AtividadeSerializer
    permission_classes = [HierarchyPermission]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['tipo', 'status']
    search_fields = ['titulo', 'descricao']
    ordering_fields = ['data_vencimento', 'data_criacao']
    
    def get_queryset(self):
        user = self.request.user
        
        if user.perfil == 'ADMIN':
            return Atividade.objects.all()
        elif user.perfil == 'RESPONSAVEL':
            return Atividade.objects.filter(proprietario__canal=user.canal)
        else:
            return Atividade.objects.filter(proprietario=user)
    
    @action(detail=True, methods=['post'])
    def concluir(self, request, pk=None):
        """Marca uma atividade como concluída"""
        atividade = self.get_object()
        
        from django.utils import timezone
        atividade.status = Atividade.STATUS_CONCLUIDA
        atividade.data_conclusao = timezone.now()
        atividade.save()
        
        serializer = self.get_serializer(atividade)
        return Response(serializer.data)
