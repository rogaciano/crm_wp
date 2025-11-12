<template>
  <div>
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-3xl font-bold text-gray-900">Contatos</h1>
      <button class="btn btn-primary">+ Novo Contato</button>
    </div>

    <div class="card mb-6">
      <input
        v-model="searchQuery"
        type="text"
        placeholder="Buscar por nome, email ou cargo..."
        class="input"
        @input="loadContatos"
      />
    </div>

    <div class="card overflow-hidden">
      <table class="table">
        <thead class="bg-gray-50">
          <tr>
            <th class="table-header">Nome</th>
            <th class="table-header">Email</th>
            <th class="table-header">Telefone</th>
            <th class="table-header">Cargo</th>
            <th class="table-header">Empresa</th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-for="contato in contatos" :key="contato.id" class="hover:bg-gray-50">
            <td class="table-cell font-medium">{{ contato.nome }}</td>
            <td class="table-cell">{{ contato.email }}</td>
            <td class="table-cell">{{ contato.telefone }}</td>
            <td class="table-cell">{{ contato.cargo }}</td>
            <td class="table-cell">{{ contato.conta_nome }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/services/api'

const contatos = ref([])
const searchQuery = ref('')

onMounted(() => {
  loadContatos()
})

async function loadContatos() {
  try {
    const response = await api.get('/contatos/', { params: { search: searchQuery.value } })
    contatos.value = response.data.results || response.data
  } catch (error) {
    console.error('Erro ao carregar contatos:', error)
  }
}
</script>
