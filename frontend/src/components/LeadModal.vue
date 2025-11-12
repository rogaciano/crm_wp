<template>
  <BaseModal
    :show="show"
    :title="isEdit ? 'Editar Lead' : 'Novo Lead'"
    @close="$emit('close')"
    @confirm="handleSubmit"
    :loading="loading"
  >
    <form @submit.prevent="handleSubmit" class="space-y-4">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Nome <span class="text-red-500">*</span>
          </label>
          <input
            v-model="form.nome"
            type="text"
            required
            class="input"
            placeholder="Nome completo"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Email
          </label>
          <input
            v-model="form.email"
            type="email"
            class="input"
            placeholder="email@exemplo.com"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Telefone
          </label>
          <input
            v-model="form.telefone"
            type="text"
            class="input"
            placeholder="(00) 0000-0000"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Empresa
          </label>
          <input
            v-model="form.empresa"
            type="text"
            class="input"
            placeholder="Nome da empresa"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Cargo
          </label>
          <input
            v-model="form.cargo"
            type="text"
            class="input"
            placeholder="Cargo do contato"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Fonte
          </label>
          <select v-model="form.fonte" class="input">
            <option value="">Selecione...</option>
            <option value="Site">Site</option>
            <option value="Evento">Evento</option>
            <option value="Indicação">Indicação</option>
            <option value="LinkedIn">LinkedIn</option>
            <option value="Cold Call">Cold Call</option>
            <option value="Outro">Outro</option>
          </select>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Status
          </label>
          <select v-model="form.status" class="input">
            <option value="Novo">Novo</option>
            <option value="Contatado">Contatado</option>
            <option value="Qualificado">Qualificado</option>
            <option value="Descartado">Descartado</option>
          </select>
        </div>
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">
          Observações
        </label>
        <textarea
          v-model="form.notas"
          rows="3"
          class="input"
          placeholder="Informações adicionais sobre o lead..."
        ></textarea>
      </div>
    </form>
  </BaseModal>
</template>

<script setup>
import { ref, watch } from 'vue'
import BaseModal from './BaseModal.vue'
import api from '@/services/api'

const props = defineProps({
  show: Boolean,
  lead: Object
})

const emit = defineEmits(['close', 'saved'])

const loading = ref(false)
const isEdit = ref(false)

const form = ref({
  nome: '',
  email: '',
  telefone: '',
  empresa: '',
  cargo: '',
  fonte: '',
  status: 'Novo',
  notas: ''
})

watch(() => props.lead, (newLead) => {
  if (newLead) {
    isEdit.value = true
    form.value = { ...newLead }
  } else {
    isEdit.value = false
    resetForm()
  }
}, { immediate: true })

function resetForm() {
  form.value = {
    nome: '',
    email: '',
    telefone: '',
    empresa: '',
    cargo: '',
    fonte: '',
    status: 'Novo',
    notas: ''
  }
}

async function handleSubmit() {
  loading.value = true
  try {
    const data = { ...form.value }
    
    // Remover campos vazios opcionais
    Object.keys(data).forEach(key => {
      if (data[key] === '' || data[key] === null || data[key] === undefined) {
        delete data[key]
      }
    })
    
    // Remover campos que não devem ser enviados na criação
    if (!isEdit.value) {
      delete data.id
      delete data.proprietario
      delete data.proprietario_nome
      delete data.data_criacao
      delete data.data_atualizacao
    }
    
    if (isEdit.value) {
      await api.put(`/leads/${form.value.id}/`, data)
    } else {
      await api.post('/leads/', data)
    }
    emit('saved')
    emit('close')
    resetForm()
  } catch (error) {
    console.error('Erro ao salvar lead:', error)
    const errorMsg = error.response?.data?.detail || 
                     JSON.stringify(error.response?.data) || 
                     error.message
    alert('Erro ao salvar lead: ' + errorMsg)
  } finally {
    loading.value = false
  }
}
</script>
