import React, { useEffect, useState, useCallback } from 'react';
import VideoCard from './VideoCard';
import './App.css';

const VideoList = () => {
    const [videos, setVideos] = useState([]);
    const [page, setPage] = useState(1);
    const [limit] = useState(10);
    const [totalPages, setTotalPages] = useState(1);

    const fetchVideos = useCallback(async () => {
        const response = await fetch(`http://backend:5000/api/videos_detail?page=${page}&limit=${limit}`);
        const data = await response.json();
        console.log(" have data")
        setVideos(data.videos);

        const totalCount = data.total_count;
        setTotalPages(Math.ceil(totalCount / limit)); // Calculate total pages
    }, [page, limit]);

    useEffect(() => {
        fetchVideos();
    }, [fetchVideos]);

    return (
        <div className="video-list">
            <h1>Video List</h1>
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
