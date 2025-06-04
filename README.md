# Chatbot Web Application

Welcome to the Chatbot Web Application! This project is a simple Flask-based web application that allows users to interact with various AI language models from OpenAI and other providers. With just a few clicks, you can generate responses to your prompts using some of the most sophisticated AI models available.

## Features

- **User-Friendly Interface**: Easily input prompts and choose different AI models through a web interface.
- **Model Variety**: Select from a range of preconfigured models, including:
  - OpenAI GPT-3.5 Turbo
  - Mistral 7B Instruct
  - Hugging Face Mistral 7B
  - Meta's Llama 2 7B Chat
  - Anthropic Claude 3 Haiku
- **Real-time Responses**: Get instant responses based on the selected model and input prompt.

## Getting Started

### Prerequisites

Before you begin, ensure you have Python installed on your machine along with Flask and the OpenAI SDK. You may also need to sign up for an API key from OpenRouter or whichever provider you choose.

### Installation

1. **Clone the repository**: 
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Install dependencies**: 
   ```bash
   pip install Flask openai
   ```

3. **Update your API key**:  
   Replace the placeholder API key in the code with your own key:  
   ```python
   api_key="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"  # Ganti dengan API key kamu
   ```

### Running the Application

To run the application, execute the following command in your terminal:  
```bash
python app.py
```

Then open your web browser and navigate to `http://127.0.0.1:5000` to access the application.

### Using the Application

1. **Input your prompt**: Type your question or statement in the text box provided.
2. **Select a model**: Choose from the available AI models in the dropdown menu.
3. **Get a response**: Hit the submit button to receive a generated response from the selected model.

## Code Explanation

Here's a brief overview of the code:

- **Flask Initialization**: The application is initialized with Flask, and an OpenAI client is created with your API key.
- **Model List**: A predefined list of available AI models is set for users to select from.
- **Main Route**: The main route (`/`) handles both GET and POST requests. When a user submits a prompt, it sends the information to the chosen model and retrieves the response to render on the page.

## Contributing

If you'd like to contribute to this project, feel free to fork the repository and submit a pull request. All contributions are welcome!

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

Thanks to [Flask](https://flask.palletsprojects.com/) and [OpenAI](https://openai.com/) for providing the frameworks and APIs that made this project possible.

---

Feel free to customize the content of this README to better fit your project's identity!
