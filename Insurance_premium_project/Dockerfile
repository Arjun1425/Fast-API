FROM python:3.11-slim

WORKDIR /app

COPY requirements_pip.txt .

RUN pip install --no-cache-dir -r requirements_pip.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0", "--port", "8000"]