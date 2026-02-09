# Waypoint Backend – AI Market Intelligence API

> Backend API powering **Waypoint**, an AI-powered market intelligence platform built for the **Google Gemini 3 Hackathon 2026**.

[![Gemini 3](https://img.shields.io/badge/Gemini-3%20Flash-blue)](https://ai.google.dev)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://python.org)

👉 **Main project & full documentation:**  
[https://github.com/rutvishah22/waypoint-frontend](https://github.com/rutvishah22/waypoint-frontend)

---

## 🚀 What This Backend Does

This repository contains the **FastAPI backend** responsible for:

- Collecting real-world market data via Tavily AI
- Running multi-stage analysis using **Gemini 3**
- Generating structured, evidence-based market intelligence
- Persisting results and serving them to the frontend dashboard

The core innovation — **category diagnosis** — is entirely executed here.

---

## 🤖 Gemini 3 Usage (Core Logic)

- **Model:** `gemini-2.0-flash-exp` (Gemini 3 Flash Preview)
- **Features used:**
  - Structured JSON output with strict schemas
  - Multi-turn reasoning (2-stage workflow)
  - Large context processing (15–30 competitors per run)
  - Business and strategy reasoning (not just summarization)

### Gemini Workflow

**Stage 1 – Category Diagnosis**
```python
base_analysis = gemini_service.generate_structured(
    prompt=market_data + analysis_instructions,
    response_schema={
        "category_diagnosis": {
            "assumed_category": str,
            "recommended_category": str,
            "should_reframe": bool,
            "reasoning": str,
            "confidence": float
        }
    }
)
```
- Determines assumed vs recommended category
- Decides whether reframing is required
- Produces evidence-backed reasoning

**Stage 2 – Strategic Expansion**
```python
detailed_analysis = gemini_service.expand_dashboard_analysis(
    collected_data=market_data,
    base_analysis=stage1_result
)
```
- Builds 10 detailed dashboard sections
- Market reality, competitors, user needs, strategy, MVP, pricing, GTM, risks

All outputs are generated as **machine-parseable JSON** for production reliability.

---

## 🏗️ Tech Stack

- **Framework:** FastAPI (Python 3.11)
- **AI Engine:** Google Gemini 3 API
- **Web Intelligence:** Tavily AI
- **Database:** MongoDB Atlas
- **Deployment:** Render (free tier)

---

## 📦 API Endpoints

### Start Analysis
```http
POST /analyze
```

**Request Body:**
```json
{
  "product_idea": "AI content strategy tool",
  "tier": "free",
  "email": "optional@email.com"
}
```

**Response:**
```json
{
  "success": true,
  "job_id": "abc123...",
  "message": "Analysis started"
}
```

---

### Fetch Results
```http
GET /results/{job_id}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "status": "complete",
    "product_idea": "AI content strategy tool",
    "analysis": {
      "category_diagnosis": "...",
      "overview": "...",
      "market_reality": "...",
      "competitive_landscape": "...",
      "user_pain_and_desires": "...",
      "strategy_and_positioning": "...",
      "mvp_blueprint": "...",
      "pricing_and_monetization": "...",
      "go_to_market": "...",
      "risks_and_unknowns": "..."
    },
    "raw_market_data": {
      "competitors": [...],
      "market_intelligence": {...}
    }
  }
}
```

---

### Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy"
}
```

---

## ⚙️ Local Setup

### Prerequisites

- Python 3.11+
- MongoDB instance
- API keys:
  - [Gemini API Key](https://ai.google.dev)
  - [Tavily API Key](https://tavily.com)

### Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/waypoint-backend.git
cd waypoint-backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file:

```env
GEMINI_API_KEY=your_gemini_api_key
TAVILY_API_KEY=your_tavily_api_key
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/
```

### Run Server

```bash
uvicorn app.main:app --reload
```

Backend runs at: 👉 `http://localhost:8000`

**API Documentation:** `http://localhost:8000/docs` (FastAPI auto-generated)

---

## 🗂️ Project Structure

```
waypoint-backend/
├── app/
│   ├── main.py                 # FastAPI app & routes
│   ├── core/
│   │   └── config.py           # Environment configuration
│   ├── services/
│   │   ├── gemini_service.py   # Gemini 3 integration
│   │   ├── tavily_service.py   # Tavily AI integration
│   │   ├── data_collector.py   # Market data collection
│   │   └── analysis_service.py # Orchestration logic
│   └── utils/
│       ├── market_classifier.py # Signal classification
│       └── fingerprint.py       # URL deduplication
├── requirements.txt
├── .env.example
└── README.md
```

---

## 🧠 Why This Backend Matters

Without this backend:
- ❌ There is no category diagnosis
- ❌ No competitive intelligence
- ❌ No evidence-based strategy
- ❌ No Gemini-powered reasoning

This service transforms unstructured market data into **actionable startup decisions** using Gemini 3.

### Key Technical Innovations

**1. Two-Stage Gemini Pipeline**
- Base analysis establishes category positioning
- Expansion builds detailed strategic recommendations
- Maintains context across stages for coherent insights

**2. Structured Output Enforcement**
```python
# Robust JSON parsing with cleanup
raw = response.text.strip()
raw = raw.replace("```json", "").replace("```", "").strip()
parsed = json.loads(raw)
```

**3. Intelligent Data Collection**
- Deduplication prevents redundant scraping
- Classification routes signals to correct categories
- Prioritizes recent, high-confidence data

**4. Production-Ready Error Handling**
- Graceful degradation when data sources fail
- Retry logic for transient failures
- Comprehensive logging for debugging

---

## 🔗 Related Links

- 🌐 **Live Demo:** [https://waypoint-pi.vercel.app/](https://waypoint-pi.vercel.app/)
- 💻 **Frontend Repo:** [https://github.com/rutvishah22/waypoint-frontend](https://github.com/rutvishah22/waypoint-frontend)
- 📝 **Devpost Submission:** [https://devpost.com/software/waypoint](https://devpost.com/software/waypoint)
- 🎥 **Demo Video:** [https://youtube.com/watch?v=YOUR_VIDEO_ID](https://youtube.com/watch?v=YOUR_VIDEO_ID)

---

##  License

MIT License 

---

##  Acknowledgments

- **Google Gemini Team** - For the powerful Gemini 3 API
- **Tavily AI** - For reliable web intelligence
- **Render** - For free backend hosting
- **MongoDB** - For free database tier


---

**Built with FastAPI, Gemini 3, and a focus on real-world startup decisions.**

*Submitted to the Google Gemini 3 Hackathon 2026*
