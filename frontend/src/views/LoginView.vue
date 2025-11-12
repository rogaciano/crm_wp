<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-primary-500 to-primary-700">
    <div class="bg-white p-8 rounded-xl shadow-2xl w-full max-w-md">
      <div class="text-center mb-8">
        <h1 class="text-3xl font-bold text-gray-900">CRM de Vendas</h1>
        <p class="text-gray-600 mt-2">Faça login para continuar</p>
      </div>

      <form @submit.prevent="handleLogin" class="space-y-6">
        <div>
          <label for="username" class="block text-sm font-medium text-gray-700 mb-2">
            Usuário
          </label>
          <input
            id="username"
            v-model="username"
            type="text"
            required
            class="input"
            placeholder="Digite seu usuário"
          />
        </div>

        <div>
          <label for="password" class="block text-sm font-medium text-gray-700 mb-2">
            Senha
          </label>
          <input
            id="password"
            v-model="password"
            type="password"
            required
            class="input"
            placeholder="Digite sua senha"
          />
        </div>

        <div v-if="error" class="bg-red-50 text-red-600 p-3 rounded-lg text-sm">
          {{ error }}
        </div>

        <button
          type="submit"
          :disabled="loading"
          class="w-full btn btn-primary py-3 text-lg"
        >
          <span v-if="!loading">Entrar</span>
          <span v-else>Entrando...</span>
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const username = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')

async function handleLogin() {
  loading.value = true
  error.value = ''

  try {
    console.log('🔐 LoginView: Iniciando login...')
    await authStore.login(username.value, password.value)
    console.log('✅ LoginView: Login bem-sucedido, redirecionando...')
    router.push('/')
  } catch (err) {
    console.error('❌ LoginView: Erro no login:', err)
    console.error('❌ LoginView: Erro detalhado:', err.response?.data)
    console.error('❌ LoginView: Status:', err.response?.status)
    error.value = err.response?.data?.detail || 'Usuário ou senha inválidos'
  } finally {
    loading.value = false
  }
}
</script>
