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

# Give execution rights on the fetch_videos.sh script
RUN chmod +x /app/fetch_videos.sh

# Add crontab file in the cron directory
COPY crontab /etc/cron.d/fetch_videos_cron

# Apply cron job
RUN crontab /etc/cron.d/fetch_videos_cron

# Create the log file to be able to run tail
RUN touch /var/log/cron.log

# Start the cron and Flask app
CMD cron && python3 app.py

# Expose the port the app runs on
EXPOSE 5000

# Run the app
CMD ["python", "app.py"]
