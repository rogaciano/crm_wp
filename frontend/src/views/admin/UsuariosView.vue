<template>
  <div>
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-3xl font-bold text-gray-900">Gestão de Usuários</h1>
      <button class="btn btn-primary">+ Novo Usuário</button>
    </div>

    <div class="card overflow-hidden">
      <table class="table">
        <thead class="bg-gray-50">
          <tr>
            <th class="table-header">Nome</th>
            <th class="table-header">Email</th>
            <th class="table-header">Perfil</th>
            <th class="table-header">Canal</th>
            <th class="table-header">Status</th>
            <th class="table-header">Ações</th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-for="usuario in usuarios" :key="usuario.id" class="hover:bg-gray-50">
            <td class="table-cell font-medium">
              {{ usuario.first_name }} {{ usuario.last_name }}
            </td>
            <td class="table-cell">{{ usuario.email }}</td>
            <td class="table-cell">
              <span :class="getPerfilClass(usuario.perfil)">
                {{ getPerfilLabel(usuario.perfil) }}
              </span>
            </td>
            <td class="table-cell">{{ usuario.canal_nome || 'N/A' }}</td>
            <td class="table-cell">
              <span :class="usuario.is_active ? 'text-green-600' : 'text-red-600'">
                {{ usuario.is_active ? 'Ativo' : 'Inativo' }}
              </span>
            </td>
            <td class="table-cell">
              <button class="text-primary-600 hover:text-primary-700 mr-2">Editar</button>
              <button class="text-red-600 hover:text-red-700">Desativar</button>
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

const usuarios = ref([])

onMounted(() => {
  loadUsuarios()
})

async function loadUsuarios() {
  try {
    const response = await api.get('/usuarios/')
    usuarios.value = response.data.results || response.data
  } catch (error) {
    console.error('Erro ao carregar usuários:', error)
  }
}

function getPerfilLabel(perfil) {
  const labels = {
    'ADMIN': 'Administrador',
    'RESPONSAVEL': 'Responsável',
    'VENDEDOR': 'Vendedor'
  }
  return labels[perfil] || perfil
}

function getPerfilClass(perfil) {
  const classes = {
    'ADMIN': 'px-2 py-1 text-xs rounded-full bg-red-100 text-red-800',
    'RESPONSAVEL': 'px-2 py-1 text-xs rounded-full bg-purple-100 text-purple-800',
    'VENDEDOR': 'px-2 py-1 text-xs rounded-full bg-blue-100 text-blue-800'
  }
  return classes[perfil] || 'px-2 py-1 text-xs rounded-full bg-gray-100 text-gray-800'
}
</script>
