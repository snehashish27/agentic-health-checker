# seed_cloudant.py
import json
import os
from ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from app.config import settings

def migrate_to_cloudant():
    print("🚀 Initializing IBM Cloudant Migration...")

    # 1. Authenticate with IBM Cloudant
    authenticator = IAMAuthenticator(settings.CLOUDANT_API_KEY)
    cloudant = CloudantV1(authenticator=authenticator)
    cloudant.set_service_url(settings.CLOUDANT_URL)

    db_name = "trusted-medical-guidelines"

    # 2. Check if database exists, create if it doesn't
    try:
        cloudant.get_database_information(db=db_name).get_result()
        print(f"✅ Database '{db_name}' already exists.")
    except Exception:
        print(f"⚠️ Database not found. Creating '{db_name}'...")
        cloudant.put_database(db=db_name).get_result()
        print("✅ Database created successfully.")

    # 3. Load the local JSON file
    if not os.path.exists("sample_guidelines.json"):
        print("❌ Cannot find sample_guidelines.json!")
        return

    with open("sample_guidelines.json", "r", encoding="utf-8") as f:
        guidelines = json.load(f)

    # 4. Upload documents to the cloud
    print(f"📦 Uploading {len(guidelines)} guidelines to Cloudant...")
    for doc in guidelines:
        # Cloudant requires an '_id' field for unique documents
        if 'id' in doc:
            doc['_id'] = doc.pop('id') 
            
        try:
            cloudant.post_document(db=db_name, document=doc).get_result()
            print(f"   -> Uploaded: {doc.get('condition')}")
        except Exception as e:
            # If it throws a 409 error, it means the document is already in the database
            if "conflict" in str(e).lower():
                print(f"   -> Skipped (Already exists): {doc.get('condition')}")
            else:
                print(f"   -> Error uploading {doc.get('condition')}: {e}")

    print("🎉 Migration Complete! Your data is now in the cloud.")

if __name__ == "__main__":
    migrate_to_cloudant()