# 🎥 FamPay Video Fetcher API

Welcome to the **FamPay Video Fetcher API**! This project is designed to seamlessly fetch, store, and serve the latest YouTube videos based on user-defined queries. With a powerful backend and a sleek frontend, this application aims to deliver an efficient and user-friendly experience.

## 🚀 Project Highlights

- **Continuous Video Fetching**: The server pulls the latest videos from YouTube every 10 seconds, ensuring you have the freshest content at your fingertips.
- **Efficient Data Storage**: Using **PostgreSQL** for relational database management allows for robust data handling and efficient indexing through B-tree, making searches quick and reliable.
- **Paginated API Endpoints**: Easily access the stored videos with pagination, ensuring smooth navigation through large datasets.
- **Smart Search Functionality**: Search for videos using partial matches in titles or descriptions, making it easier to find exactly what you need.
- **Dockerized for Convenience**: Run the entire application effortlessly using Docker, allowing for easy deployment and scalability.

## 🛠️ Tech Stack

- **Backend**: Python with Flask
- **Frontend**: React
- **Database**: PostgreSQL

## 📦 Getting Started

### 1. Clone the Repository

To get started with the project, clone the repository using the following command:

```bash
git clone <your-repo-url>
cd <your-repo-directory>

To run the service 

```bash
docker-compose up -d
