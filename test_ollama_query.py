import requests
import json
import sys

def main():
    url = "http://127.0.0.1:8003/api/v1/query"
    payload = {
        "query": "Who are the students who submitted the AgroGuard-AI project report?",
        "tenant_id": "00000000-0000-0000-0000-000000000000",
        "llm_provider": "ollama",
        "prompt_version": "v1",
        "embedding_provider": "gemini"
    }

    print("Sending POST request to RAG Engine...")
    print(f"URL: {url}")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(url, json=payload, timeout=300)
        print(f"\nResponse Status: {response.status_code}")
        if response.status_code == 200:
            res_data = response.json()
            print("\nGenerated Answer:")
            print("-" * 50)
            print(res_data.get("answer"))
            print("-" * 50)
            print(f"Faithful: {res_data.get('faithful')}")
            print(f"Router Decision: {res_data.get('route')}")
            print("Retrieved Context Chunks:")
            for idx, ctx in enumerate(res_data.get("contexts", [])):
                print(f"  Chunk #{idx+1}: {ctx[:100]}...")
        else:
            print(f"Error Response: {response.text}")
    except Exception as e:
        print(f"Failed to connect to RAG Engine: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
