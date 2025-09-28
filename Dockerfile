FROM python:3.11-slim

# Set envs
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create app dir
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Collect static files (optional if you serve from Django)
RUN python manage.py collectstatic --noinput || true

EXPOSE 8000
CMD ["uvicorn", "hr_backend.asgi:application", "--host", "0.0.0.0", "--port", "8000"]
