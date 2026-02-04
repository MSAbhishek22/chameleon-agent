# Chameleon Agent - Agentic Honey-Pot System

**India AI Impact Buildathon - Fraud Detection Challenge**

An AI-powered honeypot system that detects scam messages and autonomously engages scammers using psychologically sophisticated personas to extract actionable intelligence.

## 🎯 Key Features

- **Intelligent Scam Detection**: Multi-signal detection for 5 scam types (tech support, financial, prize, romance, job)
- **Adaptive Personas**: 5 psychologically crafted personas that respond believably to different scam types
- **Strategic Engagement**: Multi-phase conversation strategy (trust building → extraction → deep extraction)
- **Intelligence Extraction**: Extracts bank accounts, UPI IDs, phone numbers, and phishing URLs
- **Real-time Processing**: <2s response time with LLM-powered agent

## 🏗️ Architecture

```
Mock Scammer API → FastAPI Endpoint → Scam Detector → Persona Selector
                                    ↓
                            Conversation Manager (LLM)
                                    ↓
                            Intelligence Extractor → JSON Response
```

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Google Gemini API key (or Groq API key)

### Installation

```bash
# Clone repository
cd "THE CHAMELEON AGENT"

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm

# Configure environment
copy .env.example .env
# Edit .env and add your API keys
```

### Running Locally

```bash
uvicorn main:app --reload --port 8000
```

API will be available at: `http://localhost:8000`

### Testing

```bash
# Run unit tests
pytest tests/ -v

# Test endpoint
curl -X POST http://localhost:8000/honeypot \
  -H "X-API-Key: your_api_key" \
  -H "Content-Type: application/json" \
  -d '{"message": "Congratulations! You won 5 lakh rupees!", "conversation_id": "test_123"}'
```

## 📡 API Specification

### Endpoint: `POST /honeypot`

**Headers:**
- `X-API-Key`: Your authentication key

**Request Body:**
```json
{
  "message": "string",
  "conversation_id": "string",
  "history": [
    {"role": "scammer", "content": "..."},
    {"role": "agent", "content": "..."}
  ]
}
```

**Response:**
```json
{
  "scam_detected": true,
  "scam_type": "prize",
  "confidence": 0.95,
  "agent_response": "Really?! Oh my god! How do I claim it?",
  "extracted_intelligence": {
    "bank_accounts": [...],
    "upi_ids": [...],
    "urls": [...],
    "phone_numbers": [...]
  },
  "engagement_metrics": {
    "turn_count": 5,
    "persona_used": "excited_winner"
  }
}
```

## 🎭 Personas

1. **Worried Senior Citizen** - For tech support & financial scams
2. **Eager Job Seeker** - For job & investment scams
3. **Middle-Class Professional** - For financial & KYC scams
4. **Excited Prize Winner** - For lottery & prize scams
5. **Lonely Individual** - For romance & trust scams

## 🧪 Testing Strategy

- **Unit Tests**: Scam detection, entity extraction, persona selection
- **Integration Tests**: Full conversation flows
- **Mock Scenarios**: 20+ realistic scam conversations
- **Load Testing**: 100 concurrent requests

## 🚢 Deployment

### Railway (Recommended)

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway init
railway up

# Get public URL
railway domain
```

### Environment Variables (Production)
Set these in Railway dashboard:
- `HONEYPOT_API_KEY`
- `GOOGLE_API_KEY`
- `LLM_PROVIDER=gemini`
- `ENVIRONMENT=production`

## 📊 Evaluation Metrics

- **Scam Detection Accuracy**: >95%
- **Engagement Duration**: 8+ turns average
- **Intelligence Extraction**: 3+ entities per conversation
- **Response Latency**: <2s
- **Uptime**: 99%+

## 🛡️ Security & Privacy

- API key authentication
- No data persistence (stateless)
- Conversation history only in memory during session
- No logging of sensitive extracted data in production

## 📝 License

Built for India AI Impact Buildathon 2026

## 👥 Team

Chameleon Agent Team
