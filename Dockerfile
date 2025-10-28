# Step 1: Use a slim and specific Python version as the base image
FROM python:3.10-slim

# Step 2: Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Step 3: Set the working directory inside the container
WORKDIR /app

# Step 4: Copy only the dependency file first to leverage Docker layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Copy your entire project into the working directory

COPY . .

# Step 6: Expose the port Streamlit runs on
EXPOSE 8501

# Step 7: Define the command to run your application from its sub-directory

CMD ["streamlit", "run", "app/app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true"]