FROM python:3.8-slim
RUN pip install gunicorn
RUN pip install psycopg2-binary
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD ["sh", "-c", "sleep 5 && gunicorn crud.wsgi:application --bind 0.0.0.0:8000"]
