import React from 'react';
import './VideoCard.css';

const VideoCard = ({ video }) => {
    const youtubeUrl = `https://www.youtube.com/watch?v=${video.video_id}`;

    return (
        <a href={youtubeUrl} target="_blank" rel="noopener noreferrer" className="video-card-link">
            <div className="video-card">
                <img src={video.thumbnail_url} alt={video.title} className="thumbnail" />
                <div className="video-info">
                    <h3 className="video-title">{video.title}</h3>
                </div>
            </div>
        </a>
    );
};

export default VideoCard;
