import React, { useEffect, useState, useCallback } from 'react';
import VideoCard from './VideoCard';
import './App.css';

const VideoList = () => {
    const [videos, setVideos] = useState([]);
    const [page, setPage] = useState(1);
    const [limit] = useState(10); // Assuming limit is fixed; change if needed
    const [totalPages, setTotalPages] = useState(1);
    const [searchQuery, setSearchQuery] = useState(""); // Defined setSearchQuery with useState

    const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

    // Function to fetch videos with conditional URL based on search query
    const fetchVideos = useCallback(async (url) => {
        const response = await fetch(url);
        const data = await response.json();

        setVideos(data.videos);
        const totalCount = data.total_count;
        setTotalPages(Math.ceil(totalCount / limit));
    }, [limit]);

    useEffect(() => {
        const url = searchQuery 
            ? `${API_URL}/api/videos/search?query=${searchQuery}&page=${page}&limit=${limit}`
            : `${API_URL}/api/videos_detail?page=${page}&limit=${limit}`;
        fetchVideos(url);
    }, [fetchVideos, searchQuery, page, limit, API_URL]); // Added limit as a dependency

    // Search handler
    const handleSearch = (e) => {
        e.preventDefault();
        setPage(1); // Reset to first page for new search
    };

    // Reset handler to call video_details API directly
    const handleReset = () => {
        setSearchQuery("");
        setPage(1);
        fetchVideos(`${API_URL}/api/videos_detail?page=1&limit=${limit}`); // Explicitly call video_details API
    };

    return (
        <div className="video-list">
            <h1>Video List</h1>
            <div className="search-bar">
                <input 
                    type="text" 
                    placeholder="Search videos..." 
                    value={searchQuery} 
                    onChange={(e) => setSearchQuery(e.target.value)} 
                />
                <button onClick={handleSearch}>Search</button>
                <button onClick={handleReset}>Reset</button>
            </div>
            <div className="video-grid">
                {videos.map(video => (
                    <VideoCard key={video.video_id} video={video} />
                ))}
            </div>
            <div className="pagination">
                <button onClick={() => setPage(prev => Math.max(prev - 1, 1))} disabled={page === 1}>Previous</button>
                {Array.from({ length: totalPages }, (_, i) => (
                    <button 
                        key={i} 
                        className={page === i + 1 ? 'active' : ''}
                        onClick={() => setPage(i + 1)}
                    >
                        {i + 1}
                    </button>
                ))}
                <button onClick={() => setPage(prev => Math.min(prev + 1, totalPages))} disabled={page === totalPages}>Next</button>
            </div>
        </div>
    );
};

export default VideoList;
