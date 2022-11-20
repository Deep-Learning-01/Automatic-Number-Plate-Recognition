
FROM python:3.8.5-slim-buster

RUN apt-get update 

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

RUN apt-get install ffmpeg libsm6 libxext6  -y

CMD ["python3", "app.py"]