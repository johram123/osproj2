FROM python:3.12.1-slim

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y sqlite3 && \ 
    pip install --no-cache-dir -r requirements.txt 
    

EXPOSE 5000

CMD ["python", "app.py"]
