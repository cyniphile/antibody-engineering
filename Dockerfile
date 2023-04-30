FROM python:3.10

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
ENV DOCKER_ENV_DATA_PROJECT=true

COPY . .

EXPOSE 4200
EXPOSE 8888
EXPOSE 5000