git clone https://github.com/arutovan-droid/alos-ani-mvp.git
**ALOS – Advanced Logistics Operating System** is a concept for a regional logistics OS for complex trade corridors  
(Iran–Caucasus–Black Sea, INSTC, Middle Corridor, etc.).

This repository contains a **minimal MVP** of the customs engine module called  
**ANI – Automated Neural Inspector**.

> Goal: given a messy, mixed-language item description  
> (e.g. `բլուտուզ խոսփաքեր`),  
> produce a suggested HS (Tariff) code and a simple risk flag.

---

## What this MVP does

This prototype demonstrates the core idea of the customs engine:

1. **Normalization**  
   - Converts Armenian script and mixed text into a cleaned Latin form.  
   - Example:  
     `բլուտուզ խոսփաքեր (новый, 2025)` → `blutuz khospaker  novyi  2025`

2. **Embeddings & semantic search**  
   - Uses `sentence-transformers` to encode the normalized text into vector embeddings.  
   - Compares it to a tiny in-memory **knowledge base** of reference descriptions.

3. **HS classification (very small demo)**  
   - Picks the closest description and returns:
     - HS code (e.g. `851821` for bluetooth speakers),
     - risk flag (`low`, `encryption`, `dual-use`),
     - confidence score.

It is **not production-ready**, but is meant to show the architecture:

> normalization → embeddings → semantic search → HS classification.

---

## Repository structure

```text
alos-ani-mvp/
├─ README.md
├─ requirements.txt
├─ alos_core/
│  ├─ __init__.py
│  └─ customs/
│     ├─ __init__.py
│     ├─ normalizer.py   # Armenian → Latin + cleanup
│     ├─ engine.py       # Embeddings + semantic HS lookup
│     └─ api.py          # FastAPI HTTP endpoint
└─ examples/
   └─ demo_classify.py   # Simple CLI demo
Core modules
alos_core/customs/normalizer.py

ArmNormalizer class:

lowercases, trims,

maps Armenian letters to Latin (բ → b, խ → kh, ու → u, …),

removes non-alphanumeric noise.

alos_core/customs/engine.py

CustomsEngine class:

loads a multilingual SentenceTransformer model
(paraphrase-multilingual-MiniLM-L12-v2),

keeps a small, hard-coded knowledge base of item descriptions with HS codes,

provides predict_hs(raw_query: str) → dict with:

hs_code, risk_flag, confidence, etc.

alos_core/customs/api.py

FastAPI application exposing a single endpoint:

POST /classify with JSON body {"text": "..."}

returns JSON with HS code prediction and metadata.

examples/demo_classify.py

Simple interactive CLI tool for quick testing.

Installation
bash
Копировать код
git clone https://github.com/arutovan-droid/alos-ani-mvp.git
cd alos-ani-mvp

python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate

pip install -r requirements.txt
Usage
1. CLI demo
Run:

bash
Копировать код
python -m examples.demo_classify
Sample interaction:

text
Копировать код
ALOS ANI demo. Type text (Ctrl+C to exit).
> բլուտուզ խոսփաքեր
HS: 851821 | conf=0.91 | risk=low | matched='wireless bluetooth speaker portable audio device' | norm='blutuz khospaker'

> айфон 15 про
HS: 851712 | conf=0.88 | risk=encryption | matched='smartphone mobile phone iphone samsung with encryption' | norm='аифон 15 про'
(Numbers in this example are illustrative — exact scores depend on the model run.)

2. HTTP API (FastAPI)
Start the API server:

bash
Копировать код
uvicorn alos_core.customs.api:app --reload
You should see something like:

text
Копировать код
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
Swagger UI
Open in a browser:

http://127.0.0.1:8000/docs

You can test the /classify endpoint interactively there.

cURL example
bash
Копировать код
curl -X POST http://127.0.0.1:8000/classify \
  -H "Content-Type: application/json" \
  -d '{"text": "բլուտուզ խոսփաքեր"}'
Example JSON response:

json
Копировать код
{
  "raw_input": "բլուտուզ խոսփաքեր",
  "normalized": "blutuz khospaker",
  "matched_desc": "wireless bluetooth speaker portable audio device",
  "confidence": 0.91,
  "hs_code": "851821",
  "risk_flag": "low"
}
Notes on language & data
In real customs documents in this region, we mostly see:

Armenian script + Russian/English,

sometimes mixed with transliterated Chinese/Turkish product names.

Armenian written in Latin (“barev dzez”-style, hy-Latn) is common in chats,
but relatively rare in official documents.

The current MVP:

Explicitly handles Armenian script via a custom normalizer,

Treats existing Latin text as-is,

Is easy to extend later with:

better Armenian normalization,

dedicated support for hy-Latn,

larger HS code dictionaries and proper vector databases.

Roadmap / TODO (high-level)
Replace the tiny hard-coded knowledge base with:

a proper HS code + description dataset,

a vector DB (Qdrant / FAISS / Chroma).

Add top-k results and ambiguity handling:

multiple candidate HS codes with scores,

thresholds for human review.

Extend language handling:

richer Armenian normalization,

better support for Russian + hybrid text,

optional hy-Latn handling if real data requires it.

Add logging & telemetry:

track corrections from human inspectors,

support human-in-the-loop learning.

Disclaimer
This repository is a minimal proof-of-concept for the ALOS customs engine (ANI):

It is not meant for production use as-is.

The HS codes and descriptions in the knowledge base are illustrative.

There is no legal or compliance guarantee in this code.

It is intended to demonstrate one possible architecture for
an AI-assisted customs classification engine in a complex multilingual environment.
