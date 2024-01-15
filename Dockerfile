FROM python:3.10

EXPOSE 8094

WORKDIR /app/geospatial_map_viewer

COPY . /app/geospatial_map_viewer

RUN pip install --no-cache-dir --upgrade pip

RUN pip install -r /app/geospatial_map_viewer/requirements.txt

RUN mkdir /app/geospatial_map_viewer/static/media

CMD ["gunicorn", "-w", "4" ,"--bind" ,"0.0.0.0:8094", "wsgi:app"]
