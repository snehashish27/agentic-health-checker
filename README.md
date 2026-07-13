# 🏥 Sanjeevani AI
### Your Intelligent, Agentic Medical Assistant
**Built with IBM Watsonx**

---

## 🌟 The Challenge
Understanding health conditions based on symptoms can be daunting, as individuals often struggle with misinformation, delayed detection, and self-diagnosis risks. Verified medical data and guidelines are scattered across various medical journals and government portals. Without reliable, real-time symptom analysis, many fail to take informed health actions, apply preventive care, or determine the appropriate urgency for consulting a doctor.

## 🚀 Our Solution
**Sanjeevani AI** is an intelligent, multi-agent health symptom checker designed to combat medical misinformation, reduce self-diagnosis anxiety, and provide immediate, actionable triage guidance. Built on the powerful **IBM Watsonx AI** platform, our solution transforms scattered, complex medical knowledge into a highly empathetic, accessible, and interactive health companion.

To meet and exceed the challenge objectives, we architected Sanjeevani AI using a sophisticated **Multi-Agent RAG (Retrieval-Augmented Generation) Pipeline**, ensuring that all advice is strictly grounded in verified clinical data.

---

## ✨ Key Features & Agents

🤖 **Symptom Analysis Agent (Extractor)**
Users do not need to navigate complex medical menus; they simply type or speak their symptoms in natural language. Our dedicated Extractor Agent processes the input to identify clinical markers, symptom durations, and severity levels in real-time.

📚 **Medical Knowledge Agent (Retriever)**
To eliminate AI hallucinations and the risks of unchecked self-diagnosis, we implemented a robust Vector Database using **ChromaDB**. When symptoms are analyzed, this Agent performs semantic similarity searches against a curated dataset of verified WHO and government medical guidelines.

🩺 **Advisory & Triage Agent (Generator)**
Our Generator Agent acts as an empathetic digital physician. Using the retrieved verified guidelines, it formulates a conversational response that clearly outlines safe home care remedies, preventive advice, and critical "Hospital Triggers".

🌍 **Seamless Multi-Language Interaction**
Healthcare is universal, and so is Sanjeevani AI. The Advisory Agent dynamically detects the user's input language and script (e.g., English, Hindi, Bengali, Hinglish). It is strictly prompted to respond in the exact same language and script, providing critical health triage to diverse populations without relying on clunky third-party translation APIs.

---

## 🛠 The Medical Toolkit (Bonus Features)

To ensure comprehensive care, we expanded the system with an advanced, interactive "Mega Menu" toolkit:
*   🚑 **Emergency Hospital Triangulation:** A geolocation-aware **Hospital Finder Agent** automatically triggers during critical emergencies, calculating the distance and driving time to the nearest highly-rated clinics.
*   📊 **Interactive Vitals Analyzer:** Users can log real-time vitals (BP, SpO2, Heart Rate) which are instantly analyzed against clinical thresholds and injected directly into the LLM's chat context.
*   🧪 **Lab Report Explainer:** A specialized Agent that decodes dense, anxiety-inducing medical jargon from lab PDF reports into plain, easy-to-understand language.
*   🚨 **Distraction-Free First Aid Guide:** Step-by-step, visually striking emergency protocols equipped with Text-to-Speech (TTS) accessibility for high-stress situations.

---

## ⚙️ Technology Stack

*   **AI Backend:** IBM Cloud & IBM Watsonx AI ( Llama Architectures)
*   **Vector Database:** ChromaDB & HuggingFace Sentence Transformers (`all-MiniLM-L6-v2`)
*   **Backend Framework:** Python, FastAPI, Uvicorn
*   **Frontend:** HTML5, Vanilla JS, Tailwind CSS

---

## 💻 How to Run Locally

**1. Clone the repository and install dependencies:**
```bash
git clone https://github.com/snehashish27/agentic-health-checker.git
cd agentic-health-checker
pip install -r requirements.txt
```

**2. Set up your IBM Watsonx Credentials:**
Create a `.env` file in the root directory and add your credentials:
```env
IBM_CLOUD_API_KEY=""
WATSONX_SPACE_ID=""
WATSONX_URL="https://au-syd.ml.cloud.ibm.com"
CLOUDANT_URL=""
CLOUDANT_API_KEY=""
```

**3. Build the Vector Database:**
Seed ChromaDB with the verified WHO sample guidelines:
```bash
python scripts/seed_vector_db.py
```

**4. Start the Application:**
```bash
uvicorn app.main:app --reload
```
Navigate to `http://localhost:8000` in your browser to start using Sanjeevani AI!

---
