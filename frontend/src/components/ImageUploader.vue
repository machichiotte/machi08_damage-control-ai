<script setup>
import { ref } from 'vue'
import DepthViewer3D from './DepthViewer3D.vue'

const API_URL = 'http://127.0.0.1:8000'

const isDragging = ref(false)
const isUploading = ref(false)
const isAnalyzing = ref(false)
const isDetecting = ref(false)
const uploadedImage = ref(null)
const uploadResult = ref(null)
const analysisResult = ref(null)
const detectionResult = ref(null)
const errorMessage = ref(null)

const handleDragOver = (e) => {
  e.preventDefault()
  isDragging.value = true
}

const handleDragLeave = () => {
  isDragging.value = false
}

const handleDrop = (e) => {
  e.preventDefault()
  isDragging.value = false

  const files = e.dataTransfer.files
  if (files.length > 0) {
    handleFile(files[0])
  }
}

const handleFileInput = (e) => {
  const files = e.target.files
  if (files.length > 0) {
    handleFile(files[0])
  }
}

const handleFile = async (file) => {
  // Vérifier que c'est une image
  if (!file.type.startsWith('image/')) {
    errorMessage.value = 'Veuillez sélectionner une image'
    return
  }

  // Réinitialiser les états
  errorMessage.value = null
  uploadResult.value = null

  // Prévisualisation locale
  const reader = new FileReader()
  reader.onload = (e) => {
    uploadedImage.value = e.target.result
  }
  reader.readAsDataURL(file)

  // Upload vers le backend
  isUploading.value = true

  const formData = new FormData()
  formData.append('file', file)

  try {
    const response = await fetch(`${API_URL}/upload`, {
      method: 'POST',
      body: formData
    })

    if (!response.ok) {
      throw new Error('Erreur lors de l\'upload')
    }

    const data = await response.json()
    uploadResult.value = data
  } catch (error) {
    errorMessage.value = error.message
    uploadedImage.value = null
  } finally {
    isUploading.value = false
  }
}

const analyzeDepth = async () => {
  if (!uploadResult.value) return

  isAnalyzing.value = true
  errorMessage.value = null

  try {
    const response = await fetch(`${API_URL}/analyze/${uploadResult.value.filename}`, {
      method: 'POST'
    })

    if (!response.ok) {
      throw new Error('Erreur lors de l\'analyse')
    }

    const data = await response.json()
    analysisResult.value = data
  } catch (error) {
    errorMessage.value = error.message
  } finally {
    isAnalyzing.value = false
  }
}

const detectObjects = async () => {
  if (!uploadResult.value) return

  isDetecting.value = true
  errorMessage.value = null

  try {
    const response = await fetch(`${API_URL}/detect/${uploadResult.value.filename}`, {
      method: 'POST'
    })

    if (!response.ok) {
      throw new Error('Erreur lors de la détection')
    }

    const data = await response.json()
    detectionResult.value = data
  } catch (error) {
    errorMessage.value = error.message
  } finally {
    isDetecting.value = false
  }
}

const isDetectingParts = ref(false)
const partsResult = ref(null)

const detectParts = async () => {
  if (!uploadResult.value) return

  isDetectingParts.value = true
  errorMessage.value = null

  try {
    const response = await fetch(`${API_URL}/detect/parts/${uploadResult.value.filename}`, {
      method: 'POST'
    })

    if (!response.ok) {
      throw new Error('Erreur lors de la détection de pièces')
    }

    const data = await response.json()
    partsResult.value = data
  } catch (error) {
    errorMessage.value = error.message
  } finally {
    isDetectingParts.value = false
  }
}

const reset = () => {
  uploadedImage.value = null
  uploadResult.value = null
  analysisResult.value = null
  detectionResult.value = null
  partsResult.value = null
  errorMessage.value = null
}
</script>

<template>
  <div class="w-full max-w-2xl">
    <!-- Zone d'upload -->
    <div v-if="!uploadedImage" @dragover="handleDragOver" @dragleave="handleDragLeave" @drop="handleDrop" :class="[
      'border-2 border-dashed rounded-xl p-12 text-center transition-all duration-300 cursor-pointer',
      isDragging
        ? 'border-blue-500 bg-blue-500/10 scale-105'
        : 'border-slate-600 hover:border-blue-400 hover:bg-slate-800/50'
    ]">
      <input type="file" accept="image/*" @change="handleFileInput" class="hidden" id="file-input" />
      <label for="file-input" class="cursor-pointer">
        <div class="text-6xl mb-4">📸</div>
        <p class="text-xl font-semibold mb-2">
          {{ isDragging ? 'Déposez l\'image ici' : 'Glissez une photo ou cliquez' }}
        </p>
        <p class="text-sm text-gray-400">
          Formats acceptés : JPG, PNG, WEBP
        </p>
      </label>
    </div>

    <!-- Prévisualisation et résultat -->
    <div v-else class="space-y-6">
      <!-- Image uploadée -->
      <div class="relative rounded-xl overflow-hidden bg-slate-800 border border-slate-700">
        <img :src="uploadedImage" alt="Image uploadée" class="w-full h-auto" />
        <button @click="reset"
          class="absolute top-4 right-4 bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-lg transition-colors">
          ✕ Supprimer
        </button>
      </div>

      <!-- Loader -->
      <div v-if="isUploading" class="text-center py-8">
        <div class="inline-block animate-spin rounded-full h-12 w-12 border-4 border-blue-500 border-t-transparent">
        </div>
        <p class="mt-4 text-gray-400">Analyse en cours...</p>
      </div>

      <!-- Résultat Upload -->
      <div v-else-if="uploadResult" class="space-y-4">
        <div class="bg-slate-800 rounded-xl p-6 border border-slate-700">
          <h3 class="text-xl font-semibold mb-4 text-green-400">✓ Upload réussi</h3>
          <div class="space-y-2 text-sm mb-4">
            <div class="flex justify-between">
              <span class="text-gray-400">Nom du fichier :</span>
              <span class="font-mono text-xs">{{ uploadResult.filename }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-400">Taille :</span>
              <span>{{ (uploadResult.size / 1024).toFixed(2) }} KB</span>
            </div>
          </div>

          <!-- Actions -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <button v-if="!analysisResult" @click="analyzeDepth" :disabled="isAnalyzing"
              class="w-full bg-gradient-to-r from-blue-500 to-purple-500 hover:from-blue-600 hover:to-purple-600 disabled:from-gray-500 disabled:to-gray-600 text-white font-semibold py-3 px-6 rounded-lg transition-all transform hover:scale-105 disabled:scale-100 disabled:cursor-not-allowed">
              <span v-if="!isAnalyzing">🎯 Analyser la profondeur (3D)</span>
              <span v-else class="flex items-center justify-center gap-2">
                <span
                  class="inline-block animate-spin rounded-full h-4 w-4 border-2 border-white border-t-transparent"></span>
                Analyse en cours...
              </span>
            </button>

            <button v-if="!detectionResult" @click="detectObjects" :disabled="isDetecting"
              class="w-full bg-gradient-to-r from-orange-500 to-red-500 hover:from-orange-600 hover:to-red-600 disabled:from-gray-500 disabled:to-gray-600 text-white font-semibold py-3 px-6 rounded-lg transition-all transform hover:scale-105 disabled:scale-100 disabled:cursor-not-allowed">
              <span v-if="!isDetecting">🔍 Détecter les objets (YOLO)</span>
              <span v-else class="flex items-center justify-center gap-2">
                <span
                  class="inline-block animate-spin rounded-full h-4 w-4 border-2 border-white border-t-transparent"></span>
                Détection en cours...
              </span>
            </button>

            <button v-if="!partsResult" @click="detectParts" :disabled="isDetectingParts"
              class="w-full bg-gradient-to-r from-pink-500 to-rose-500 hover:from-pink-600 hover:to-rose-600 disabled:from-gray-500 disabled:to-gray-600 text-white font-semibold py-3 px-6 rounded-lg transition-all transform hover:scale-105 disabled:scale-100 disabled:cursor-not-allowed md:col-span-2">
              <span v-if="!isDetectingParts">🧩 Analyser les pièces (Zero-Shot)</span>
              <span v-else class="flex items-center justify-center gap-2">
                <span
                  class="inline-block animate-spin rounded-full h-4 w-4 border-2 border-white border-t-transparent"></span>
                Analyse OWL-ViT en cours...
              </span>
            </button>
          </div>
        </div>

        <!-- Résultat de l'analyse Depth -->
        <div v-if="analysisResult" class="bg-slate-800 rounded-xl p-6 border border-green-500/50">
          <h3 class="text-xl font-semibold mb-4 text-green-400">✓ Analyse Profondeur terminée</h3>

          <!-- Comparaison côte à côte -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
            <div>
              <p class="text-sm text-gray-400 mb-2">Image originale</p>
              <img :src="uploadedImage" alt="Original" class="w-full rounded-lg border border-slate-600" />
            </div>
            <div>
              <p class="text-sm text-gray-400 mb-2">Carte de profondeur 3D</p>
              <img :src="`${API_URL}${analysisResult.depth_map}`" alt="Depth Map"
                class="w-full rounded-lg border border-purple-500" />
            </div>
          </div>

          <!-- Statistiques -->
          <div class="bg-slate-900/50 rounded-lg p-4 space-y-2 text-sm">
            <div class="flex justify-between">
              <span class="text-gray-400">Profondeur moyenne :</span>
              <span class="font-mono">{{ analysisResult.stats.mean_depth.toFixed(2) }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-400">Profondeur min/max :</span>
              <span class="font-mono">{{ analysisResult.stats.min_depth.toFixed(2) }} / {{
                analysisResult.stats.max_depth.toFixed(2) }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-400">Appareil utilisé :</span>
              <span class="uppercase">{{ analysisResult.device_used }}</span>
            </div>
          </div>

          <!-- Visualisation 3D Interactive -->
          <div class="mt-6">
            <h4 class="text-lg font-semibold mb-3 text-purple-400">🧊 Visualisation 3D Interactive</h4>
            <DepthViewer3D :depthMapUrl="`${API_URL}${analysisResult.depth_map}`" :originalImageUrl="uploadedImage" />
          </div>
        </div>

        <!-- Résultat de la détection d'objets (YOLO) -->
        <div v-if="detectionResult" class="bg-slate-800 rounded-xl p-6 border border-orange-500/50">
          <h3 class="text-xl font-semibold mb-4 text-orange-400">✓ Détection d'objets terminée (YOLO)</h3>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
            <div>
              <p class="text-sm text-gray-400 mb-2">Image annotée</p>
              <img :src="`${API_URL}${detectionResult.annotated_image}`" alt="Annotated Image"
                class="w-full rounded-lg border border-orange-500" />
            </div>

            <!-- Liste des objets détectés -->
            <div class="bg-slate-900/50 rounded-lg p-4">
              <h4 class="text-sm font-semibold text-gray-300 mb-3">Objets détectés ({{
                detectionResult.stats.total_objects }})</h4>

              <div class="space-y-2 max-h-[300px] overflow-y-auto pr-2">
                <div v-for="(obj, index) in detectionResult.detections" :key="index"
                  class="flex justify-between items-center bg-slate-800 p-2 rounded border border-slate-700">
                  <span class="capitalize text-white">{{ obj.class }}</span>
                  <span class="text-xs font-mono text-orange-400">{{ (obj.confidence * 100).toFixed(1) }}%</span>
                </div>
              </div>

              <div class="mt-4 pt-4 border-t border-slate-700 text-xs text-gray-400">
                <p>Classes trouvées : {{ detectionResult.stats.classes_detected.join(', ') }}</p>
                <p class="mt-1">Confiance moyenne : {{ (detectionResult.stats.avg_confidence * 100).toFixed(1) }}%</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Résultat de la détection de pièces (OWL-ViT) -->
        <div v-if="partsResult" class="bg-slate-800 rounded-xl p-6 border border-pink-500/50">
          <h3 class="text-xl font-semibold mb-4 text-pink-400">✓ Analyse des pièces terminée (OWL-ViT)</h3>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
            <div>
              <p class="text-sm text-gray-400 mb-2">Image annotée</p>
              <img :src="`${API_URL}${partsResult.annotated_image}`" alt="Annotated Image"
                class="w-full rounded-lg border border-pink-500" />
            </div>

            <!-- Liste des pièces détectées -->
            <div class="bg-slate-900/50 rounded-lg p-4">
              <h4 class="text-sm font-semibold text-gray-300 mb-3">Pièces identifiées ({{
                partsResult.stats.total_objects }})</h4>

              <div class="space-y-2 max-h-[300px] overflow-y-auto pr-2">
                <div v-for="(obj, index) in partsResult.detections" :key="index"
                  class="flex justify-between items-center bg-slate-800 p-2 rounded border border-slate-700">
                  <span class="capitalize text-white">{{ obj.class }}</span>
                  <span class="text-xs font-mono text-pink-400">{{ (obj.confidence * 100).toFixed(1) }}%</span>
                </div>
              </div>

              <div class="mt-4 pt-4 border-t border-slate-700 text-xs text-gray-400">
                <p>Pièces trouvées : {{ partsResult.stats.classes_detected.join(', ') }}</p>
                <p class="mt-1">Confiance moyenne : {{ (partsResult.stats.avg_confidence * 100).toFixed(1) }}%</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Erreur -->
      <div v-else-if="errorMessage" class="bg-red-500/10 border border-red-500 rounded-xl p-6">
        <p class="text-red-400">❌ {{ errorMessage }}</p>
      </div>
    </div>
  </div>
</template>
