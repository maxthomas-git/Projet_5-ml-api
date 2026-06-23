FROM python:3.10

WORKDIR /app

COPY . /app

ENV PYTHONPATH=.

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 7860

CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "7860"]
