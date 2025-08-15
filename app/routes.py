import os

from app import app
from app.email import send_email_to_admin
from flask import Flask, request, jsonify, send_from_directory, abort
from datetime import datetime

FILES_DIR = "./files"

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World! This is a Flask app in Docker!"


@app.route('/send_email', methods=['POST'])
def send_email_endpoint():
    try:
        data = request.json

        if not all(key in data for key in ['name', 'description', 'contacts']):
            return jsonify({'error': 'Необходимы name, description и contacts'}), 400

        # Отправляем письмо себе (дата будет определена внутри функции)
        send_email_to_admin(
            name=data['name'],
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

@app.route('/download', methods=['GET'])
def download_file():
    # Получаем имя файла из параметров запроса
    filename = request.args.get('filename')

    if not filename:
        return jsonify({"error": "Не указано имя файла"}), 400

    # Безопасная проверка — чтобы нельзя было запросить файлы вне папки
    if ".." in filename or filename.startswith("/"):
        return jsonify({"error": "Некорректное имя файла"}), 400

    # Проверяем, что файл существует
    filepath = os.path.join(FILES_DIR, filename)
    if not os.path.exists(filepath):
        abort(404, description="Файл не найден")

    # Отправляем файл пользователю
    return send_from_directory(FILES_DIR, filename, as_attachment=True)