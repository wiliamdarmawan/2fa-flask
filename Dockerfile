FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy and install dependencies first
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app files
COPY . .

# Expose the application port
EXPOSE 5001

# Start the Flask app
CMD ["python", "main.py"]