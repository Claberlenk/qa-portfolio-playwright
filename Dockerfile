FROM mcr.microsoft.com/playwright/python:v1.50.0-jammy

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Run all tests by default; override CMD to target a subset
CMD ["pytest", "--tb=short", "-v"]
