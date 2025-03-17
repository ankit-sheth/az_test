
FROM python:3.8-slim-buster


COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

WORKDIR /app
COPY . /app

## for env variables - to show as an example
ENV secret=123 
ENV algorithm=HS256

EXPOSE 5001

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5001"]