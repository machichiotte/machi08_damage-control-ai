<script setup>
</script>

<template>
  <div class="min-h-screen flex flex-col items-center justify-center p-4">
    <h1 class="text-5xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-emerald-400 mb-8">
      DamageControl AI
    </h1>
    <p class="text-xl text-gray-400 mb-8">L'Expert en Sinistres Automatisé</p>
    
    <div class="grid grid-cols-1 md:grid-cols-2 gap-8 w-full max-w-4xl">
        <div class="bg-slate-800 p-6 rounded-xl border border-slate-700">
            <h2 class="text-2xl font-semibold mb-4">📸 Upload</h2>
            <div class="border-2 border-dashed border-slate-600 rounded-lg h-64 flex items-center justify-center text-slate-500 hover:border-blue-500 hover:text-blue-500 transition-colors cursor-pointer">
                <span>Glisser une photo ou cliquer</span>
            </div>
        </div>
        
        <div class="bg-slate-800 p-6 rounded-xl border border-slate-700">
            <h2 class="text-2xl font-semibold mb-4">🧊 Analyse 3D</h2>
            <div class="bg-black rounded-lg h-64 flex items-center justify-center">
                <span class="text-sm text-gray-600">Vue 3D (TresJS) à venir...</span>
            </div>
        </div>
    </div>
  </div>
</template>
