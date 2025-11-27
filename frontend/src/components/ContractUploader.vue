<template>
    <div class="contract-uploader">
        <h2>📄 Analyse de Contrat d'Assurance</h2>

        <!-- Zone de drop -->
        <div class="drop-zone" :class="{ 'drag-over': isDragging, 'has-file': contractFile }" @drop.prevent="handleDrop"
            @dragover.prevent="isDragging = true" @dragleave.prevent="isDragging = false">
            <input ref="fileInput" type="file" accept=".pdf,image/*" @change="handleFileSelect" style="display: none" />

            <div v-if="!contractFile" class="drop-zone-content">
                <div class="icon">📑</div>
                <p class="title">Glissez votre contrat ici</p>
                <p class="subtitle">ou</p>
                <button @click="$refs.fileInput.click()" class="upload-btn">
                    Parcourir les fichiers
                </button>
                <p class="formats">PDF, JPG, PNG acceptés</p>
            </div>

            <div v-else class="file-info">
                <div class="file-icon">📄</div>
                <div class="file-details">
                    <p class="file-name">{{ contractFile.name }}</p>
                    <p class="file-size">{{ formatFileSize(contractFile.size) }}</p>
                </div>
                <button @click="removeFile" class="remove-btn">✕</button>
            </div>
        </div>

        <!-- Bouton d'analyse -->
        <button v-if="contractFile && !isAnalyzing && !analysisResult" @click="analyzeContract" class="analyze-btn">
            🔍 Analyser le contrat
        </button>

        <!-- Loader -->
        <div v-if="isAnalyzing" class="loader">
            <div class="spinner"></div>
            <p>Analyse en cours...</p>
            <p class="sub">Extraction du texte et analyse des garanties</p>
        </div>

        <!-- Résultats de l'analyse -->
        <div v-if="analysisResult" class="analysis-results">
            <h3>✅ Analyse terminée</h3>

            <!-- Franchise -->
            <div class="result-card">
                <div class="card-header">
                    <span class="icon">💰</span>
                    <h4>Franchise</h4>
                </div>
                <div class="card-content">
                    <div v-if="analysisResult.analysis.franchise.found" class="value-found">
                        <p class="amount">{{ analysisResult.analysis.franchise.amount }} €</p>
                        <p class="label">Montant de la franchise</p>
                    </div>
                    <div v-else class="value-not-found">
                        <p>❌ Franchise non trouvée dans le contrat</p>
                    </div>
                </div>
            </div>

            <!-- Plafond -->
            <div class="result-card">
                <div class="card-header">
                    <span class="icon">📊</span>
                    <h4>Plafond de garantie</h4>
                </div>
                <div class="card-content">
                    <div v-if="analysisResult.analysis.plafond.found" class="value-found">
                        <p class="amount">{{ formatAmount(analysisResult.analysis.plafond.amount) }} €</p>
                        <p class="label">Limite de couverture</p>
                    </div>
                    <div v-else class="value-not-found">
                        <p>❌ Plafond non trouvé dans le contrat</p>
                    </div>
                </div>
            </div>

            <!-- Garanties -->
            <div class="result-card garanties-card">
                <div class="card-header">
                    <span class="icon">🛡️</span>
                    <h4>Garanties souscrites</h4>
                </div>
                <div class="card-content">
                    <div class="garanties-summary">
                        <p class="count">{{ analysisResult.analysis.summary.garanties_count }} garanties détectées</p>
                    </div>
                    <div class="garanties-list">
                        <div v-for="(value, key) in analysisResult.analysis.garanties" :key="key" class="garantie-item"
                            :class="{ active: value }">
                            <span class="check">{{ value ? '✅' : '❌' }}</span>
                            <span class="name">{{ formatGarantieName(key) }}</span>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Actions -->
            <div class="actions">
                <button @click="reset" class="secondary-btn">
                    🔄 Analyser un autre contrat
                </button>
                <button @click="proceedToComparison" class="primary-btn">
                    ➡️ Comparer avec les dégâts
                </button>
            </div>
        </div>

        <!-- Erreur -->
        <div v-if="error" class="error-message">
            <span class="icon">⚠️</span>
            <p>{{ error }}</p>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'

const isDragging = ref(false)
const contractFile = ref(null)
const isAnalyzing = ref(false)
const analysisResult = ref(null)
const error = ref(null)
const fileInput = ref(null)

const handleDrop = (e) => {
    isDragging.value = false
    const files = e.dataTransfer.files
    if (files.length > 0) {
        contractFile.value = files[0]
        error.value = null
    }
}

const handleFileSelect = (e) => {
    const files = e.target.files
    if (files.length > 0) {
        contractFile.value = files[0]
        error.value = null
    }
}

const removeFile = () => {
    contractFile.value = null
    analysisResult.value = null
    error.value = null
    if (fileInput.value) {
        fileInput.value.value = ''
    }
}

const formatFileSize = (bytes) => {
    if (bytes < 1024) return bytes + ' B'
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB'
    return (bytes / (1024 * 1024)).toFixed(1) + ' MB'
}

const formatAmount = (amount) => {
    return new Intl.NumberFormat('fr-FR').format(amount)
}

const formatGarantieName = (key) => {
    const names = {
        tous_risques: 'Tous risques',
        tiers: 'Responsabilité civile (Tiers)',
        vol: 'Vol',
        incendie: 'Incendie',
        bris_de_glace: 'Bris de glace',
        assistance: 'Assistance'
    }
    return names[key] || key
}

const analyzeContract = async () => {
    if (!contractFile.value) return

    isAnalyzing.value = true
    error.value = null

    try {
        // 1. Upload du contrat
        const formData = new FormData()
        formData.append('file', contractFile.value)

        const uploadResponse = await fetch('http://127.0.0.1:8000/upload/contract', {
            method: 'POST',
            body: formData
        })

        if (!uploadResponse.ok) {
            throw new Error('Erreur lors de l\'upload du contrat')
        }

        const uploadData = await uploadResponse.json()

        // 2. Analyse du contrat
        const analyzeResponse = await fetch(
            `http://127.0.0.1:8000/analyze/contract/${uploadData.filename}`,
            { method: 'POST' }
        )

        if (!analyzeResponse.ok) {
            throw new Error('Erreur lors de l\'analyse du contrat')
        }

        analysisResult.value = await analyzeResponse.json()
    } catch (err) {
        error.value = err.message
    } finally {
        isAnalyzing.value = false
    }
}

const reset = () => {
    contractFile.value = null
    analysisResult.value = null
    error.value = null
    if (fileInput.value) {
        fileInput.value.value = ''
    }
}

const proceedToComparison = () => {
    // TODO: Navigation vers la comparaison avec les dégâts
    console.log('Procéder à la comparaison', analysisResult.value)
}
</script>

<style scoped>
.contract-uploader {
    max-width: 800px;
    margin: 0 auto;
    padding: 2rem;
}

h2 {
    font-size: 2rem;
    font-weight: 700;
    margin-bottom: 2rem;
    text-align: center;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.drop-zone {
    border: 3px dashed #cbd5e0;
    border-radius: 16px;
    padding: 3rem;
    text-align: center;
    transition: all 0.3s ease;
    background: #f7fafc;
    cursor: pointer;
}

.drop-zone.drag-over {
    border-color: #667eea;
    background: #edf2f7;
    transform: scale(1.02);
}

.drop-zone.has-file {
    border-color: #48bb78;
    background: #f0fff4;
}

.drop-zone-content .icon {
    font-size: 4rem;
    margin-bottom: 1rem;
}

.drop-zone-content .title {
    font-size: 1.25rem;
    font-weight: 600;
    color: #2d3748;
    margin-bottom: 0.5rem;
}

.drop-zone-content .subtitle {
    color: #718096;
    margin-bottom: 1rem;
}

.upload-btn {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    padding: 0.75rem 2rem;
    border-radius: 8px;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: transform 0.2s;
}

.upload-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.formats {
    margin-top: 1rem;
    font-size: 0.875rem;
    color: #a0aec0;
}

.file-info {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 1rem;
    background: white;
    border-radius: 12px;
}

.file-icon {
    font-size: 2.5rem;
}

.file-details {
    flex: 1;
    text-align: left;
}

.file-name {
    font-weight: 600;
    color: #2d3748;
    margin-bottom: 0.25rem;
}

.file-size {
    font-size: 0.875rem;
    color: #718096;
}

.remove-btn {
    background: #fc8181;
    color: white;
    border: none;
    width: 32px;
    height: 32px;
    border-radius: 50%;
    cursor: pointer;
    font-size: 1.25rem;
    transition: all 0.2s;
}

.remove-btn:hover {
    background: #f56565;
    transform: scale(1.1);
}

.analyze-btn {
    width: 100%;
    margin-top: 1.5rem;
    background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
    color: white;
    border: none;
    padding: 1rem 2rem;
    border-radius: 12px;
    font-size: 1.125rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s;
}

.analyze-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 16px rgba(72, 187, 120, 0.3);
}

.loader {
    text-align: center;
    padding: 3rem;
}

.spinner {
    width: 60px;
    height: 60px;
    margin: 0 auto 1rem;
    border: 4px solid #e2e8f0;
    border-top-color: #667eea;
    border-radius: 50%;
    animation: spin 1s linear infinite;
}

@keyframes spin {
    to {
        transform: rotate(360deg);
    }
}

.loader p {
    font-size: 1.125rem;
    font-weight: 600;
    color: #2d3748;
    margin-bottom: 0.5rem;
}

.loader .sub {
    font-size: 0.875rem;
    color: #718096;
    font-weight: 400;
}

.analysis-results {
    margin-top: 2rem;
}

.analysis-results h3 {
    font-size: 1.5rem;
    font-weight: 700;
    color: #48bb78;
    margin-bottom: 1.5rem;
    text-align: center;
}

.result-card {
    background: white;
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    transition: transform 0.2s;
}

.result-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 12px rgba(0, 0, 0, 0.1);
}

.card-header {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 1rem;
}

.card-header .icon {
    font-size: 1.5rem;
}

.card-header h4 {
    font-size: 1.125rem;
    font-weight: 600;
    color: #2d3748;
}

.value-found .amount {
    font-size: 2rem;
    font-weight: 700;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.25rem;
}

.value-found .label {
    color: #718096;
    font-size: 0.875rem;
}

.value-not-found p {
    color: #e53e3e;
    font-weight: 500;
}

.garanties-summary {
    margin-bottom: 1rem;
    padding: 0.75rem;
    background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
    border-radius: 8px;
}

.garanties-summary .count {
    font-weight: 600;
    color: #667eea;
}

.garanties-list {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 0.75rem;
}

.garantie-item {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.75rem;
    background: #f7fafc;
    border-radius: 8px;
    transition: all 0.2s;
}

.garantie-item.active {
    background: #f0fff4;
    border: 1px solid #48bb78;
}

.garantie-item .check {
    font-size: 1.25rem;
}

.garantie-item .name {
    font-size: 0.875rem;
    font-weight: 500;
    color: #2d3748;
}

.actions {
    display: flex;
    gap: 1rem;
    margin-top: 2rem;
}

.secondary-btn,
.primary-btn {
    flex: 1;
    padding: 1rem 2rem;
    border-radius: 12px;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s;
    border: none;
}

.secondary-btn {
    background: #e2e8f0;
    color: #2d3748;
}

.secondary-btn:hover {
    background: #cbd5e0;
    transform: translateY(-2px);
}

.primary-btn {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
}

.primary-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 16px rgba(102, 126, 234, 0.3);
}

.error-message {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 1rem;
    background: #fff5f5;
    border: 1px solid #fc8181;
    border-radius: 12px;
    margin-top: 1rem;
}

.error-message .icon {
    font-size: 1.5rem;
}

.error-message p {
    color: #c53030;
    font-weight: 500;
}
</style>
