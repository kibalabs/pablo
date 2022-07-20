FROM python:3.9.2-slim

WORKDIR /app

COPY requirements-dev.txt $WORKDIR
RUN pip install -r requirements-dev.txt
COPY requirements.txt $WORKDIR
RUN pip install -r requirements.txt

COPY . $WORKDIR

EXPOSE 5000
CMD ["./start-api.sh"]
