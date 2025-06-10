import requests

COHERE_API_BASE_URL = "https://api.cohere.ai/v1/chat"

def call_cohere_api(api_key: str, message: str, model_name: str = "command-r"):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model_name,
        "message": message
    }
    try:
        response = requests.post(COHERE_API_BASE_URL, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        # Struktur respons Cohere: data['text']
        return data['text']
    except Exception as e:
        raise Exception(f"Gagal memanggil Cohere API: {str(e)}")