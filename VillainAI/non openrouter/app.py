import os
from flask import Flask, request, jsonify, render_template, Response
from dotenv import load_dotenv
import time
import json
from functools import lru_cache

# Import handlers
from handlers import gemini_handler, mistral_handler, cohere_handler

load_dotenv()

app = Flask(__name__)

# Ambil API keys dari environment variables
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
MISTRAL_API_KEY = os.getenv('MISTRAL_API_KEY')
COHERE_API_KEY = os.getenv('COHERE_API_KEY')

# Konfigurasi model yang tersedia
MODELS = {
    'gemini': {
        'api_key': GEMINI_API_KEY,
        'handler_function': gemini_handler.call_gemini_api,
        'models': ['gemini-1.5-flash-latest']
    },
    'mistral': {
        'api_key': MISTRAL_API_KEY,
        'handler_function': mistral_handler.call_mistral_api,
        'models': ['mistral-small-latest']
    },
    'cohere': {
        'api_key': COHERE_API_KEY,
        'handler_function': cohere_handler.call_cohere_api,
        'models': ['command-r']
    }
}

# Fungsi untuk mendapatkan respons AI
@lru_cache(maxsize=100)
def get_cached_response(message, provider, model_name):
    timestamp = int(time.time()) // 3600
    return _get_ai_response(message, provider, model_name, timestamp)

def _get_ai_response(message, provider, model_name, _timestamp=None):
    if provider not in MODELS:
        raise ValueError(f'Provider {provider} not supported')

    provider_config = MODELS[provider]
    
    if model_name not in provider_config['models']:
        raise ValueError(f'Model {model_name} not available for {provider}')
        
    api_key = provider_config['api_key']
    handler = provider_config['handler_function']
    
    if not api_key:
        raise ValueError(f'API key for {provider} not configured')

    try:
        # Panggil fungsi handler yang sesuai
        ai_response = handler(api_key=api_key, message=message, model_name=model_name)
        return ai_response
    except Exception as e:
        print(f"Error calling {provider} API via handler: {str(e)}")
        raise

@app.route('/')
def index():
    all_models = []
    for provider, config in MODELS.items():
        for model_id in config['models']:
            all_models.append({
                'provider': provider,
                'model': model_id,
                'display_name': f'{provider}: {model_id}'
            })
    return render_template('index.html', models=all_models)

@app.route('/api/chat', methods=['POST'])
def chat():
    # Mendukung baik JSON maupun form data
    if request.is_json:
        data = request.get_json()
        message = data.get('message')
        provider = data.get('provider')
        model_name = data.get('model')
    else:
        message = request.form.get('message')
        provider_model = request.form.get('provider_model')
        if provider_model:
            provider, model_name = provider_model.split('|')
        else:
            provider, model_name = None, None
    
    if not message or not provider or not model_name:
        return jsonify({'error': 'Missing required fields'}), 400
    
    try:
        ai_response = get_cached_response(message, provider, model_name)
        
        return jsonify({
            'response': ai_response,
            'provider': provider,
            'model': model_name
        })
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

@app.route('/api/models')
def get_models():
    return jsonify(MODELS)

@app.route('/api/chat/stream', methods=['POST'])
def chat_stream():
    data = request.json
    
    if not data or 'message' not in data or 'provider' not in data or 'model' not in data:
        return jsonify({'error': 'Missing required fields'}), 400
    
    message = data['message']
    provider = data['provider']
    model_name = data['model']
    
    if provider not in MODELS:
        return jsonify({'error': f'Provider {provider} not supported'}), 400
    
    if model_name not in MODELS[provider]['models']:
        return jsonify({'error': f'Model {model_name} not available for {provider}'}), 400
    
    api_key = MODELS[provider]['api_key']
    
    if not api_key:
        return jsonify({'error': f'API key for {provider} not configured'}), 500
    
    # Implementasi streaming sederhana - mengembalikan respons penuh sebagai satu chunk
    def generate():
        try:
            ai_response = _get_ai_response(message, provider, model_name)
            # Kirim respons sebagai satu chunk
            yield f"data: {json.dumps({'content': ai_response})}\n\n"
            # Tandai selesai
            yield f"data: {json.dumps({'done': True})}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
    
    return Response(generate(), mimetype='text/event-stream')

if __name__ == '__main__':
    os.makedirs('templates', exist_ok=True)
    os.makedirs('handlers', exist_ok=True)
    app.run(debug=True)