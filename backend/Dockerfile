FROM python:3.12

WORKDIR /app

ADD . .

RUN pip install -r requirement.txt

EXPOSE 8888

CMD ["uvicorn","main:app", "--port", "8888", "--host", "0.0.0.0"]
