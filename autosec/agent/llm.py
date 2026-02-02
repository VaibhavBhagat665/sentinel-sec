import os

def get_llm(temperature=0):
    groq_key = os.environ.get("GROQ_API_KEY")
    if groq_key:
        from langchain_groq import ChatGroq
        return ChatGroq(
            temperature=temperature,
            model_name="llama-3.1-8b-instant",
            api_key=groq_key
        )
    
    ollama_model = os.environ.get("OLLAMA_MODEL", "llama3")
    ollama_host = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
    
    try:
        import requests
        r = requests.get(f"{ollama_host}/api/tags", timeout=2)
        if r.status_code == 200:
            from langchain_ollama import ChatOllama
            print(f"Using Ollama ({ollama_model})")
            return ChatOllama(model=ollama_model, temperature=temperature, base_url=ollama_host)
    except:
        pass
    
    raise ValueError(
        "No LLM configured. Either:\n"
        "1. Install Ollama: ollama.ai/download, then 'ollama pull llama3'\n"
        "2. Set GROQ_API_KEY environment variable"
    )
