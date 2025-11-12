<template>
  <BaseModal
    :show="show"
    :title="isEdit ? 'Editar Oportunidade' : 'Nova Oportunidade'"
    size="lg"
    @close="$emit('close')"
    @confirm="handleSubmit"
    :loading="loading"
  >
    <form @submit.prevent="handleSubmit" class="space-y-4">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div class="md:col-span-2">
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Nome da Oportunidade <span class="text-red-500">*</span>
          </label>
          <input
            v-model="form.nome"
            type="text"
            required
            class="input"
            placeholder="Ex: Venda de Sistema - Empresa XYZ"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Conta <span class="text-red-500">*</span>
          </label>
          <select v-model="form.conta" required class="input">
            <option value="">Selecione uma conta...</option>
            <option v-for="conta in contas" :key="conta.id" :value="conta.id">
              {{ conta.nome_empresa }}
            </option>
          </select>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Contato Principal
          </label>
          <select v-model="form.contato_principal" class="input">
            <option value="">Selecione um contato...</option>
            <option v-for="contato in contatos" :key="contato.id" :value="contato.id">
              {{ contato.nome }}
            </option>
          </select>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Estágio do Funil <span class="text-red-500">*</span>
          </label>
          <select v-model="form.estagio" required class="input">
            <option value="">Selecione...</option>
            <option v-for="estagio in estagios" :key="estagio.id" :value="estagio.id">
              {{ estagio.nome }}
            </option>
          </select>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Valor Estimado (R$)
          </label>
          <input
            v-model.number="form.valor_estimado"
            type="number"
            step="0.01"
            min="0"
            class="input"
            placeholder="0,00"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Data de Fechamento Esperada
          </label>
          <input
            v-model="form.data_fechamento_esperada"
            type="date"
            class="input"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Probabilidade (%)
          </label>
          <input
            v-model.number="form.probabilidade"
            type="number"
            min="0"
            max="100"
            class="input"
            placeholder="0-100"
          />
        </div>

        <div class="md:col-span-2">
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Descrição
          </label>
          <textarea
            v-model="form.descricao"
            rows="3"
            class="input"
            placeholder="Detalhes sobre a oportunidade..."
          ></textarea>
        </div>
      </div>
    </form>
  </BaseModal>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import BaseModal from './BaseModal.vue'
import api from '@/services/api'

const props = defineProps({
  show: Boolean,
  oportunidade: Object
})

const emit = defineEmits(['close', 'saved'])

const loading = ref(false)
const isEdit = ref(false)
const contas = ref([])
const contatos = ref([])
const estagios = ref([])

const form = ref({
  nome: '',
  conta: '',
  contato_principal: '',
  estagio: '',
  valor_estimado: 0,
  data_fechamento_esperada: '',
  probabilidade: 0,
  descricao: ''
})

watch(() => props.show, async (newVal) => {
  if (newVal) {
    await loadOptions()
  }
})

watch(() => props.oportunidade, (newOportunidade) => {
  if (newOportunidade) {
    isEdit.value = true
    form.value = { ...newOportunidade }
  } else {
    isEdit.value = false
    resetForm()
  }
}, { immediate: true })

async function loadOptions() {
  try {
    const [contasRes, contatosRes, estagiosRes] = await Promise.all([
      api.get('/contas/'),
      api.get('/contatos/'),
      api.get('/estagios-funil/')
    ])
    contas.value = contasRes.data.results || contasRes.data
    contatos.value = contatosRes.data.results || contatosRes.data
    estagios.value = estagiosRes.data.results || estagiosRes.data
  } catch (error) {
    console.error('Erro ao carregar opções:', error)
  }
}

function resetForm() {
  form.value = {
    nome: '',
    conta: '',
    contato_principal: '',
    estagio: '',
    valor_estimado: 0,
    data_fechamento_esperada: '',
    probabilidade: 0,
    descricao: ''
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
      await api.put(`/oportunidades/${form.value.id}/`, data)
    } else {
      await api.post('/oportunidades/', data)
    }
    emit('saved')
    emit('close')
    resetForm()
  } catch (error) {
    console.error('Erro ao salvar oportunidade:', error)
    const errorMsg = error.response?.data?.detail || 
                     JSON.stringify(error.response?.data) || 
                     error.message
    alert('Erro ao salvar oportunidade: ' + errorMsg)
  } finally {
    loading.value = false
  }
}
</script>
