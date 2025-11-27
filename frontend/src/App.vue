<script setup>
import { ref } from 'vue'
import ImageUploader from './components/ImageUploader.vue'
import ContractUploader from './components/ContractUploader.vue'

const activeTab = ref('image')
</script>

<template>
  <div class="min-h-screen flex flex-col items-center justify-center p-8">
    <!-- Header -->
    <div class="text-center mb-12">
      <h1
        class="text-6xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 via-purple-400 to-emerald-400 mb-4 animate-gradient">
        DamageControl AI
      </h1>
      <p class="text-xl text-gray-400">L'Expert en Sinistres Automatisé</p>
      <div class="flex gap-4 justify-center mt-4 text-sm text-gray-500">
        <span class="flex items-center gap-2">
          <span class="w-2 h-2 bg-green-500 rounded-full animate-pulse"></span>
          Backend connecté
        </span>
      </div>
    </div>

    <!-- Tabs -->
    <div class="flex gap-4 mb-8">
      <button @click="activeTab = 'image'" :class="[
        'px-6 py-3 rounded-xl font-semibold transition-all',
        activeTab === 'image'
          ? 'bg-gradient-to-r from-blue-500 to-purple-500 text-white shadow-lg'
          : 'bg-slate-800/50 text-gray-400 hover:bg-slate-700/50'
      ]">
        📸 Analyser une photo
      </button>
      <button @click="activeTab = 'contract'" :class="[
        'px-6 py-3 rounded-xl font-semibold transition-all',
        activeTab === 'contract'
          ? 'bg-gradient-to-r from-purple-500 to-emerald-500 text-white shadow-lg'
          : 'bg-slate-800/50 text-gray-400 hover:bg-slate-700/50'
      ]">
        📄 Analyser un contrat
      </button>
    </div>

    <!-- Main Content -->
    <ImageUploader v-if="activeTab === 'image'" />
    <ContractUploader v-if="activeTab === 'contract'" />

    <!-- Info Cards -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 w-full max-w-4xl mt-12">
      <div
        class="bg-slate-800/50 backdrop-blur-sm p-6 rounded-xl border border-slate-700/50 hover:border-blue-500/50 transition-all">
        <div class="text-3xl mb-3">🎯</div>
        <h3 class="font-semibold mb-2">Depth Estimation</h3>
        <p class="text-sm text-gray-400">Analyse 3D de la gravité des impacts</p>
      </div>

      <div
        class="bg-slate-800/50 backdrop-blur-sm p-6 rounded-xl border border-slate-700/50 hover:border-purple-500/50 transition-all">
        <div class="text-3xl mb-3">🔍</div>
        <h3 class="font-semibold mb-2">Détection IA</h3>
        <p class="text-sm text-gray-400">Identification des pièces endommagées</p>
      </div>

      <div
        class="bg-slate-800/50 backdrop-blur-sm p-6 rounded-xl border border-slate-700/50 hover:border-emerald-500/50 transition-all">
        <div class="text-3xl mb-3">📄</div>
        <h3 class="font-semibold mb-2">Analyse Contrat</h3>
        <p class="text-sm text-gray-400">Extraction des garanties et franchises</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
@keyframes gradient {

  0%,
  100% {
    background-position: 0% 50%;
  }

  50% {
    background-position: 100% 50%;
  }
}

.animate-gradient {
  background-size: 200% 200%;
  animation: gradient 3s ease infinite;
}
</style>
