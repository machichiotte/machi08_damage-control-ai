<template>
  <div class="claim-evaluator">
    <h2>🔍 Évaluation du Sinistre</h2>

    <!-- Sélection des fichiers -->
    <div v-if="!evaluation" class="file-selection">
      <div class="selection-card">
        <h3>📸 Image du sinistre</h3>
        <input v-model="imageFilename" type="text" placeholder="Ex: image_abc123.jpg" class="file-input" />
        <p class="hint">Nom du fichier image uploadé</p>
      </div>

      <div class="selection-card">
        <h3>📄 Contrat d'assurance</h3>
        <input v-model="contractFilename" type="text" placeholder="Ex: contract_xyz789.pdf" class="file-input" />
        <p class="hint">Nom du fichier contrat uploadé</p>
      </div>

      <div class="selection-card">
        <h3>⚠️ Type de sinistre</h3>
        <select v-model="damageType" class="damage-type-select">
          <option value="accident">Accident / Collision</option>
          <option value="vol">Vol</option>
          <option value="incendie">Incendie</option>
          <option value="bris_glace">Bris de glace</option>
          <option value="vandalisme">Vandalisme</option>
        </select>
      </div>

      <button @click="evaluateClaim" :disabled="!imageFilename || !contractFilename || isEvaluating"
        class="evaluate-btn">
        {{ isEvaluating ? '⏳ Évaluation en cours...' : '🔍 Évaluer le sinistre' }}
      </button>
    </div>

    <!-- Loader -->
    <div v-if="isEvaluating" class="loader">
      <div class="spinner"></div>
      <p>Analyse en cours...</p>
      <p class="sub">Croisement des données visuelles et contractuelles</p>
    </div>

    <!-- Résultat de l'évaluation -->
    <div v-if="evaluation" class="evaluation-result">
      <!-- Décision principale -->
      <div class="decision-banner" :class="{ covered: evaluation.decision.covered }">
        <div class="decision-icon">
          {{ evaluation.decision.covered ? '✅' : '❌' }}
        </div>
        <div class="decision-content">
          <h3>{{ evaluation.decision.covered ? 'SINISTRE COUVERT' : 'SINISTRE NON COUVERT' }}</h3>
          <p class="reason">{{ evaluation.decision.reason }}</p>
        </div>
      </div>

      <!-- Détails financiers -->
      <div class="financial-details">
        <h3>💰 Détails financiers</h3>
        <div class="cost-grid">
          <div class="cost-item">
            <span class="label">Coût estimé des dégâts</span>
            <span class="value">{{ formatCurrency(evaluation.costs.estimated_damage) }}</span>
          </div>
          <div class="cost-item">
            <span class="label">Franchise</span>
            <span class="value">{{ formatCurrency(evaluation.costs.franchise) }}</span>
          </div>
          <div class="cost-item">
            <span class="label">Plafond de garantie</span>
            <span class="value">{{ formatCurrency(evaluation.costs.plafond) }}</span>
          </div>
          <div class="cost-item highlight">
            <span class="label">Remboursement</span>
            <span class="value">{{ formatCurrency(evaluation.costs.reimbursement) }}</span>
          </div>
          <div class="cost-item">
            <span class="label">Reste à charge</span>
            <span class="value">{{ formatCurrency(evaluation.costs.out_of_pocket) }}</span>
          </div>
        </div>
      </div>

      <!-- Couverture -->
      <div class="coverage-details">
        <h3>🛡️ Couverture</h3>
        <div class="coverage-info">
          <div class="info-item">
            <span class="label">Type de sinistre</span>
            <span class="badge">{{ formatDamageType(evaluation.coverage.damage_type) }}</span>
          </div>
          <div class="info-item">
            <span class="label">Garanties applicables</span>
            <div class="garanties-list">
              <span v-for="garantie in evaluation.coverage.garanties_applicables" :key="garantie"
                class="garantie-badge">
                {{ formatGarantieName(garantie) }}
              </span>
              <span v-if="evaluation.coverage.garanties_applicables.length === 0" class="no-garantie">
                Aucune garantie applicable
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- Dégâts détectés -->
      <div class="damages-details">
        <h3>🔧 Dégâts détectés</h3>
        <div class="severity-badge" :class="evaluation.damages.severity">
          {{ formatSeverity(evaluation.damages.severity) }}
        </div>

        <div v-if="evaluation.damages.breakdown.length > 0" class="breakdown-table">
          <table>
            <thead>
              <tr>
                <th>Pièce</th>
                <th>Confiance</th>
                <th>Coût de base</th>
                <th>Coût estimé</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in evaluation.damages.breakdown" :key="item.part">
                <td>{{ item.part }}</td>
                <td>{{ item.confidence }}%</td>
                <td>{{ formatCurrency(item.base_cost) }}</td>
                <td class="estimated">{{ formatCurrency(item.estimated_cost) }}</td>
              </tr>
            </tbody>
          </table>
        </div>
        <p v-else class="no-parts">Aucune pièce spécifique détectée (estimation basée sur la profondeur)</p>
      </div>

      <!-- Actions -->
      <div class="actions">
        <button @click="reset" class="secondary-btn">
          🔄 Nouvelle évaluation
        </button>
        <button @click="downloadReport" class="primary-btn">
          📥 Télécharger le rapport
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
import { API_URL } from '../config.js'

const imageFilename = ref('')
const contractFilename = ref('')
const damageType = ref('accident')
const isEvaluating = ref(false)
const evaluation = ref(null)
const error = ref(null)

const formatCurrency = (amount) => {
  return new Intl.NumberFormat('fr-FR', {
    style: 'currency',
    currency: 'EUR'
  }).format(amount)
}

const formatDamageType = (type) => {
  const types = {
    accident: 'Accident / Collision',
    vol: 'Vol',
    incendie: 'Incendie',
    bris_glace: 'Bris de glace',
    vandalisme: 'Vandalisme'
  }
  return types[type] || type
}

const formatGarantieName = (key) => {
  const names = {
    tous_risques: 'Tous risques',
    tiers: 'Responsabilité civile',
    vol: 'Vol',
    incendie: 'Incendie',
    bris_de_glace: 'Bris de glace',
    assistance: 'Assistance'
  }
  return names[key] || key
}

const formatSeverity = (severity) => {
  const severities = {
    minor: '🟢 Dégâts mineurs',
    moderate: '🟡 Dégâts modérés',
    severe: '🔴 Dégâts importants'
  }
  return severities[severity] || severity
}

const evaluateClaim = async () => {
  if (!imageFilename.value || !contractFilename.value) return

  isEvaluating.value = true
  error.value = null

  try {
    const response = await fetch(
      `${API_URL}/evaluate/claim?image_filename=${encodeURIComponent(imageFilename.value)}&contract_filename=${encodeURIComponent(contractFilename.value)}&damage_type=${damageType.value}`,
      { method: 'POST' }
    )

    if (!response.ok) {
      const errorData = await response.json()
      throw new Error(errorData.detail || 'Erreur lors de l\'évaluation')
    }

    const data = await response.json()
    evaluation.value = data.evaluation
  } catch (err) {
    error.value = err.message
  } finally {
    isEvaluating.value = false
  }
}

const reset = () => {
  evaluation.value = null
  error.value = null
  imageFilename.value = ''
  contractFilename.value = ''
  damageType.value = 'accident'
}

const downloadReport = () => {
  const report = JSON.stringify(evaluation.value, null, 2)
  const blob = new Blob([report], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `rapport-sinistre-${Date.now()}.json`
  a.click()
  URL.revokeObjectURL(url)
}
</script>

<style scoped>
.claim-evaluator {
  max-width: 1200px;
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

.file-selection {
  display: grid;
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.selection-card {
  background: white;
  border-radius: 16px;
  padding: 1.5rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
}

.selection-card h3 {
  font-size: 1.125rem;
  font-weight: 600;
  color: #2d3748;
  margin-bottom: 1rem;
}

.file-input,
.damage-type-select {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.2s;
  color: #2d3748;
  background: white;
}

.file-input::placeholder {
  color: #a0aec0;
}

.file-input:focus,
.damage-type-select:focus {
  outline: none;
  border-color: #667eea;
}

.hint {
  margin-top: 0.5rem;
  font-size: 0.875rem;
  color: #718096;
}

.evaluate-btn {
  width: 100%;
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

.evaluate-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(72, 187, 120, 0.3);
}

.evaluate-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
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

.evaluation-result {
  display: grid;
  gap: 1.5rem;
}

.decision-banner {
  background: linear-gradient(135deg, #fc8181 0%, #f56565 100%);
  border-radius: 16px;
  padding: 2rem;
  display: flex;
  align-items: center;
  gap: 1.5rem;
  color: white;
  box-shadow: 0 8px 16px rgba(245, 101, 101, 0.3);
}

.decision-banner.covered {
  background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
  box-shadow: 0 8px 16px rgba(72, 187, 120, 0.3);
}

.decision-icon {
  font-size: 4rem;
}

.decision-content h3 {
  font-size: 1.75rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
}

.decision-content .reason {
  font-size: 1rem;
  opacity: 0.9;
}

.financial-details,
.coverage-details,
.damages-details {
  background: white;
  border-radius: 16px;
  padding: 1.5rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
}

.financial-details h3,
.coverage-details h3,
.damages-details h3 {
  font-size: 1.25rem;
  font-weight: 600;
  color: #2d3748;
  margin-bottom: 1rem;
}

.cost-grid {
  display: grid;
  gap: 1rem;
}

.cost-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem;
  background: #f7fafc;
  border-radius: 8px;
}

.cost-item.highlight {
  background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
  border: 2px solid #667eea;
}

.cost-item .label {
  font-weight: 500;
  color: #4a5568;
}

.cost-item .value {
  font-size: 1.25rem;
  font-weight: 700;
  color: #2d3748;
}

.coverage-info {
  display: grid;
  gap: 1rem;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.info-item .label {
  font-weight: 500;
  color: #4a5568;
  font-size: 0.875rem;
}

.badge {
  display: inline-block;
  padding: 0.5rem 1rem;
  background: #667eea;
  color: white;
  border-radius: 8px;
  font-weight: 600;
  font-size: 0.875rem;
}

.garanties-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.garantie-badge {
  padding: 0.5rem 1rem;
  background: #48bb78;
  color: white;
  border-radius: 8px;
  font-size: 0.875rem;
  font-weight: 500;
}

.no-garantie {
  color: #e53e3e;
  font-style: italic;
}

.severity-badge {
  display: inline-block;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  font-weight: 600;
  margin-bottom: 1rem;
}

.severity-badge.minor {
  background: #c6f6d5;
  color: #22543d;
}

.severity-badge.moderate {
  background: #fef3c7;
  color: #78350f;
}

.severity-badge.severe {
  background: #fed7d7;
  color: #742a2a;
}

.breakdown-table {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
}

thead {
  background: #f7fafc;
}

th {
  padding: 0.75rem;
  text-align: left;
  font-weight: 600;
  color: #4a5568;
  font-size: 0.875rem;
}

td {
  padding: 0.75rem;
  border-top: 1px solid #e2e8f0;
  color: #2d3748;
}

td.estimated {
  font-weight: 700;
  color: #667eea;
}

.no-parts {
  color: #718096;
  font-style: italic;
}

.actions {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
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
