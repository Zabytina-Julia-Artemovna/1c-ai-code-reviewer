# 1. Берем готовый образ Ollama (он уже содержит саму Ollama)
FROM ollama/ollama:latest

# 2. Устанавливаем Python и pip внутри этого образа
RUN apt-get update && apt-get install -y python3 python3-pip curl zstd && \
    rm -rf /var/lib/apt/lists/*

# 3. Копируем наш скрипт
COPY review.py /app/review.py

# 4. Устанавливаем библиотеки Python
RUN pip install requests python-dotenv --break-system-packages

# 5. Открываем порт
EXPOSE 11434

# 6. Запускаем Ollama в фоне и наш скрипт
ENTRYPOINT ["/bin/sh", "-c", "ollama serve & sleep 5 && ollama pull deepseek-coder:1.3b && python3 /app/review.py"]
