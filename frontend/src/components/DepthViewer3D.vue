<script setup>
import { ref, onMounted, onBeforeUnmount, watch } from 'vue'
import * as THREE from 'three'
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js'

const props = defineProps({
  depthMapUrl: {
    type: String,
    required: true
  },
  originalImageUrl: {
    type: String,
    required: true
  }
})

const containerRef = ref(null)
const isLoading = ref(true)

let scene, camera, renderer, controls, mesh
let animationId = null

const init = async () => {
  if (!containerRef.value) return
  
  isLoading.value = true
  
  // Créer la scène
  scene = new THREE.Scene()
  scene.background = new THREE.Color(0x000000)
  
  // Créer la caméra
  camera = new THREE.PerspectiveCamera(
    50,
    containerRef.value.clientWidth / containerRef.value.clientHeight,
    0.1,
    1000
  )
  camera.position.z = 5
  
  // Créer le renderer
  renderer = new THREE.WebGLRenderer({ antialias: true })
  renderer.setSize(containerRef.value.clientWidth, containerRef.value.clientHeight)
  renderer.setPixelRatio(window.devicePixelRatio)
  containerRef.value.appendChild(renderer.domElement)
  
  // Créer les contrôles orbitaux
  controls = new OrbitControls(camera, renderer.domElement)
  controls.enableDamping = true
  controls.dampingFactor = 0.05
  controls.autoRotate = true
  controls.autoRotateSpeed = 2
  controls.enableZoom = true
  controls.enablePan = true
  
  // Lumières
  const ambientLight = new THREE.AmbientLight(0xffffff, 0.6)
  scene.add(ambientLight)
  
  const directionalLight1 = new THREE.DirectionalLight(0xffffff, 0.8)
  directionalLight1.position.set(5, 5, 5)
  scene.add(directionalLight1)
  
  const directionalLight2 = new THREE.DirectionalLight(0xffffff, 0.4)
  directionalLight2.position.set(-5, -5, -5)
  scene.add(directionalLight2)
  
  const pointLight = new THREE.PointLight(0x8b5cf6, 0.5)
  pointLight.position.set(0, 0, 3)
  scene.add(pointLight)
  
  // Charger les textures
  const textureLoader = new THREE.TextureLoader()
  
  try {
    const [imageTexture, depthTexture] = await Promise.all([
      new Promise((resolve, reject) => {
        textureLoader.load(props.originalImageUrl, resolve, undefined, reject)
      }),
      new Promise((resolve, reject) => {
        textureLoader.load(props.depthMapUrl, resolve, undefined, reject)
      })
    ])
    
    // Créer le mesh avec displacement map
    const geometry = new THREE.PlaneGeometry(4, 3, 256, 256)
    const material = new THREE.MeshStandardMaterial({
      map: imageTexture,
      displacementMap: depthTexture,
      displacementScale: 0.8,
      roughness: 0.7,
      metalness: 0.2
    })
    
    mesh = new THREE.Mesh(geometry, material)
    scene.add(mesh)
    
    isLoading.value = false
    
    // Démarrer l'animation
    animate()
  } catch (error) {
    console.error('Erreur lors du chargement des textures:', error)
    isLoading.value = false
  }
}

const animate = () => {
  animationId = requestAnimationFrame(animate)
  
  if (controls) {
    controls.update()
  }
  
  if (renderer && scene && camera) {
    renderer.render(scene, camera)
  }
}

const handleResize = () => {
  if (!containerRef.value || !camera || !renderer) return
  
  camera.aspect = containerRef.value.clientWidth / containerRef.value.clientHeight
  camera.updateProjectionMatrix()
  renderer.setSize(containerRef.value.clientWidth, containerRef.value.clientHeight)
}

const cleanup = () => {
  if (animationId) {
    cancelAnimationFrame(animationId)
  }
  
  if (controls) {
    controls.dispose()
  }
  
  if (renderer) {
    renderer.dispose()
    if (containerRef.value && renderer.domElement) {
      containerRef.value.removeChild(renderer.domElement)
    }
  }
  
  if (mesh) {
    mesh.geometry.dispose()
    mesh.material.dispose()
  }
  
  window.removeEventListener('resize', handleResize)
}

onMounted(() => {
  init()
  window.addEventListener('resize', handleResize)
})

onBeforeUnmount(() => {
  cleanup()
})

// Recharger si les URLs changent
watch(() => [props.depthMapUrl, props.originalImageUrl], () => {
  cleanup()
  init()
})
</script>

<template>
  <div class="w-full h-[500px] rounded-xl overflow-hidden bg-black relative border border-purple-500/30">
    <!-- Loader -->
    <div v-if="isLoading" class="absolute inset-0 flex items-center justify-center bg-slate-900/90 z-10">
      <div class="text-center">
        <div class="inline-block animate-spin rounded-full h-12 w-12 border-4 border-purple-500 border-t-transparent mb-4"></div>
        <p class="text-gray-400">Chargement de la scène 3D...</p>
      </div>
    </div>

    <!-- Container pour Three.js -->
    <div ref="containerRef" class="w-full h-full"></div>

    <!-- Instructions -->
    <div class="absolute bottom-4 left-4 right-4 bg-black/80 backdrop-blur-sm px-4 py-3 rounded-lg">
      <div class="flex items-center justify-between text-sm flex-wrap gap-2">
        <div class="flex gap-4 text-gray-300 flex-wrap">
          <span>🖱️ <strong>Rotation</strong> : Clic gauche + glisser</span>
          <span>🔍 <strong>Zoom</strong> : Molette</span>
          <span>↔️ <strong>Déplacement</strong> : Clic droit + glisser</span>
        </div>
        <div class="text-purple-400 font-semibold animate-pulse">
          ↻ Rotation automatique
        </div>
      </div>
    </div>
  </div>
</template>
