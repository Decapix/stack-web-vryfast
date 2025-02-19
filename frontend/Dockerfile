# frontend/Dockerfile
FROM python:3.13-alpine3.21
WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install  -r requirements.txt

COPY . .

CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
