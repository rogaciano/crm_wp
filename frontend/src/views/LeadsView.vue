<template>
  <div>
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-3xl font-bold text-gray-900">Leads</h1>
      <button @click="openCreateModal" class="btn btn-primary">
        + Novo Lead
      </button>
    </div>

    <!-- Filtros -->
    <div class="card mb-6">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Buscar por nome, email ou empresa..."
          class="input"
          @input="loadLeads"
        />
        <select v-model="statusFilter" class="input" @change="loadLeads">
          <option value="">Todos os Status</option>
          <option value="Novo">Novo</option>
          <option value="Contatado">Contatado</option>
          <option value="Qualificado">Qualificado</option>
          <option value="Convertido">Convertido</option>
          <option value="Descartado">Descartado</option>
        </select>
        <select v-model="fonteFilter" class="input" @change="loadLeads">
          <option value="">Todas as Fontes</option>
          <option value="Site">Site</option>
          <option value="Evento">Evento</option>
          <option value="Indicação">Indicação</option>
          <option value="LinkedIn">LinkedIn</option>
        </select>
      </div>
    </div>

    <!-- Tabela -->
    <div class="card overflow-hidden">
      <div v-if="loading" class="text-center py-12">
        <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
      </div>

      <table v-else class="table">
        <thead class="bg-gray-50">
          <tr>
            <th class="table-header">Nome</th>
            <th class="table-header">Email</th>
            <th class="table-header">Telefone</th>
            <th class="table-header">Empresa</th>
            <th class="table-header">Status</th>
            <th class="table-header">Fonte</th>
            <th class="table-header">Ações</th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-for="lead in leads" :key="lead.id" class="hover:bg-gray-50">
            <td class="table-cell font-medium">{{ lead.nome }}</td>
            <td class="table-cell">{{ lead.email }}</td>
            <td class="table-cell">{{ lead.telefone }}</td>
            <td class="table-cell">{{ lead.empresa }}</td>
            <td class="table-cell">
              <span :class="getStatusClass(lead.status)">
                {{ lead.status }}
              </span>
            </td>
            <td class="table-cell">{{ lead.fonte }}</td>
            <td class="table-cell">
              <div class="flex space-x-2">
                <button
                  v-if="lead.status !== 'Convertido'"
                  @click="converterLead(lead)"
                  class="text-green-600 hover:text-green-700"
                  title="Converter Lead"
                >
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
                  </svg>
                </button>
                <button
                  @click="openEditModal(lead)"
                  class="text-primary-600 hover:text-primary-700"
                  title="Editar"
                >
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                  </svg>
                </button>
                <button
                  @click="deleteLead(lead)"
                  class="text-red-600 hover:text-red-700"
                  title="Excluir"
                >
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                  </svg>
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>

      <div v-if="leads.length === 0 && !loading" class="text-center py-12 text-gray-500">
        Nenhum lead encontrado
      </div>

      <!-- Modal -->
      <LeadModal
        :show="showModal"
        :lead="selectedLead"
        @close="closeModal"
        @saved="handleSaved"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/services/api'
import LeadModal from '@/components/LeadModal.vue'

const leads = ref([])
const loading = ref(false)
const showModal = ref(false)
const selectedLead = ref(null)
const searchQuery = ref('')
const statusFilter = ref('')
const fonteFilter = ref('')

onMounted(() => {
  loadLeads()
})

async function loadLeads() {
  loading.value = true
  try {
    const params = {
      search: searchQuery.value,
      status: statusFilter.value,
      fonte: fonteFilter.value
    }
    const response = await api.get('/leads/', { params })
    leads.value = response.data.results || response.data
  } catch (error) {
    console.error('Erro ao carregar leads:', error)
  } finally {
    loading.value = false
  }
}

function getStatusClass(status) {
  const classes = {
    'Novo': 'px-2 py-1 text-xs rounded-full bg-blue-100 text-blue-800',
    'Contatado': 'px-2 py-1 text-xs rounded-full bg-yellow-100 text-yellow-800',
    'Qualificado': 'px-2 py-1 text-xs rounded-full bg-purple-100 text-purple-800',
    'Convertido': 'px-2 py-1 text-xs rounded-full bg-green-100 text-green-800',
    'Descartado': 'px-2 py-1 text-xs rounded-full bg-gray-100 text-gray-800'
  }
  return classes[status] || 'px-2 py-1 text-xs rounded-full bg-gray-100 text-gray-800'
}

function openCreateModal() {
  selectedLead.value = null
  showModal.value = true
}

function openEditModal(lead) {
  selectedLead.value = lead
  showModal.value = true
}

function closeModal() {
  showModal.value = false
  selectedLead.value = null
}

function handleSaved() {
  loadLeads()
}

async function converterLead(lead) {
  if (!confirm(`Deseja converter o lead "${lead.nome}"?`)) return
  
  try {
    await api.post(`/leads/${lead.id}/converter/`, {
      criar_oportunidade: true,
      nome_oportunidade: `Oportunidade - ${lead.nome}`
    })
    alert('Lead convertido com sucesso!')
    loadLeads()
  } catch (error) {
    console.error('Erro ao converter lead:', error)
    alert('Erro ao converter lead')
  }
}

async function deleteLead(lead) {
  if (!confirm(`Deseja excluir o lead "${lead.nome}"?`)) return
  
  try {
    await api.delete(`/leads/${lead.id}/`)
    loadLeads()
  } catch (error) {
    console.error('Erro ao excluir lead:', error)
    alert('Erro ao excluir lead')
  }
}
</script>
