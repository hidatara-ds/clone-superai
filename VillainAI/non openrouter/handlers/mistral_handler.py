import requests

MISTRAL_API_BASE_URL = "https://api.mistral.ai/v1/chat/completions"

def call_mistral_api(api_key: str, message: str, model_name: str = "mistral-small-latest"):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model_name,
        "messages": [
            {"role": "user", "content": message}
        ]
    }
    try:
        response = requests.post(MISTRAL_API_BASE_URL, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        # Struktur respons Mistral: data['choices'][0]['message']['content']
        return data['choices'][0]['message']['content']
    except Exception as e:
        raise Exception(f"Gagal memanggil Mistral API: {str(e)}")