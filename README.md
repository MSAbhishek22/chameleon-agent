![Chameleon Agent](https://capsule-render.vercel.app/api?type=waving&color=0:0d1117,50:1f6feb,100:8957e5&height=180&section=header&text=Chameleon%20Agent&fontSize=42&fontColor=ffffff&animation=fadeIn)

# 🦎 Chameleon Agent — The Agentic Honey-Pot

> **It plays the perfect victim — so the scammer becomes the one being studied.**

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Google Gemini](https://img.shields.io/badge/Google%20Gemini-8E75B2?style=for-the-badge&logo=googlegemini&logoColor=white)
![Built For](https://img.shields.io/badge/Built%20for-India%20AI%20Impact%20Buildathon%20·%20Fraud%20Detection-1f6feb?style=for-the-badge)

---

## 📖 The Story

Every day, thousands of Indians get the same calls: *"Your account will be blocked."* *"You have won 5 lakh rupees!"* *"This is the bank, share your OTP."* The people on the other end are professionals — scripted, patient, and gone the moment they've been paid.

The Chameleon Agent flips that script. Instead of blocking the scammer, it **becomes the victim they dream of** — a confused retired bank employee, an excited lottery winner, a busy shopkeeper — talks to them at length, keeps them busy… and quietly notes down everything that can identify them: the bank accounts, UPI IDs, phone numbers and phishing links they reveal while trying to run the con. Built for the **India AI Impact Buildathon — Fraud Detection Challenge**.

Like a chameleon, it changes colour to match whoever is hunting it.

---

## 🎯 The Problem

- 📞 Scam calls and messages scale effortlessly; human victims and police reports don't.
- 🕵️ Scammers reveal their real infrastructure — payment accounts, UPI handles, phishing domains — *only mid-conversation*, to someone they believe is about to pay.
- 🚔 By the time a real victim reports a scam, that infrastructure has usually moved on.

## 👥 Who It's For

- 🏦 **Banks & fintech fraud teams** — who need fresh scammer payment identifiers, not yesterday's blocklists.
- 👮 **Cybercrime & enforcement units** — actionable intelligence (accounts, UPI IDs, URLs) extracted from live scam conversations.
- 🛡️ **Trust & safety builders** — a working reference architecture for agentic honeypots in the Indian scam ecosystem.

## ✨ What It Does

> Every feature below is in the code in this repo (`main.py`, `app/`, `requirements.txt`):

- 🔍 **Detects the scam first** — `app/detection.py` (`ScamDetector`) analyses each incoming message and classifies it across **5 scam types: tech support, financial, prize/lottery, romance and job** scams, with a confidence score.
- 🎭 **Answers in character** — `app/personas.py` holds **5 psychologically-crafted personas** matched to scam type — verified in code: *Ramesh Kumar*, a trusting 67-year-old retired bank employee for tech-support/financial scams; *Suresh Menon*, a busy Bangalore shopkeeper; *Priya Sharma*, an excited Jaipur student for lottery scams — each with its own delay-and-extract conversation strategy.
- 🧲 **Extracts the intelligence** — `app/extraction.py` (`IntelligenceExtractor`) pulls **bank accounts, UPI IDs, phone numbers and phishing URLs** out of the conversation as it unfolds.
- 💬 **Sustains the conversation** — `app/agent.py` (`ConversationManager`) runs a multi-turn, Gemini-powered engagement (trust-building → extraction → deep extraction) with per-session state.
- 🔌 **Ships as an API** — a FastAPI service (`main.py`) with `POST /honeypot`, a hackathon-format `POST /` endpoint, `GET /health`, API-key header authentication, CORS, and a `Procfile` + step-by-step Render deployment guide (`DEPLOYMENT.md`) for going live.

## 🔑 USP

**It doesn't detect scams to stop the conversation — it detects them to *start* one.** Ordinary filters say "blocked" and learn nothing. The Chameleon wastes the scammer's scarcest resource (time), plays a persona tuned to their exact script, and walks away with the payment identifiers enforcement actually needs — the scammer interviews *themselves*.

## 🛠️ Tech Stack

- 🐍 **Python + FastAPI** — the API service (`uvicorn` / `gunicorn` in `requirements.txt`)
- 🤖 **Google Gemini** (`google-generativeai`) — the LLM behind the personas and conversation manager
- 📦 **Pydantic** — request/response models (`app/models.py`)
- ⚙️ **python-dotenv, requests, regex** — config, HTTP and pattern-based extraction support

## 🚀 Future Plans

- [ ] Persist extracted intelligence into a shareable, deduplicated scammer-indicator feed.
- [ ] Add voice-call personas for the call-centre scams that never touch text.
- [ ] Expand persona library with regional-language (Hindi-first) variants.
- [ ] Package the detector as a standalone library other apps can embed.

## 🚀 How to Run

```bash
pip install -r requirements.txt
```

Set your Gemini API key (`GEMINI_API_KEY` in a `.env` file), then start the API:

```bash
uvicorn main:app --reload
```

- `POST /honeypot` — send a message and get the honeypot's in-character reply.
- `GET /health` — service health check.
- Deploy: see `DEPLOYMENT.md` for the step-by-step Render guide.

## 🔗 More From The Builder

**Built by [M S Abhishek](https://github.com/MSAbhishek22)** — agents that protect people are a running theme here; see also ClaimLens and Verity.
👉 **[github.com/MSAbhishek22](https://github.com/MSAbhishek22)**

> *"The best defence against a con artist is a victim who was never real."*
