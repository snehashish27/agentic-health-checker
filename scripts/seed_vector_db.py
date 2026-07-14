# seed_vector_db.py
import chromadb
import json
from sentence_transformers import SentenceTransformer

def build_vector_database():
    print("🧠 Loading Embedding Model (all-MiniLM-L6-v2)...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    print("🗄️ Initializing ChromaDB...")
    # This creates a local folder called 'chroma_db' to store your vector arrays
    client = chromadb.PersistentClient(path="./chroma_db")
    
    # Create or overwrite the collection
    try:
        client.delete_collection(name="medical_guidelines")
    except:
        pass
    collection = client.create_collection(name="medical_guidelines")

    # Load your verified data
    with open("sample_guidelines.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    print(f"📦 Embedding {len(data)} documents into vector space...")
    for i, doc in enumerate(data):
        # We combine the condition and symptoms into one rich paragraph for the AI to embed
        text_to_embed = f"Condition: {doc['condition']}. Symptoms include: {', '.join(doc['indicators'])}. Care involves: {doc['home_care']}"
        
        # Convert text to a 384-dimensional vector array
        embedding = model.encode(text_to_embed).tolist()

        # ChromaDB requires all metadata values to be str, int, float, or bool.
        sanitized_doc = {}
        for k, v in doc.items():
            if isinstance(v, list):
                sanitized_doc[k] = ", ".join(str(item) for item in v)
            elif isinstance(v, dict):
                sanitized_doc[k] = str(v)
            else:
                sanitized_doc[k] = v

        # Store the vector alongside the sanitized metadata
        collection.add(
            embeddings=[embedding],
            metadatas=[sanitized_doc],
            ids=[doc.get("id", f"doc_{i}")]
        )
        print(f"   -> Embedded: {doc['condition']}")

    print("✅ True RAG Vector Database Successfully Built!")

if __name__ == "__main__":
    build_vector_database()