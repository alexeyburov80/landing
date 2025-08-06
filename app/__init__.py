from flask import Flask
from flask_mail import Mail

app = Flask(__name__)

# Конфигурация (лучше вынести в отдельный config.py)
app.config.update(
    MAIL_SERVER='smtp.mail.ru',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USERNAME='aux80@mail.ru',
    MAIL_DEFAULT_SENDER=('Имя отправителя', 'aux80@mail.ru'),
    MAIL_PASSWORD='FXMXbjhcL7ynIpMVQ5Km',
    ADMIN_EMAIL='aux80@mail.ru'
)

mail = Mail(app)

from app import routes

# for example
# curl -X POST http://localhost:5000/send_email \
#   -H "Content-Type: application/json" \
#   -d '{
#     "description": "Тестовое письмо",
#     "contacts": ["user1@example.com", "user2@example.com"],
#     "send_date": "2023-12-31 12:00:00"
#   }'