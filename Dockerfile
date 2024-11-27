FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy the app code
COPY app ./app

# Expose the port
EXPOSE 8000

# Run the FastAPI app
CMD ["python", "app/main.py"]
