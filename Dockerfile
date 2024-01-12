FROM python:3.10

EXPOSE 8094

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir --upgrade pip

RUN pip install -r requirements.txt

COPY . /app

CMD ["gunicorn", "-w", "4" ,"--bind" ,"0.0.0.0:8094", "wsgi:app"]