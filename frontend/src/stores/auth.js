import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/services/api'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const accessToken = ref(localStorage.getItem('access_token'))
  const refreshToken = ref(localStorage.getItem('refresh_token'))

  const isAuthenticated = computed(() => !!accessToken.value)
  const isAdmin = computed(() => user.value?.perfil === 'ADMIN')
  const isResponsavel = computed(() => user.value?.perfil === 'RESPONSAVEL')
  const isVendedor = computed(() => user.value?.perfil === 'VENDEDOR')

  async function login(username, password) {
    try {
      console.log('🔐 Tentando fazer login...', { username })
      // Usando o serviço api centralizado
      const response = await api.post('/auth/login/', {
        username,
        password
      })

      console.log('✅ Login bem-sucedido, tokens recebidos')
      accessToken.value = response.data.access
      refreshToken.value = response.data.refresh

      localStorage.setItem('access_token', response.data.access)
      localStorage.setItem('refresh_token', response.data.refresh)

      console.log('📡 Buscando dados do usuário...')
      await fetchUser()
      console.log('✅ Dados do usuário carregados:', user.value)
      return true
    } catch (error) {
      console.error('❌ Login failed:', error)
      console.error('Error details:', error.response?.data)
      throw error
    }
  }

  async function fetchUser() {
    try {
      console.log('📡 fetchUser: Fazendo requisição para /usuarios/me/')
      const response = await api.get('/usuarios/me/')
      console.log('📡 fetchUser: Resposta recebida:', response.data)
      user.value = response.data
    } catch (error) {
      console.error('❌ Failed to fetch user:', error)
      console.error('❌ Error response:', error.response?.data)
      console.error('❌ Error status:', error.response?.status)
      if (error.response?.status === 401) {
        logout()
      }
      throw error
    }
  }

  function logout() {
    user.value = null
    accessToken.value = null
    refreshToken.value = null
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
  }

  return {
    user,
    accessToken,
    isAuthenticated,
    isAdmin,
    isResponsavel,
    isVendedor,
    login,
    fetchUser,
    logout
  }
})
