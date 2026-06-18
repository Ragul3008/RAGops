FROM python:3.12-slim
RUN apt-get install -y libgomp1
WORKDIR /app
COPY pyproject.toml .
RUN pip install --no-cache-dir -e ".[gpu]"
COPY . .
EXPOSE 8001
CMD ["uvicorn","app.main:app","--workers","4"]