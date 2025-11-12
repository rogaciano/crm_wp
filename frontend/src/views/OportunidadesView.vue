<template>
  <div>
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-3xl font-bold text-gray-900">Oportunidades</h1>
      <button class="btn btn-primary">+ Nova Oportunidade</button>
    </div>

    <div class="card overflow-hidden">
      <table class="table">
        <thead class="bg-gray-50">
          <tr>
            <th class="table-header">Nome</th>
            <th class="table-header">Conta</th>
            <th class="table-header">Valor</th>
            <th class="table-header">Estágio</th>
            <th class="table-header">Previsão</th>
            <th class="table-header">Probabilidade</th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-for="oportunidade in oportunidades" :key="oportunidade.id" class="hover:bg-gray-50">
            <td class="table-cell font-medium">{{ oportunidade.nome }}</td>
            <td class="table-cell">{{ oportunidade.conta_nome }}</td>
            <td class="table-cell font-semibold text-green-600">
              R$ {{ Number(oportunidade.valor_estimado || 0).toLocaleString('pt-BR', { minimumFractionDigits: 2 }) }}
            </td>
            <td class="table-cell">
              <span class="px-2 py-1 text-xs rounded-full" :style="{ backgroundColor: oportunidade.estagio_cor + '20', color: oportunidade.estagio_cor }">
                {{ oportunidade.estagio_nome }}
              </span>
            </td>
            <td class="table-cell">{{ formatDate(oportunidade.data_fechamento_esperada) }}</td>
            <td class="table-cell">{{ oportunidade.probabilidade }}%</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/services/api'

const oportunidades = ref([])

onMounted(() => {
  loadOportunidades()
})

async function loadOportunidades() {
  try {
    const response = await api.get('/oportunidades/')
    oportunidades.value = response.data.results || response.data
  } catch (error) {
    console.error('Erro ao carregar oportunidades:', error)
  }
}

function formatDate(dateString) {
  if (!dateString) return 'N/A'
  return new Date(dateString).toLocaleDateString('pt-BR')
}
</script>
