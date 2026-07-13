# app/main.py
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.agents.extractor import ClinicalExtractorAgent
from app.agents.retriever import KnowledgeRetriever
from app.agents.generator import ClinicalGeneratorAgent
from app.agents.hospital_finder import HospitalFinder
from app.agents.lab_explainer import LabExplainerAgent
from typing import Optional

# 1. Initialize the Web Application
app = FastAPI(title="Agentic Health Checker API", version="1.0.0")

# 2. Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Load the AI Agents
print("Booting AI Agents (Connecting to Sydney Watsonx)...")
extractor = ClinicalExtractorAgent()
retriever = KnowledgeRetriever()
generator = ClinicalGeneratorAgent()
hospital_finder = HospitalFinder()
lab_explainer = LabExplainerAgent()
print("System Ready.")

# 4. Define Request Structure
class PatientRequest(BaseModel):
    complaint: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    history: list = []

class LabReportRequest(BaseModel):
    report_text: str

# 5. Core API Route
@app.post("/api/v1/analyze")
async def analyze_patient_case(request: PatientRequest):
    try:
        extracted_data = extractor.extract_symptoms(request.complaint)
        symptoms_list = extracted_data.get("symptoms", [])
        matched_guidelines = retriever.fetch_matching_guidelines(symptoms_list)
        
        # New RAG Generation Step with History
        rag_response = generator.generate_response(request.complaint, matched_guidelines, request.history)
        
        # Tool Intercept Step
        hospital_recommendations = []
        if "[TOOL: HOSPITAL_FINDER]" in rag_response:
            rag_response = rag_response.replace("[TOOL: HOSPITAL_FINDER]", "").strip()
            
            lat = request.latitude if request.latitude is not None else 28.7041
            lon = request.longitude if request.longitude is not None else 77.1025
            
            print(f"Triggering Hospital Finder Tool at {lat}, {lon}...")
            hospital_recommendations = hospital_finder.find_nearest_hospitals(lat, lon)
            print(f"Hospitals found: {len(hospital_recommendations)}")
        
        return {
            "status": "success",
            "clinical_extraction": extracted_data,
            "medical_knowledge": matched_guidelines,
            "rag_output": rag_response,
            "hospital_recommendations": hospital_recommendations
        }
    except Exception as e:
        print(f"Server Error: {e}")
        raise HTTPException(status_code=500, detail="Internal AI Processing Error")

@app.post("/api/v1/explain_labs")
async def explain_labs(request: LabReportRequest):
    try:
        explanation = lab_explainer.explain_report(request.report_text)
        return {
            "status": "success",
            "explanation": explanation
        }
    except Exception as e:
        print(f"Lab Explainer Error: {e}")
        raise HTTPException(status_code=500, detail="Internal AI Processing Error")

@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    # This reads your HTML file and serves it as the main web page
    with open("frontend.html", "r", encoding="utf-8") as f:
        return f.read()