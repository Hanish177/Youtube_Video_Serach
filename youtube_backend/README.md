# YouTube Video Search API

![YouTube Video Search](https://example.com/your-image-url.png) <!-- Replace with an actual image URL if available -->

## Overview

The **YouTube Video Search API** is a robust backend service designed to fetch and store the latest YouTube videos based on a given search query. The API supports pagination and allows users to search through stored video data using titles and descriptions. Built with **Python Flask** and utilizing **PostgreSQL** for data storage, this API is scalable, efficient, and dockerized for easy deployment.

## Features

- Fetches and stores the latest YouTube videos based on a predefined search query.
- Pagination support for retrieving video data.
- Basic search functionality for querying stored videos by title and description.
- Built-in handling for duplicate entries using PostgreSQL.
- Dockerized setup for easy deployment and scalability.
- Supports filtering and sorting options for search results.

## Technologies Used

- **Python** - Backend development with Flask.
- **PostgreSQL** - Relational database management for easy indexing and storage.
- **Docker** - Containerization for easy deployment.
- **Flask-CORS** - Enable Cross-Origin Resource Sharing for the frontend.
- **psycopg2** - PostgreSQL database adapter for Python.

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Hanish177/Youtube_Video_Serach.git
   cd Youtube_Video_Serach
   ```
2.  **To run the backend Only**
    ```bash
    python app.py
    ```
