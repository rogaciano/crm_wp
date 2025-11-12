<template>
  <div>
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-3xl font-bold text-gray-900">Estágios do Funil</h1>
      <button class="btn btn-primary">+ Novo Estágio</button>
    </div>

    <div class="card">
      <p class="text-gray-600 mb-6">
        Configure os estágios do funil de vendas. Os estágios serão exibidos no Kanban na ordem definida.
      </p>

      <div class="space-y-3">
        <div
          v-for="estagio in estagios"
          :key="estagio.id"
          class="flex items-center justify-between p-4 border rounded-lg hover:bg-gray-50"
        >
          <div class="flex items-center space-x-4">
            <div 
              class="w-12 h-12 rounded-lg flex items-center justify-center text-white font-bold"
              :style="{ backgroundColor: estagio.cor }"
            >
              {{ estagio.ordem }}
            </div>
            <div>
              <h3 class="font-medium text-gray-900">{{ estagio.nome }}</h3>
              <p class="text-sm text-gray-500">
                {{ getTipoLabel(estagio.tipo) }} • {{ estagio.total_oportunidades }} oportunidades
              </p>
            </div>
          </div>
          <div class="flex space-x-2">
            <button class="text-primary-600 hover:text-primary-700">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
              </svg>
            </button>
            <button class="text-red-600 hover:text-red-700">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/services/api'

const estagios = ref([])

onMounted(() => {
  loadEstagios()
})

async function loadEstagios() {
  try {
    const response = await api.get('/estagios-funil/')
    estagios.value = response.data.results || response.data
  } catch (error) {
    console.error('Erro ao carregar estágios:', error)
  }
}

function getTipoLabel(tipo) {
  const labels = {
    'ABERTO': 'Aberto',
    'GANHO': 'Fechado - Ganho',
    'PERDIDO': 'Fechado - Perdido'
  }
  return labels[tipo] || tipo
}
</script>
