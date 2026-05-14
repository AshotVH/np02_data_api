FROM python:3.11
EXPOSE 8080
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["gunicorn", "--workers", "4", "--timeout", "60", "--bind", "0.0.0.0:8080", "main:app"]
