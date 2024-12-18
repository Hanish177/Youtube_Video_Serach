from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime, timedelta
import pytz
import requests
import psycopg2
from psycopg2.extras import execute_values
from psycopg2 import OperationalError,sql
import os

app = Flask(__name__)
CORS(app, origins="*")

# PostgreSQL database configuration
db_config = {
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),  # This should now point to the "db" service
    'port': os.getenv('DB_PORT'),
    'dbname': os.getenv('DB_NAME')
}

try:
    connection = psycopg2.connect(**db_config)
    print("database Connection successful")
    connection.close()
except OperationalError as e:
    print("Error while connecting to PostgreSQL", e)

@app.route('/api/health', methods=['GET'])
def health():
    return 'good health'

def create_database():
    # Connect to the PostgreSQL server
    conn = psycopg2.connect(user=db_config['user'], password=db_config['password'], host=db_config['host'], port=db_config['port'])
    conn.autocommit = True  # Enable autocommit to create the database
    cursor = conn.cursor()
    
    try:
        # Check if the database already exists
        cursor.execute(sql.SQL("SELECT 1 FROM pg_database WHERE datname = %s"), [db_config['dbname']])
        exists = cursor.fetchone()
        
        if not exists:
            # Create the database if it doesn't exist
            cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_config['dbname'])))
            print(f"Database '{db_config['dbname']}' created successfully.")
        else:
            print(f"Database '{db_config['dbname']}' already exists. No need to create.")
    except Exception as e:
        print(f"Error creating database: {e}")
    finally:
        cursor.close()
        conn.close()

def create_table():
    # Connect to the specified database
    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()
    
    # Define the table name and columns
    table_name = "videos"
    columns = {
        "video_id": "VARCHAR(50) PRIMARY KEY NOT NULL",
        "title": "TEXT",
        "description": "TEXT",
        "published_at": "TIMESTAMP WITHOUT TIME ZONE",
        "thumbnail_url": "TEXT",
        "tags": "TEXT[]"
    }

    # SQL statement to check if the table exists
    check_table_exists_query = sql.SQL("""
        SELECT EXISTS (
            SELECT 1 
            FROM information_schema.tables 
            WHERE table_name = {table}
        );
    """).format(table=sql.Literal(table_name))

    # SQL statement to create the table if it doesn't exist
    create_table_query = sql.SQL("CREATE TABLE {table} ({fields});").format(
        table=sql.Identifier(table_name),
        fields=sql.SQL(", ").join(
            sql.SQL("{} {}").format(sql.Identifier(col), sql.SQL(dtype)) for col, dtype in columns.items()
        )
    )

    try:
        # Check if the table exists
        cursor.execute(check_table_exists_query)
        exists = cursor.fetchone()[0]
        
        if not exists:
            # Create the table if it doesn't exist
            cursor.execute(create_table_query)
            conn.commit()
            print("Table 'videos' created successfully.")
        else:
            print("Table 'videos' already exists. No need to create.")
    except Exception as e:
        print(f"Error creating table: {e}")
    finally:
        cursor.close()
        conn.close()



@app.route('/api/videos', methods=['GET'])
def get_videos():
    query = request.args.get('query', 'cricket')  # Default to 'cricket'
    api_key = os.getenv('API_KEY')  # Replace with your actual API key
    search_url = "https://www.googleapis.com/youtube/v3/search"
    video_details_url = "https://www.googleapis.com/youtube/v3/videos"

    # Step 1: Fetch video IDs
    now = datetime.now(pytz.UTC)
    published_after = now - timedelta(days=7)
    # Format datetime in ISO 8601 format as required by YouTube API
    published_after_str = published_after.isoformat()
    search_params = {
        "part": "snippet",
        "q": query,
        "type": "video",
        "order": "date",  # Sort by date to get latest videos
        "maxResults": 50,
        "publishedAfter": published_after_str,
        "fields": "items(id/videoId,snippet/publishedAt)",  # Added publishedAt to verify dates
        "key": api_key
    }
    search_response = requests.get(search_url, params=search_params)
    video_ids = [item["id"]["videoId"] for item in search_response.json().get("items", [])]

    # Step 2: Fetch video details
    if video_ids:
        details_params = {
            "part": "snippet",
            "id": ",".join(video_ids),
            "fields": "items(id,snippet/title,snippet/description,snippet/publishedAt,snippet/thumbnails/high/url,snippet/tags)",
            "key": api_key
        }
        details_response = requests.get(video_details_url, params=details_params)
        if details_response.status_code == 200:
            videos = details_response.json().get("items", [])
            print("Video details fetched successfully")
        else:
            print("Error fetching video details:", details_response.status_code, details_response.text)
        videos = details_response.json().get("items", [])

        # Step 3: Store video details in PostgreSQL
        with psycopg2.connect(**db_config) as conn:
            with conn.cursor() as cur:
                video_data = [
                    (
                        video["id"],
                        video["snippet"]["title"],
                        video["snippet"]["description"],
                        video["snippet"]["publishedAt"],
                        video["snippet"]["thumbnails"]["high"]["url"],
                        video["snippet"].get("tags", [])
                    )
                    for video in videos
                ]
                insert_query = """
                    INSERT INTO videos (video_id, title, description, published_at, thumbnail_url, tags)
                    VALUES %s
                    ON CONFLICT (video_id) DO NOTHING;
                """
                try:
                    execute_values(cur, insert_query, video_data)
                    print("insert query work fine")
                except Exception as e:
                    print(f"Error inserting data: {e}")
            conn.commit()
    return "data storage is complete"

@app.route('/api/videos_detail', methods=['GET'])
def get_videos_details():
    page = request.args.get('page', 1, type=int)  # Current page, default is 1
    limit = request.args.get('limit', 10, type=int)  # Number of records per page, default is 10

    offset = (page - 1) * limit  # Calculate the offset for pagination

    # Connect to the PostgreSQL database
    with psycopg2.connect(**db_config) as conn:
        with conn.cursor() as cur:

            cur.execute("SELECT COUNT(*) FROM videos;")
            total_count = cur.fetchone()[0]

            if total_count == 0:
                # If no records exist, fetch and store video data
                response_message = get_videos()  # Call your function to fetch and store videos
                print(response_message)
            else:
                print("table in not empty :",total_count)

            # Step 1: Retrieve video details from PostgreSQL
            select_query = """
                SELECT video_id, title, description, published_at, thumbnail_url, tags
                FROM videos
                ORDER BY published_at DESC
                LIMIT %s OFFSET %s;
            """
            cur.execute(select_query, (limit, offset))
            rows = cur.fetchall()

            # Step 2: Format the response
            videos = []
            for row in rows:
                video = {
                    "video_id": row[0],
                    "title": row[1],
                    "description": row[2],
                    "published_at": row[3],
                    "thumbnail_url": row[4],
                    "tags": row[5]
                }
                videos.append(video)

            # Step 3: Get the total count of videos for pagination metadata
            cur.execute("SELECT COUNT(*) FROM videos;")
            total_count = cur.fetchone()[0]

    # Step 4: Create the paginated response
    response = {
        "page": page,
        "limit": limit,
        "total_count": total_count,
        "videos": videos
    }
    return jsonify(response)

@app.route('/api/videos/search', methods=['GET'])
def search_videos():
    # Get the search query, page, and limit from request parameters
    query = request.args.get('query', '')
    page = request.args.get('page', 1, type=int)  # Default to page 1
    limit = request.args.get('limit', 10, type=int)  # Default limit of 10 results per page

    if not query:
        return jsonify({"message": "Search query cannot be empty"}), 400

    offset = (page - 1) * limit  # Calculate offset for pagination

    # Split the search query into individual keywords
    keywords = query.split()
    like_clauses = []
    params = []

    # Construct the LIKE clauses for each keyword
    for word in keywords:
        like_clauses.append("LOWER(title) LIKE LOWER(%s) OR LOWER(description) LIKE LOWER(%s)")
        params.extend([f"%{word}%", f"%{word}%"])

    # Join the LIKE clauses with AND for requiring all keywords to match
    where_clause = " AND ".join(like_clauses)

    # Connect to the PostgreSQL database
    with psycopg2.connect(**db_config) as conn:
        with conn.cursor() as cur:
            # Step 1: Retrieve count of total matching records for pagination
            count_query = f"""
                SELECT COUNT(*)
                FROM videos
                WHERE {where_clause};
            """
            cur.execute(count_query, tuple(params))
            total_count = cur.fetchone()[0]

            # Step 2: Retrieve paginated video details matching the search query in descending order by published_at
            search_query = f"""
                SELECT video_id, title, description, published_at, thumbnail_url, tags
                FROM videos
                WHERE {where_clause}
                ORDER BY published_at DESC
                LIMIT %s OFFSET %s;
            """
            params.extend([limit, offset])  # Add limit and offset to params
            cur.execute(search_query, tuple(params))
            rows = cur.fetchall()

            # Step 3: Format the response with the paginated results
            videos = []
            for row in rows:
                video = {
                    "video_id": row[0],
                    "title": row[1],
                    "description": row[2],
                    "published_at": row[3],
                    "thumbnail_url": row[4],
                    "tags": row[5]
                }
                videos.append(video)

    # Step 4: Create and return the paginated response
    response = {
        "page": page,
        "limit": limit,
        "total_count": total_count,
        "videos": videos
    }
    return jsonify(response)


if __name__ == '__main__':
    create_database()
    create_table()
    app.run(host='0.0.0.0', port=5000)
