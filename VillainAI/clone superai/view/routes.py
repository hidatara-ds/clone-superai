from flask import Blueprint, render_template, request, jsonify
from config import AI_MODELS, get_openrouter_api_key
import requests

main = Blueprint('main', __name__)

DEFAULT_AUTO_MODEL_ID = "openrouter/mistralai/mistral-7b-instruct"

@main.route('/')
def index():
    return render_template('index.html', models=AI_MODELS)

@main.route('/submit', methods=['POST'])
def submit():
    prompt = request.form.get('prompt', '').strip()
    selected_model_id = request.form.get('model_id', 'auto')

    if not prompt:
        return jsonify({"error": "Prompt tidak boleh kosong.", "status": "error"}), 400

    actual_model_id = selected_model_id
    auto_selected = False

    if selected_model_id == 'auto':
        actual_model_id = DEFAULT_AUTO_MODEL_ID
        auto_selected = True
        if actual_model_id not in AI_MODELS:
            return jsonify({"error": "Model default untuk mode auto tidak valid.", "status": "error"}), 500

    if actual_model_id not in AI_MODELS:
        return jsonify({"error": "Pilihan model tidak valid.", "status": "error"}), 400

    model_config = AI_MODELS[actual_model_id]
    if model_config.get("api_provider") != "openrouter":
        return jsonify({"error": f"Model '{model_config['name']}' tidak dikonfigurasi untuk OpenRouter.", "status": "error"}), 500

    openrouter_api_key = get_openrouter_api_key()
    if not openrouter_api_key:
        return jsonify({"error": "OPENROUTER_API_KEY tidak dikonfigurasi di file .env.", "status": "error"}), 500

    try:
        openrouter_model_tag = model_config.get("openrouter_model_id")
        if not openrouter_model_tag:
            return jsonify({"error": f"Konfigurasi ID model OpenRouter hilang untuk {actual_model_id}", "status": "error"}), 500

        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {openrouter_api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": openrouter_model_tag,
            "messages": [{"role": "user", "content": prompt}]
        }
        response = requests.post(url, headers=headers, json=data, timeout=60)
        response.raise_for_status()
        result = response.json()
        ai_response = result["choices"][0]["message"]["content"].strip()
        return jsonify({
            "model_used": model_config["name"],
            "prompt": prompt,
            "response": ai_response,
            "auto_selected": auto_selected,
            "pricing_tier": model_config.get("pricing_tier", "N/A"),
            "status": "success"
        })
    except Exception as e:
        return jsonify({"error": f"Terjadi kesalahan: {str(e)}", "status": "error"}), 500