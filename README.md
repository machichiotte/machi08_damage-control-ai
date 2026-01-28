# DamageControl AI - Automated Claims Expert

[![GitHub](https://img.shields.io/badge/GitHub-machichiotte%2Fdamage--control--ai-blue?logo=github)](https://github.com/machichiotte/damage-control-ai)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](./LICENSE)
[![Netlify Status](https://api.netlify.com/api/v1/badges/YOUR_SITE_ID/deploy-status)](https://app.netlify.com/sites/damage-control-ai/deploys)

## 🌐 Live Demo

🚀 **Application**: [https://damage-control-ai.netlify.app](https://damage-control-ai.netlify.app)

📚 **API Documentation**: [https://machichiotte-damage-control-ai-backend.hf.space/docs](https://machichiotte-damage-control-ai-backend.hf.space/docs)

> 💡 **Infrastructure**: Frontend hosted on Netlify, Backend on Hugging Face Spaces (16 GB RAM).

## 🎯 Overview

## 📸 Features in Action

### 1. Interactive Dashboard

The application welcomes you with a modern, dark-themed interface designed for efficiency.
![Dashboard](assets/dashboard.png)

### 2. Smart Upload & Analysis

Upload photos easily via drag & drop. The system instantly validates the image and proposes relevant AI analyses.
![Upload Analysis](assets/upload_success.png)

### 3. Object Detection (YOLO)

Identify general objects (vehicles, people) in the scene to understand the context of the accident.
![YOLO Detection](assets/yolo_detection.png)

### 4. Part Claims Inspection (Zero-Shot)

Precisely detect car parts (wheels, bumpers, doors) to assess specific damages using OWL-ViT technology.
![Parts Analysis](assets/owl_detection.png)

### 5. Depth Estimation (3D)

Analyze the severity of impacts using 3D depth maps (not shown above, but available in the app).
![Depth Estimation](assets/depth_estimation.png)

### 6. Interactive 3D Visualization

Explore the scene in 3D with interactive controls.
![3D Visualization](assets/3d_visualization.png)

## ✨ Core Capabilities

### ✅ Implemented

1. **Interactive Image Upload** - Drag & drop, instant preview.
2. **Depth Estimation** - 3D depth maps with INFERNO colormap.
3. **Interactive 3D Visualization** - 3D rendering with TresJS.
4. **Object Detection** - YOLOv8 nano for real-time detection.
5. **Zero-Shot Detection** - OWL-ViT for specific part identification.
6. **Contract Analysis** - PDF/Image upload and Regex extraction.
7. **Claim Evaluation** - Automated decision making based on visual and contractual data.

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
pnpm install
pnpm run dev
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
