FROM python:3.9-slim
WORKDIR /app

COPY . /app

RUN if [ -f "requirements.txt" ]; then pip install --no-cache-dir -r requirements.txt; fi

EXPOSE 5000

CMD ["python", "ServeurTaches.py"]