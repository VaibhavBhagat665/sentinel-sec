import chromadb
from chromadb.utils import embedding_functions
import os

class CVERetriever:
    def __init__(self, persist_dir="./cve_db"):
        self.client = chromadb.PersistentClient(path=persist_dir)
        
        self.embed_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )
        
        self.collection = self.client.get_or_create_collection(
            name="cve_knowledge",
            embedding_function=self.embed_fn
        )
    
    def add_cve(self, cve_id: str, description: str, fix_pattern: str):
        self.collection.add(
            documents=[f"{description} FIX: {fix_pattern}"],
            ids=[cve_id],
            metadatas=[{"cve_id": cve_id, "fix": fix_pattern}]
        )
    
    def search(self, query: str, n_results: int = 3) -> list[dict]:
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        
        retrieved = []
        for i, doc in enumerate(results["documents"][0]):
            meta = results["metadatas"][0][i]
            retrieved.append({
                "cve_id": meta.get("cve_id"),
                "context": doc,
                "fix_pattern": meta.get("fix")
            })
        return retrieved

def get_rag_context(query: str) -> str:
    try:
        retriever = CVERetriever()
        results = retriever.search(query)
        if not results:
            return ""
        
        context = "Relevant CVE patterns:\n"
        for r in results:
            context += f"- {r['cve_id']}: {r['fix_pattern']}\n"
        return context
    except Exception:
        return ""
