from flask import Blueprint, render_template, request, jsonify
from app.models.message import Message
from app import db
import os
import time

# Create blueprint
chat_bp = Blueprint('chat', __name__)

# Import LLM service
from app.services.llm_service import get_llm_response, get_available_models

@chat_bp.route('/')
def index():
    """Render the chat interface"""
    # Get chat history from database
    messages = Message.query.order_by(Message.timestamp.asc()).all()
    
    # Get available models
    available_models = get_available_models()
    
    return render_template('chat.html', messages=messages, available_models=available_models)

@chat_bp.route('/send', methods=['POST'])
def send_message():
    """Handle sending a message"""
    # Get message content and selected model from form
    content = request.form.get('content')
    selected_model = request.form.get('model', 'auto')
    
    if not content:
        return jsonify({'error': 'Message cannot be empty'}), 400
    
    # Save user message to database
    user_message = Message(content=content, sender='user')
    db.session.add(user_message)
    db.session.commit()
    
    try:
        # Get response from LLM service
        ai_response = get_llm_response(content, selected_model)
        
        # Save AI response to database
        ai_message = Message(content=ai_response, sender='ai')
        db.session.add(ai_message)
        db.session.commit()
        
        return jsonify({
            'user_message': {
                'content': content,
                'timestamp': time.time()
            },
            'ai_message': {
                'content': ai_response,
                'timestamp': time.time()
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@chat_bp.route('/clear', methods=['POST'])
def clear_chat():
    """Clear chat history"""
    try:
        # Delete all messages from database
        Message.query.delete()
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500