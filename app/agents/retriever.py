# app/agents/retriever.py
from ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from app.config import settings

class KnowledgeRetriever:
    def __init__(self):
        self.db_name = "trusted-medical-guidelines"
        
        # Connect to Cloudant on boot
        authenticator = IAMAuthenticator(settings.CLOUDANT_API_KEY)
        self.cloudant = CloudantV1(authenticator=authenticator)
        self.cloudant.set_service_url(settings.CLOUDANT_URL)

    def fetch_matching_guidelines(self, extracted_symptoms: list) -> list:
        """
        Pulls guidelines directly from the live Cloudant database and matches symptoms.
        """
        try:
            # Fetch all documents from the cloud database
            response = self.cloudant.post_all_docs(
                db=self.db_name, 
                include_docs=True
            ).get_result()
            
            # Extract the actual data from the Cloudant wrapper
            cloud_guidelines = [item['doc'] for item in response['rows']]
            
            matched_records = []
            normalized_symptoms = [s.lower() for s in extracted_symptoms]

            # Cross-reference logic
            for record in cloud_guidelines:
                indicators = [ind.lower() for ind in record.get("indicators", [])]
                match_count = sum(1 for symptom in normalized_symptoms if any(ind in symptom or symptom in ind for ind in indicators))
                
                if match_count > 0:
                    matched_records.append({
                        "source": record.get("source"),
                        "condition": record.get("condition"),
                        "urgency": record.get("urgency"),
                        "home_care": record.get("home_care"),
                        "hospital_trigger": record.get("hospital_trigger")
                    })
            
            return matched_records
            
        except Exception as e:
            print(f"❌ Cloudant Retrieval Error: {e}")
            return []