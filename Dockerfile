FROM python:slim
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 5700
CMD uvicorn api:app --host 0.0.0.0 --reload --port 5700