# app/agents/extractor.py
import json
from ibm_watsonx_ai.foundation_models import ModelInference
from app.config import settings

class ClinicalExtractorAgent:
    def __init__(self):
        # Using the Llama-3 70B model that is active in your Sydney region
        self.model_id = "meta-llama/llama-3-3-70b-instruct"
        self.credentials = {
            "url": settings.WATSONX_URL,
            "apikey": settings.IBM_CLOUD_API_KEY
        }
        
        # Low temperature (0.1) prevents the AI from hallucinating extra symptoms
        self.model = ModelInference(
            model_id=self.model_id,
            credentials=self.credentials,
            space_id=settings.WATSONX_SPACE_ID,
            params={"max_new_tokens": 200, "temperature": 0.1}
        )

    def extract_symptoms(self, user_input: str) -> dict:
        system_prompt = (
            "You are a highly precise clinical NLP parser. Analyze the patient's statement, "
            "which may be in English, Hindi, Hinglish, or Bengali. "
            "Extract the primary symptoms, implied duration, and severity markers. "
            "Respond ONLY with a valid JSON object matching this schema exactly:\n"
            "{\n"
            '  "symptoms": ["list", "of", "extracted", "symptoms", "normalized", "to", "english"],\n'
            '  "duration": "extracted duration or unknown",\n'
            '  "severity_markers": ["any", "worrying", "signs", "like", "bleeding"]\n'
            "}\n"
            "Do not include any conversational filler or markdown."
        )
        
        # Proper prompt formatting for Llama-3 instruction models
        full_prompt = (
            f"<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n{system_prompt}<|eot_id|>\n"
            f"<|start_header_id|>user<|end_header_id|>\nPatient Statement: {user_input}\nJSON Output:<|eot_id|>\n"
            f"<|start_header_id|>assistant<|end_header_id|>\n"
        )
        
        print(f"Executing Extractor Agent for input: '{user_input}'...")
        response = self.model.generate_text(prompt=full_prompt)
        
        try:
            # Clean potential LLM artifacts to ensure pure JSON
            clean_response = response.strip().replace("```json", "").replace("```", "")
            return json.loads(clean_response)
        except Exception as e:
            print(f"Extractor Agent Error: {e}")
            # Fallback safety structure
            return {"symptoms": [user_input.lower()], "duration": "unknown", "severity_markers": []}