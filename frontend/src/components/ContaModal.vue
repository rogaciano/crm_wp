<template>
  <BaseModal
    :show="show"
    :title="isEdit ? 'Editar Conta' : 'Nova Conta'"
    size="lg"
    @close="$emit('close')"
    @confirm="handleSubmit"
    :loading="loading"
  >
    <form @submit.prevent="handleSubmit" class="space-y-4">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div class="md:col-span-2">
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Nome da Empresa <span class="text-red-500">*</span>
          </label>
          <input
            v-model="form.nome_empresa"
            type="text"
            required
            class="input"
            placeholder="Razão social ou nome fantasia"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            CNPJ
          </label>
          <input
            v-model="form.cnpj"
            type="text"
            class="input"
            placeholder="00.000.000/0000-00"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Setor
          </label>
          <input
            v-model="form.setor"
            type="text"
            class="input"
            placeholder="Ex: Tecnologia, Varejo"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Telefone Principal
          </label>
          <input
            v-model="form.telefone_principal"
            type="text"
            class="input"
            placeholder="(00) 0000-0000"
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
            placeholder="contato@empresa.com"
          />
        </div>

        <div class="md:col-span-2">
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Website
          </label>
          <input
            v-model="form.website"
            type="url"
            class="input"
            placeholder="https://www.empresa.com"
          />
        </div>

        <div class="md:col-span-2">
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Endereço
          </label>
          <input
            v-model="form.endereco"
            type="text"
            class="input"
            placeholder="Rua, número, complemento"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Cidade
          </label>
          <input
            v-model="form.cidade"
            type="text"
            class="input"
            placeholder="Nome da cidade"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Estado
          </label>
          <select v-model="form.estado" class="input">
            <option value="">Selecione...</option>
            <option value="AC">AC</option>
            <option value="AL">AL</option>
            <option value="AP">AP</option>
            <option value="AM">AM</option>
            <option value="BA">BA</option>
            <option value="CE">CE</option>
            <option value="DF">DF</option>
            <option value="ES">ES</option>
            <option value="GO">GO</option>
            <option value="MA">MA</option>
            <option value="MT">MT</option>
            <option value="MS">MS</option>
            <option value="MG">MG</option>
            <option value="PA">PA</option>
            <option value="PB">PB</option>
            <option value="PR">PR</option>
            <option value="PE">PE</option>
            <option value="PI">PI</option>
            <option value="RJ">RJ</option>
            <option value="RN">RN</option>
            <option value="RS">RS</option>
            <option value="RO">RO</option>
            <option value="RR">RR</option>
            <option value="SC">SC</option>
            <option value="SP">SP</option>
            <option value="SE">SE</option>
            <option value="TO">TO</option>
          </select>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            CEP
          </label>
          <input
            v-model="form.cep"
            type="text"
            class="input"
            placeholder="00000-000"
          />
        </div>
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
  conta: Object
})

const emit = defineEmits(['close', 'saved'])

const loading = ref(false)
const isEdit = ref(false)

const form = ref({
  nome_empresa: '',
  cnpj: '',
  setor: '',
  telefone_principal: '',
  email: '',
  website: '',
  endereco: '',
  cidade: '',
  estado: '',
  cep: ''
})

watch(() => props.conta, (newConta) => {
  if (newConta) {
    isEdit.value = true
    form.value = { ...newConta }
  } else {
    isEdit.value = false
    resetForm()
  }
}, { immediate: true })

function resetForm() {
  form.value = {
    nome_empresa: '',
    cnpj: '',
    setor: '',
    telefone_principal: '',
    email: '',
    website: '',
    endereco: '',
    cidade: '',
    estado: '',
    cep: ''
  }
}

async function handleSubmit() {
  loading.value = true
  try {
    const data = { ...form.value }
    
    // Remover campos vazios opcionais e campos de sistema
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
      delete data.total_contatos
      delete data.total_oportunidades
      delete data.data_criacao
      delete data.data_atualizacao
    }
    
    if (isEdit.value) {
      await api.put(`/contas/${form.value.id}/`, data)
    } else {
      await api.post('/contas/', data)
    }
    emit('saved')
    emit('close')
    resetForm()
  } catch (error) {
    console.error('Erro ao salvar conta:', error)
    const errorMsg = error.response?.data?.detail || 
                     JSON.stringify(error.response?.data) || 
                     error.message
    alert('Erro ao salvar conta: ' + errorMsg)
  } finally {
    loading.value = false
  }
}
</script>
