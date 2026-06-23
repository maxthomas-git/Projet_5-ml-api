FROM python:3.11

WORKDIR /app

COPY . /app

RUN pip install uv
RUN uv sync

EXPOSE 7860

CMD ["uv", "run", "uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "7860"]
