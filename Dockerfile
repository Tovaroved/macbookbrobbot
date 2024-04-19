FROM python:3.11-alpine

WORKDIR /app
RUN apk add --no-cache gcc

COPY req.txt /app/
RUN pip install -r req.txt

COPY . /app/

EXPOSE 5000

CMD ["./docker.sh"]