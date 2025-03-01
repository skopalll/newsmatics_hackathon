
# backend/Dockerfile
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose the port your API uses (for example, 8000)
EXPOSE 8000

# Start the API (adjust according to your framework)
CMD ["python", "app.py"]

