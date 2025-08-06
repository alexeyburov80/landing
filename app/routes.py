from app import app
from app.email import send_email_to_admin
from flask import request, jsonify
from datetime import datetime

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World! This is a Flask app in Docker!"


@app.route('/send_email', methods=['POST'])
def send_email_endpoint():
    try:
        data = request.json

        if not all(key in data for key in ['description', 'contacts']):
            return jsonify({'error': 'Необходимы description и contacts'}), 400

        # Отправляем письмо себе (дата будет определена внутри функции)
        send_email_to_admin(
            description=data['description'],
            contacts=data['contacts']
        )

        return jsonify({
            'message': 'Письмо успешно отправлено администратору',
            'status': 'success'
        }), 200

    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Ошибка сервера: {str(e)}'}), 500