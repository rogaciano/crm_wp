<template>
  <div>
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-3xl font-bold text-gray-900">Gestão de Canais</h1>
      <button class="btn btn-primary">+ Novo Canal</button>
    </div>

    <div class="card overflow-hidden">
      <table class="table">
        <thead class="bg-gray-50">
          <tr>
            <th class="table-header">Nome</th>
            <th class="table-header">Responsável</th>
            <th class="table-header">Total Vendedores</th>
            <th class="table-header">Data Criação</th>
            <th class="table-header">Ações</th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-for="canal in canais" :key="canal.id" class="hover:bg-gray-50">
            <td class="table-cell font-medium">{{ canal.nome }}</td>
            <td class="table-cell">{{ canal.responsavel_nome || 'Sem responsável' }}</td>
            <td class="table-cell">{{ canal.total_vendedores }}</td>
            <td class="table-cell">{{ formatDate(canal.data_criacao) }}</td>
            <td class="table-cell">
              <button class="text-primary-600 hover:text-primary-700 mr-2">Editar</button>
              <button class="text-red-600 hover:text-red-700">Excluir</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/services/api'

const canais = ref([])

onMounted(() => {
  loadCanais()
})

async function loadCanais() {
  try {
    const response = await api.get('/canais/')
    canais.value = response.data.results || response.data
  } catch (error) {
    console.error('Erro ao carregar canais:', error)
  }
}

function formatDate(dateString) {
  if (!dateString) return 'N/A'
  return new Date(dateString).toLocaleDateString('pt-BR')
}
</script>
