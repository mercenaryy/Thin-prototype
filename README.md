# Thine — Personal Intelligence AI
### *A co-founder for the project called life.*

> Built as a working prototype inspired by [Thine](https://www.linkedin.com/company/thine) — an AI that doesn't just answer your questions, it understands your whole story.

---

## What This Is

General-purpose AI is great at answering questions you know how to ask.

But the real questions — *Am I becoming who I wanted to be? What loops am I leaving open? What drains me without me noticing?* — don't fit in a prompt.

This prototype reads one week of a real person's behavioral data and lets you have a conversation about it. Not summaries. Not dashboards alone. An AI that was actually *there* for the week and can reflect it back to you.

**Try asking:**
- *"What triggers my stress?"*
- *"What loops did I leave open this week?"*
- *"When am I actually most productive?"*
- *"What decisions did I make when I was tired?"*
- *"Summarise my week in 3 sentences."*

---

## Demo

| Chat | Dashboard | Patterns |
|------|-----------|----------|
| Ask natural language questions about the week | 6 interactive Plotly charts | 10 pattern insights + loop tracker |

**Live demo:** `[your-streamlit-url-here]`
*(Dashboard and Patterns work without an API key. Chat requires a free Groq key — 30 seconds at [console.groq.com](https://console.groq.com))*

---

## Features

**💬 Chat Interface**
- Natural language questions about the user's week
- 8 sample question buttons to get started
- Powered by LangGraph agent with custom behavioral data tools

**📊 Behavioral Dashboard**
- Emotion frequency breakdown
- Activity type distribution (Work / Social / Leisure / Health / etc.)
- Hourly activity heatmap — see exactly when the day happens
- Decision confidence chart
- Positive vs negative emotions by day of week

**🔍 Patterns & Loops**
- 10 AI-generated pattern insights with reflection prompts
- Behavioral loop tracker (Closed / Delayed / Open)
- Emotion → Decision mapping table

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Agent Framework | [LangGraph](https://github.com/langchain-ai/langgraph) |
| LLM | Groq (llama-3.3-70b-versatile) — swappable |
| Tools | Custom `@tool` functions over Excel data |
| UI | [Streamlit](https://streamlit.io) |
| Charts | [Plotly](https://plotly.com) |
| Data | openpyxl (Excel parsing) |
| Config | python-dotenv |

---

## Data Structure

The sample data is one week of a real person's life across 4 sheets:

| Sheet | Description | Records |
|-------|-------------|---------|
| Signal Theory | Daily events with time, type, emotion, signal | 67 events |
| Loops | Tasks/intentions tracked across the week | 10 loops |
| Decision Log | Decisions with context, emotion, confidence | 22 decisions |
| Pattern Engine | AI-generated behavioral insights | 10 patterns |

---

## Architecture

```
User question
      ↓
Streamlit (app.py)
      ↓
ask() in agent.py
      ↓
LangGraph agent loop
      ↓
LLM decides which tool to call
      ├── get_user_behavioral_data()  →  returns compressed data summary (~1400 tokens)
      └── analyze_user_patterns()    →  returns filtered data by category
      ↓
LLM generates answer
      ↓
Response displayed in chat
```

**Key design decisions:**
- **Lazy LLM init** — graph is only built on the first question, never at import time. Zero tokens burned on startup or page refresh.
- **Compressed data format** — events stored as `time|event|type|emotion` instead of verbose key-value pairs. Cuts token usage by 60%.
- **Swappable LLM** — change only `_build_graph()` to switch between Groq, Gemini, OpenAI, or Anthropic. Everything else stays the same.
- **System prompt injected once** — only on the first turn, not on every tool-call round trip.

---

## Setup

### Requirements
- Python 3.11 (not 3.14 — Pydantic v1 compatibility)
- A free [Groq API key](https://console.groq.com) (100k tokens/day free)

### Install & Run

```bash
# 1. Clone the repo
git clone https://github.com/yourusername/thine-prototype
cd thine-prototype

# 2. Create virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Add your API key
cp .env.example .env
# Edit .env and add your GROQ_API_KEY

# 5. Run the web app
streamlit run app.py

# Or run the CLI version
python main.py
```

### Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY="your_groq_key_here"

# Optional fallbacks
GEMINI_API_KEY="your_gemini_key_here"
OPENAI_API_KEY="your_openai_key_here"
ANTHROPIC_API_KEY="your_anthropic_key_here"
```

Get a free Groq key at [console.groq.com](https://console.groq.com) — no credit card needed.

---

## File Structure

```
thine-prototype/
├── app.py                      # Streamlit web UI
├── agent.py                    # LangGraph agent + tools
├── data_loader.py              # Excel parser + data formatter
├── main.py                     # CLI chat interface
├── AI_model-_Raw_Data.xlsx     # Sample behavioral data
├── requirements.txt            # Python dependencies
├── .env                        # API keys (never commit this)
└── .env.example                # Template for .env
```

---

## What's Next

- [ ] **File upload** — let users upload their own Excel behavioral data
- [ ] **Multi-user support** — per-user data isolation with auth
- [ ] **Vector store** — FAISS/Chroma for semantic retrieval instead of full-context injection
- [ ] **Memory layer** — LangGraph MemorySaver for persistent conversations
- [ ] **Daily logging** — in-app form to log events instead of uploading Excel
- [ ] **Weekly digest** — automated pattern summary every Sunday

---

## Why I Built This

Thine's vision is an AI that lives alongside you — not one you prompt, but one that understands your evolution. This prototype is a small proof that the idea works technically. One week of data is enough for the AI to surface real patterns, name emotional triggers, and reflect loops back at you that you didn't even realise you'd left open.

The real version needs years of data, not days. But the skeleton is here.

---

## License

MIT — use it, break it, build on it.

---

*Built with LangGraph + Groq + Streamlit*
*Inspired by [Thine](https://www.linkedin.com/company/thine) — "Thine is the mind that grows with you"*
