FROM python:3.10
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FLASK_ENV=development
WORKDIR /app
ENV PYTHONPATH=/app
COPY . .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
