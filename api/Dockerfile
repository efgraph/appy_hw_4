FROM python:3.11-slim


WORKDIR /api
RUN mkdir -p /generated

RUN apt-get update && apt-get --yes upgrade

COPY requirements.txt requirements.txt
RUN  pip install --upgrade pip && pip install -r requirements.txt --no-cache-dir

COPY . .

RUN chmod +x /api/docker-entrypoint.sh
RUN chmod +x /api/wait-for-it.sh

ENTRYPOINT sh /api/docker-entrypoint.sh

EXPOSE 8000