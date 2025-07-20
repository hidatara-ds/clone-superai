import json
from flask import Flask, request, jsonify, render_template, Response
import requests
import os
from dotenv import load_dotenv
import time
from functools import lru_cache

# Load environment variables
load_dotenv()

# Get API keys from environment variables
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
# OPENROUTER_API_KEY=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

app = Flask(__name__)

# Cache untuk menyimpan respons
# Maksimal 100 item, dengan waktu kedaluwarsa 1 jam
@lru_cache(maxsize=100)
def get_cached_response(message, provider, model_name):
    # Tambahkan timestamp untuk memastikan cache kedaluwarsa setelah 1 jam
    timestamp = int(time.time()) // 3600
    return _get_ai_response(message, provider, model_name, timestamp)

def _get_ai_response(message, provider, model_name, _timestamp=None):
    # Prepare the request based on the provider
    api_url = MODELS[provider]['api_url']
    headers = MODELS[provider]['headers']
    
    # Prepare the payload
    payload = {
        'model': model_name,
        'messages': [
            {'role': 'user', 'content': message}
        ],
        'temperature': 0.7
    }
    
    response = requests.post(api_url, headers=headers, json=payload)
    response.raise_for_status()
    
    result = response.json()
    
    # Extract the response text
    if 'choices' in result and len(result['choices']) > 0:
        if 'message' in result['choices'][0]:
            ai_response = result['choices'][0]['message']['content']
        else:
            ai_response = result['choices'][0]['text']
    else:
        ai_response = 'No response generated.'
    
    return ai_response

# Available models configuration - hanya menggunakan model gratis
MODELS = {
    'openrouter': {
        'api_url': 'https://openrouter.ai/api/v1/chat/completions',
        'headers': {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {OPENROUTER_API_KEY}',
            'HTTP-Referer': 'http://localhost:5000',  # Required by OpenRouter
            'X-Title': 'AI Chat Bot'  # Optional but recommended
        },
        'models': [
            'mistralai/mistral-7b-instruct',
            'mistralai/mistral-tiny',
            'undi95/toppy-m-7b',
            'google/gemini-flash-1.5'
        ]  
    }
}

@app.route('/')
def index():
    # Get all available models for the dropdown
    all_models = []
    for provider, config in MODELS.items():
        for model in config['models']:
            all_models.append({
                'provider': provider,
                'model': model,
                'display_name': f'{provider}: {model}'
            })
    
    return render_template('index.html', models=all_models)

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    
    if not data or 'message' not in data or 'provider' not in data or 'model' not in data:
        return jsonify({'error': 'Missing required fields'}), 400
    
    message = data['message']
    provider = data['provider']
    model_name = data['model']
    
    # Check if provider exists
    if provider not in MODELS:
        return jsonify({'error': f'Provider {provider} not supported'}), 400
    
    # Check if model exists for the provider
    if model_name not in MODELS[provider]['models']:
        return jsonify({'error': f'Model {model_name} not available for {provider}'}), 400
    
    try:
        # Gunakan fungsi cache untuk mendapatkan respons
        ai_response = get_cached_response(message, provider, model_name)
        
        return jsonify({
            'response': ai_response,
            'provider': provider,
            'model': model_name
        })
        
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'API request failed: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

@app.route('/api/models')
def get_models():
    return jsonify(MODELS)

@app.route('/api/chat/stream', methods=['GET'])
def chat_stream():
    message = request.args.get('message')
    provider = request.args.get('provider')
    model_name = request.args.get('model')
    
    if not message or not provider or not model_name:
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Check if provider exists
    if provider not in MODELS:
        return jsonify({'error': f'Provider {provider} not supported'}), 400
    
    # Check if model exists for the provider
    if model_name not in MODELS[provider]['models']:
        return jsonify({'error': f'Model {model_name} not available for {provider}'}), 400
    
    # Prepare the request based on the provider
    api_url = MODELS[provider]['api_url']
    headers = MODELS[provider]['headers']
    
    # Prepare the payload with streaming enabled
    payload = {
        'model': model_name,
        'messages': [
            {'role': 'user', 'content': message}
        ],
        'temperature': 0.7,
        'stream': True
    }
    
    def generate():
        try:
            response = requests.post(api_url, headers=headers, json=payload, stream=True)
            response.raise_for_status()
            
            token_count = 0
            
            for line in response.iter_lines():
                if line:
                    line = line.decode('utf-8')
                    if line.startswith('data: ') and not line.startswith('data: [DONE]'):
                        data = json.loads(line[6:])
                        if 'choices' in data and len(data['choices']) > 0:
                            if 'delta' in data['choices'][0] and 'content' in data['choices'][0]['delta']:
                                content = data['choices'][0]['delta']['content']
                                token_count += 1
                                yield f"data: {json.dumps({'content': content, 'token_count': token_count})}\n\n"
            
            yield f"data: {json.dumps({'done': True, 'token_count': token_count})}\n\n"
            
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
    
    return Response(generate(), mimetype='text/event-stream')

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    
    # Run the app
    app.run(debug=True)