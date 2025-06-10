import requests
import json

# Anda mungkin perlu menyesuaikan endpoint dan cara pembuatan payload
# berdasarkan dokumentasi resmi Gemini API.
# Model 'gemini-1.5-flash-latest' adalah contoh, sesuaikan dengan "Gemini 2.0 Flash" yang Anda maksud.
GEMINI_API_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models"

def call_gemini_api(api_key: str, message: str, model_name: str = "gemini-1.5-flash-latest"):
    """
    Memanggil Gemini API dan mengembalikan respons teks.
    """
    api_url = f"{GEMINI_API_BASE_URL}/{model_name}:generateContent?key={api_key}"
    
    headers = {
        "Content-Type": "application/json"
    }
    
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": message}
                ]
            }
        ]
        # Anda mungkin perlu menambahkan parameter lain seperti generationConfig, safetySettings, dll.
    }
    
    try:
        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status()  # Akan raise exception untuk status HTTP 4xx/5xx
        
        response_data = response.json()
        
        # Ekstrak teks dari respons Gemini
        # Struktur respons mungkin berbeda, cek dokumentasi Gemini
        if response_data.get("candidates") and response_data["candidates"][0].get("content"):
            return response_data["candidates"][0]["content"]["parts"][0]["text"]
        else:
            # Fallback jika struktur tidak sesuai atau ada error di data
            # Mungkin juga ada informasi error di response_data.get("promptFeedback")
            return "Tidak ada respons dari Gemini atau format respons tidak dikenal."
            
    except requests.exceptions.RequestException as e:
        print(f"Error saat memanggil Gemini API: {e}")
        # Anda bisa me-raise ulang error atau mengembalikan pesan error spesifik
        raise Exception(f"Gagal menghubungi Gemini API: {str(e)}")
    except (KeyError, IndexError) as e:
        print(f"Error parsing respons Gemini: {e}, data: {response_data}")
        raise Exception(f"Gagal memproses respons dari Gemini: {str(e)}")