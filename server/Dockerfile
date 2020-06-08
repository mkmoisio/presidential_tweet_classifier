FROM python:latest

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt
RUN python -m spacy download en_core_web_sm

WORKDIR /app
COPY . /app
EXPOSE 5000
CMD ["python", "app.py"]
