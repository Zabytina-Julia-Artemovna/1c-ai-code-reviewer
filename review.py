import requests
import json
import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

load_dotenv()
code_1c = """
Процедура ОбработкаПроведения(Отказ, Режим)
    Для Каждого Строка Из Товары Цикл
        Запрос = Новый Запрос;
        Запрос.Текст = "ВЫБРАТЬ * ИЗ Справочник.Номенклатура ГДЕ Ссылка = &Строка";
        Запрос.УстановитьПараметр("Строка", Строка.Номенклатура);
        Результат = Запрос.Выполнить().Выбрать();
    КонецЦикла;
КонецПроцедуры
"""

prompt = f"""Ты эксперт по 1С. Проанализируй этот код и найди все проблемы:

{code_1c}

Перечисли ошибки по пунктам. Обрати внимание на:
- Производительность (запросы в циклах)
- Проверки на пустые ссылки
- Отсутсвие транзакций
- Стиль кода
"""


print("Отправляю код на проверку...")

try:
    response = requests.post(
        'http://localhost:11434/api/generate',
        json={
            'model': 'deepseek-coder:1.3b',
            'prompt': prompt,
            'stream': False
        },
        timeout=600
    )
    result = response.json()['response']

except requests.exceptions.ConnectionError:
    print(" Ошибка: Не удаётся подключиться к Ollama.")
    print("Проверь, что Ollama запущена (команда: ollama serve)")
except Exception as e:
    print(f" Произошла ошибка: {e}")

def send_email(report_text):
    sender = "uzabytina9@gmail.com"
    password = os.getenv("EMAIL_PASSWORD")
    recipient = "uzabytina9@gmail.com"

    msg = MIMEText(report_text)
    msg['Subject'] = "Результат ИИ-ревью кода 1С"
    msg['From'] = sender
    msg['To'] = recipient

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender, password)
            server.send_message(msg)
        print("Письмо отправлено!")
    except Exception as e:
        print(f"Ошибка отправки почты: {e}")

send_email(result)