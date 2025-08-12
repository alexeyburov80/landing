from flask_mail import Message
from datetime import datetime
from app import mail
from flask import current_app
import request


def send_email_to_admin(description, contacts):
    """Отправляет письмо на админский ящик с данными из формы"""

    # Получаем IP пользователя
    user_ip = request.headers.get('X-Forwarded-For', request.remote_addr)

    try:
        # Валидация данных
        if len(description) > 256:
            raise ValueError("Описание превышает 256 символов")

        if not isinstance(contacts, list):
            raise ValueError("Контакты должны быть списком")

        # Текущая дата и время на сервере
        send_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Формируем текст письма для админа
        email_body = f"""
        Новый запрос на отправку письма:

        Описание: {description}
        Контакты: {', '.join(contacts)}
        Дата отправки (серверное время): {send_date}
        Айпи: {user_ip}
        
        ---
        Это письмо сгенерировано автоматически
        """

        # Получаем админский ящик из конфига
        admin_email = current_app.config.get('ADMIN_EMAIL', 'admin@example.com')

        # Создаем и отправляем письмо
        msg = Message(
            subject=f"Запрос на отправку письма ({send_date})",
            recipients=[admin_email],
            body=email_body
        )

        mail.send(msg)
        return True

    except Exception as e:
        current_app.logger.error(f"Ошибка отправки письма: {str(e)}")
        raise
