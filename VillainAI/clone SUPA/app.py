from flask import Flask, request, render_template
from openai import OpenAI

app = Flask(__name__)

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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"  # Ganti dengan API key kamu
)

AVAILABLE_MODELS = [
    "openai/gpt-3.5-turbo",
    "mistralai/mistral-7b-instruct",
    "huggingface/mistral-7b",
    "meta-llama/llama-2-7b-chat",
    "anthropic/claude-3-haiku"
]

@app.route("/", methods=["GET", "POST"])
def index():
    response = ""
    if request.method == "POST":
        user_input = request.form["prompt"]
        selected_model = request.form["model"]

        completion = client.chat.completions.create(
            model=selected_model,
            messages=[{"role": "user", "content": user_input}]
        )
        response = completion.choices[0].message.content

    return render_template("index.html", models=AVAILABLE_MODELS, response=response)
