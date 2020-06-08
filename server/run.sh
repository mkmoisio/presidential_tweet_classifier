docker build -t nlp-backend .
docker run -d --rm -p 5000:5000 --name tweet-classifier nlp-backend:latest
