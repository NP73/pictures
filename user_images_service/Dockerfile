FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

WORKDIR /usr/src/app

COPY . .
RUN apt-get update 
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN pip install --upgrade pip
RUN pip install -r requirements.txt