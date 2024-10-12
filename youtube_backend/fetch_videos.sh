#!/bin/bash

# Define the API endpoint
API_URL="http://localhost:5000/api/videos?query=cricket"  # Update this URL if needed

# Make a GET request to the API
response=$(curl -s -o /dev/null -w "%{http_code}" $API_URL)

# Check if the request was successful
if [ "$response" -eq 200 ]; then
    echo "Video data fetched successfully."
else
    echo "Failed to fetch video data. HTTP Status Code: $response"
fi
