from python:3.11-alpine

WORKDIR /usr/src/app

COPY ./requirements.txt .
RUN pip install -r ./requirements.txt
COPY ./server ./server

EXPOSE 8000

CMD ["uvicorn", "server.server:app", "--reload", "--host", "0.0.0.0"]
