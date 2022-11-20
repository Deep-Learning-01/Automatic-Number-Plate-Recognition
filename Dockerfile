
FROM python:3.9

RUN pip install --upgrade pip

RUN apt-get update 

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

CMD ["python3", "app.py"]