# Dockerfile for Backend
FROM python:3.7

# Set the working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

RUN apt-get update && apt-get install -y cron 

RUN apt-get install -y vim


# Expose the port the app runs on
EXPOSE 5000

# Run the app
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000", "--reload"]

