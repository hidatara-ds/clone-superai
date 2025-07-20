# AI Chat MVC

Aplikasi web chat AI dengan arsitektur Model-View-Controller (MVC) yang mendukung berbagai API LLM (OpenAI, Gemini, Llama) dengan fitur auto-selection.

## Fitur

- Arsitektur MVC yang bersih dan terstruktur
- Dukungan untuk berbagai API LLM:
  - OpenAI (GPT-3.5, GPT-4)
  - Google Gemini
  - Llama
- Auto-selection API berdasarkan ketersediaan dan performa
- Antarmuka web yang responsif
- Riwayat percakapan

## Struktur Proyek

```
AI-Chat-MVC/
├── app/
│   ├── models/
│   │   ├── __init__.py
│   │   ├── chat_model.py
│   │   ├── openai_model.py
│   │   ├── gemini_model.py
│   │   └── llama_model.py
│   ├── views/
│   │   ├── __init__.py
│   │   ├── templates/
│   │   │   ├── base.html
│   │   │   ├── index.html
│   │   │   └── chat.html
│   │   └── static/
│   │       ├── css/
│   │       ├── js/
│   │       └── img/
│   ├── controllers/
│   │   ├── __init__.py
│   │   └── chat_controller.py
│   └── __init__.py
├── config.py
├── .env.example
├── requirements.txt
└── run.py
```