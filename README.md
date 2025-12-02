# DamageControl AI - Automated Claims Expert

[![GitHub](https://img.shields.io/badge/GitHub-machichiotte%2Fdamage--control--ai-blue?logo=github)](https://github.com/machichiotte/damage-control-ai)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](./LICENSE)
[![Netlify Status](https://api.netlify.com/api/v1/badges/YOUR_SITE_ID/deploy-status)](https://app.netlify.com/sites/damage-control-ai/deploys)

## 🌐 Live Demo

🚀 **Application**: [https://damage-control-ai.netlify.app](https://damage-control-ai.netlify.app)  
📚 **API Documentation**: [https://machichiotte-damage-control-ai-backend.hf.space/docs](https://machichiotte-damage-control-ai-backend.hf.space/docs)

> 💡 **Infrastructure**: Frontend hosted on Netlify, Backend on Hugging Face Spaces (16 GB RAM).

## 🎯 Overview

DamageControl AI is a Progressive Web App that automates automotive damage assessment. Using artificial intelligence for image analysis (3D depth, object detection) and document processing (contract analysis), the application streamlines the claims declaration process.

## ✨ Current Features

### ✅ Implemented

1. **Interactive Image Upload** 📸

   - Drag & drop or file selection
   - Instant preview
   - Animated interface with transitions

2. **Depth Estimation (3D Vision)** 🎯

   - Impact severity analysis via depth maps
   - AI Model: Depth Anything (Hugging Face)
   - Side-by-side visualization (original vs depth map)
   - Depth statistics (min/max/average)
   - INFERNO colormap for better readability

3. **Interactive 3D Visualization** 🧊

   - 3D depth map display with TresJS
   - Automatic and manual rotation (OrbitControls)
   - Interactive zoom and pan
   - Displacement mapping for real 3D relief

4. **Object Detection (YOLO)** 🔍

   - Generic object detection (cars, people, trucks)
   - Model: YOLOv8 nano
   - Bounding boxes with confidence scores
   - Detection statistics

5. **Zero-Shot Object Detection (OWL-ViT)** 🧩

   - Specific part detection without training
   - Model: OWL-ViT (Google)
   - Detects: bumper, door, wheel, tire, headlight, hood, etc.
   - Customizable text queries

6. **Contract Analysis (NLP)** 📄

   - Insurance contract upload (PDF/Images)
   - Automatic text extraction (PyPDF2 + Tesseract OCR)
   - Regex analysis to detect:
     - Deductibles
     - Coverage limits
     - Coverage types (Theft, Fire, Glass breakage, etc.)
   - Dedicated interface with results visualization

7. **Business Logic (Claim Evaluation)** 🧠
   - `ClaimEvaluator` service to cross-reference visual and contractual analysis
   - Automatic cost estimation based on detected parts
   - Automatic decision: "Claim Covered: YES/NO"
   - Reimbursement calculation (estimated cost - deductible)
   - Complete interface with financial details and detected damages

### 🔄 In Progress (Sprint 4 - 50%)

8. **Polished UI/UX** 🎨
   - [x] Dark Mode design with Glassmorphism
   - [x] Loading animations during AI processing
   - [x] Tab system for navigation (Image / Contract)
   - [ ] Gallery of previous analyses
   - [ ] PWA (installable on mobile)
   - [ ] Performance optimizations

## 🛠 Tech Stack

- **Frontend**: Vue.js 3 (Vite) + TailwindCSS + TresJS
- **Backend**: Python (FastAPI)
- **AI/ML**: Hugging Face Transformers + Ultralytics
  - Depth Anything (depth estimation) ✅
  - YOLOv8 (object detection) ✅
  - OWL-ViT (zero-shot detection) ✅
- **Storage**: Local (files) for development
- **Deployment**: Netlify (frontend) + Hugging Face Spaces (backend)

## 📂 Project Structure

```
/damage_control_ai
├── /frontend          # Vue.js application
│   ├── /src
│   │   ├── /components
│   │   │   ├── ImageUploader.vue      # Upload component
│   │   │   ├── ContractUploader.vue   # Contract upload
│   │   │   ├── ClaimEvaluator.vue     # Claim evaluation
│   │   │   └── DepthViewer3D.vue      # 3D visualization
│   │   ├── App.vue
│   │   └── main.js
│   └── package.json
├── /backend           # FastAPI API
│   ├── main.py        # REST endpoints
│   ├── /services
│   │   ├── depth_estimator.py         # Depth Anything
│   │   ├── object_detector.py         # YOLO
│   │   ├── zero_shot_detector.py      # OWL-ViT
│   │   ├── contract_analyzer.py       # Contract analysis
│   │   └── claim_evaluator.py         # Claim evaluation
│   └── requirements.txt
└── /docs              # Documentation
    ├── ARCHITECTURE.md
    ├── SPRINTS.md
    └── SETUP.md
```

## 🏁 Quick Start

### Prerequisites

- Node.js 18+
- Python 3.9+
- ~4GB disk space (AI models)

### Installation

**Frontend:**

```bash
cd frontend
npm install
npm run dev
```

👉 Frontend accessible at http://localhost:5173

**Backend:**

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

👉 Backend accessible at http://127.0.0.1:8000

⚠️ **Note:** On first launch, AI models will be downloaded:

- Depth Anything (~400MB)
- YOLOv8 nano (~6MB)
- OWL-ViT (~600MB)

### API Documentation

Interactive Swagger documentation: http://127.0.0.1:8000/docs

## 📊 Project Progress

- ✅ **Sprint 1**: Foundations & Infrastructure (100%)
- ✅ **Sprint 2**: Vision & 3D - Depth Estimation (100%)
- ✅ **Sprint 3**: Contract Intelligence (100%)
- 🔄 **Sprint 4**: Polished UI/UX & Finalization (50%)

**Total progress: ~88%**

See [SPRINTS.md](./SPRINTS.md) for more details.

## 📖 Documentation

- [Architecture](./ARCHITECTURE.md) - Technical details and architecture choices
- [Sprints](./SPRINTS.md) - Project planning and roadmap
- [Setup](./SETUP.md) - Detailed installation guide

## 🔧 Technical Highlights

**Architecture**:

- Microservices architecture with separated frontend/backend
- RESTful API with FastAPI
- Real-time health monitoring
- Docker containerization

**AI/ML Integration**:

- Multiple transformer models (Depth Anything, OWL-ViT)
- YOLO for real-time object detection
- OCR with Tesseract for document processing
- Custom business logic for claim evaluation

**Frontend**:

- Vue 3 Composition API
- 3D rendering with Three.js (TresJS)
- Responsive design with TailwindCSS
- Progressive Web App capabilities

## 🤝 Contributing

Contributions are welcome! Feel free to open an issue or pull request.

## 📝 License

MIT License - see [LICENSE](./LICENSE)

---

**Developed by** [@machichiotte](https://github.com/machichiotte) | **2025**
