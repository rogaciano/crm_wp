<template>
  <div>
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-3xl font-bold text-gray-900">Atividades</h1>
      <button class="btn btn-primary">+ Nova Atividade</button>
    </div>

    <div class="card">
      <div class="space-y-4">
        <div
          v-for="atividade in atividades"
          :key="atividade.id"
          class="flex items-start justify-between p-4 border rounded-lg hover:bg-gray-50"
        >
          <div class="flex items-start space-x-4">
            <div :class="getIconClass(atividade.tipo)">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
              </svg>
            </div>
            <div>
              <h3 class="font-medium text-gray-900">{{ atividade.titulo }}</h3>
              <p class="text-sm text-gray-500">{{ atividade.tipo }}</p>
              <p v-if="atividade.descricao" class="text-sm text-gray-600 mt-1">{{ atividade.descricao }}</p>
              <p class="text-xs text-gray-400 mt-2">{{ atividade.proprietario_nome }}</p>
            </div>
          </div>
          <div class="text-right">
            <span :class="getStatusClass(atividade.status)">
              {{ atividade.status }}
            </span>
            <p v-if="atividade.data_vencimento" class="text-xs text-gray-500 mt-2">
              {{ formatDateTime(atividade.data_vencimento) }}
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/services/api'

const atividades = ref([])

onMounted(() => {
  loadAtividades()
})

async function loadAtividades() {
  try {
    const response = await api.get('/atividades/')
    atividades.value = response.data.results || response.data
  } catch (error) {
    console.error('Erro ao carregar atividades:', error)
  }
}

function getIconClass(tipo) {
  const classes = {
    'TAREFA': 'p-2 rounded-full bg-blue-100 text-blue-600',
    'LIGACAO': 'p-2 rounded-full bg-green-100 text-green-600',
    'REUNIAO': 'p-2 rounded-full bg-purple-100 text-purple-600',
    'EMAIL': 'p-2 rounded-full bg-yellow-100 text-yellow-600',
    'NOTA': 'p-2 rounded-full bg-gray-100 text-gray-600'
  }
  return classes[tipo] || 'p-2 rounded-full bg-gray-100 text-gray-600'
}

function getStatusClass(status) {
  const classes = {
    'Pendente': 'px-2 py-1 text-xs rounded-full bg-yellow-100 text-yellow-800',
    'Concluída': 'px-2 py-1 text-xs rounded-full bg-green-100 text-green-800',
    'Cancelada': 'px-2 py-1 text-xs rounded-full bg-red-100 text-red-800'
  }
  return classes[status] || 'px-2 py-1 text-xs rounded-full bg-gray-100 text-gray-800'
}

function formatDateTime(dateString) {
  if (!dateString) return 'N/A'
  return new Date(dateString).toLocaleString('pt-BR')
}
</script>
