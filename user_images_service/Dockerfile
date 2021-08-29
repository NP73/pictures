FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

WORKDIR /usr/src/app

COPY . .
RUN apt-get update
RUN apt install -y libgl1-mesa-glx
RUN pip install --upgrade pip
RUN pip install -r requirements.txt