body {
    font-family: 'Inter', sans-serif, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue';
    background-color: #210033;
    color: #e0e0e0;
    margin: 0;
    padding: 0;
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    overflow-x: hidden;
    transition: background-color 0.5s ease-in-out;
    position: relative;
    z-index: 1;
}

body.player-active-bg {
    background-color: #1a002c;
}

body.detail-active-bg {
    background-color: #331A40;
}

.video-background-container {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    overflow: hidden;
    z-index: 0;
    opacity: 0;
    transition: opacity 0.7s ease-in-out;
}

.video-background-container.active {
    opacity: 1;
}

.video-background-container video {
    min-width: 100%;
    min-height: 100%;
    width: auto;
    height: auto;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    object-fit: cover;
}

.video-overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.6);
    z-index: 1;
}

.page {
    width: 100%;
    max-width: 800px;
    padding: 1rem;
    display: none;
    flex-direction: column;
    align-items: center;
    box-sizing: border-box;
    position: relative;
    z-index: 2;
    background-color: transparent;
}

.page.active {
    display: flex;
}

header {
    width: 100%;
    text-align: center;
    margin-bottom: 1.5rem;
    color: #ffffff;
}

header h1 {
    font-size: 2.5rem;
    font-weight: 700;
    letter-spacing: -0.5px;
}

.song-list {
    list-style: none;
    padding: 0;
    width: 100%;
    max-width: 600px;
}

.song-list li {
    background-color: #380056;
    padding: 1rem 1.5rem;
    margin-bottom: 0.75rem;
    border-radius: 0.75rem;
    cursor: pointer;
    transition: background-color 0.2s ease, transform 0.1s ease;
    display: flex;
    align-items: center;
    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
}

.song-list li:hover {
    background-color: #8a5cf647;
    transform: translateY(-2px);
}

.song-list .song-art-list {
    width: 50px;
    height: 50px;
    border-radius: 0.5rem;
    margin-right: 1rem;
    object-fit: cover;
}

.song-list .song-info-list h3 {
    margin: 0 0 0.25rem 0;
    font-size: 1.1rem;
    color: #ffffff;
}

.song-list .song-info-list p {
    margin: 0;
    font-size: 0.85rem;
    color: #b3b3b3;
}

.loading-songs {
    text-align: center;
    color: #a0a0a0;
    font-style: italic;
    background-color: transparent !important;
    box-shadow: none !important;
    cursor: default !important;
}

.loading-songs:hover {
    background-color: transparent !important;
    transform: none !important;
}

.back-btn {
    position: absolute;
    top: 1.5rem;
    left: 1.5rem;
    background-color: #3800563a;
    color: #fff;
    border: none;
    padding: 0.6rem 1rem;
    border-radius: 2rem;
    cursor: pointer;
    font-size: 0.9rem;
    z-index: 10;
    transition: background-color 0.2s ease;
}

.back-btn:hover {
    background-color: #380056;
}

.back-btn i {
    margin-right: 0.5rem;
}

.music-player-container {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 80%;
    height: 50%;
    min-height: 90vh;
    padding-top: 3rem;
}

.music-player-box {
    background: radial-gradient(circle at top left, #2e004d3b, #1a002c3a);
    border-radius: 3rem;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
    overflow: hidden;
    width: 100%;
    max-width: 400px;
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
}

.player-header {
    display: flex;
    align-items: center;
    margin-bottom: 1.5rem;
}

.album-art-player {
    width: 80px;
    height: 80px;
    border-radius: 0.5rem;
    margin-right: 1rem;
    object-fit: cover;
    box-shadow: 0 4px 10px rgba(0,0,0,0.3);
}

.track-info-player h2 {
    font-size: 1.4rem;
    font-weight: 600;
    margin: 0 0 0.25rem 0;
    color: #ffffff;
}

.track-info-player p {
    font-size: 0.9rem;
    color: #b3b3b3;
    margin: 0;
}

.lyrics-container {
    height: 180px;
    overflow-y: auto;
    background: radial-gradient(circle at top left, #2e004d43, #1a002c3d);
    padding: 1rem;
    border-radius: 0.5rem;
    margin-bottom: 1.5rem;
    line-height: 1.6;
    font-size: 0.95rem;
    color: #d0d0d0;
}

.lyrics-container::-webkit-scrollbar {
    width: 8px;
}

.lyrics-container::-webkit-scrollbar-track {
    background: #282828;
    border-radius: 10px;
}

.lyrics-container::-webkit-scrollbar-thumb {
    background: #380056;
    border-radius: 10px;
}

.lyrics-container::-webkit-scrollbar-thumb:hover {
    background: #5a5a6e;
}

.player-controls {
    margin-top: auto;
}

.progress-section-player {
    margin-bottom: 1rem;
}

.progress-bar-container-player {
    background-color: #404040;
    border-radius: 5px;
    cursor: pointer;
    height: 10px;
    width: 100%;
}

.progress-bar-player {
    background-color: #380056;
    width: 0%;
    height: 100%;
    border-radius: 5px;
    transition: width 0.1s linear;
}

.time-display-player {
    display: flex;
    justify-content: space-between;
    font-size: 0.8rem;
    color: #a0a0a0;
    margin-top: 0.5rem;
}

.main-controls-player {
    display: flex;
    justify-content: space-around;
    align-items: center;
    margin-bottom: 1rem;
}

.control-btn-player {
    background: none;
    border: none;
    color: #e0e0e0;
    font-size: 1.6rem;
    cursor: pointer;
    transition: color 0.2s ease, transform 0.1s ease;
    padding: 0.5rem;
}

.control-btn-player:hover {
    color: #380056;
    transform: scale(1.1);
}

.control-btn-player.play-pause-player {
    font-size: 2.2rem;
    color: #380056;
}

.control-btn-player.play-pause-player:hover {
    color: #380056;
}

.control-btn-player.active-feature {
    color: #380056 !important;
}

.secondary-controls-player {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 0.5rem;
    width: 100%;
    flex-wrap: wrap;
    gap: 1rem;
}

.control-btn-player.small-icon {
    font-size: 1.2rem;
}

.volume-control-player, .playback-speed-control {
    display: flex;
    align-items: center;
}

.volume-icon-player, .speed-icon {
    color: #380056;
    font-size: 0.9rem;
}

.volume-icon-player.ml-1 { margin-left: 0.25rem; }

.volume-slider-player, .speed-slider {
    width: 80px;
    height: 6px;
    -webkit-appearance: none;
    appearance: none;
    background: #404040;
    border-radius: 3px;
    outline: none;
    opacity: 0.8;
    transition: opacity .2s;
    margin: 0 0.5rem;
}

.volume-slider-player:hover, .speed-slider:hover {
    opacity: 1;
}

.volume-slider-player::-webkit-slider-thumb, .speed-slider::-webkit-slider-thumb {
    -webkit-appearance: none;
    appearance: none;
    width: 14px;
    height: 14px;
    background: #8b5cf6;
    border-radius: 50%;
    cursor: pointer;
}

.volume-slider-player::-moz-range-thumb, .speed-slider::-moz-range-thumb {
    width: 14px;
    height: 14px;
    background: #8b5cf6;
    border-radius: 50%;
    cursor: pointer;
    border: none;
}

#currentSpeedDisplay {
    font-size: 0.85rem;
    color: #380056;
    min-width: 35px;
    text-align: right;
}

.footer-credit {
    text-align: center;
    font-size: 0.75rem;
    color: #707070;
    margin-top: 1.5rem;
}

.song-detail-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    background: radial-gradient(circle at top left, #40205e, #2a103c02);
    border-radius: 1rem;
    box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    padding: 2rem;
    width: 100%;
    max-width: 400px;
    margin-top: 5rem;
}

.detail-album-art {
    width: 180px;
    height: 180px;
    border-radius: 0.75rem;
    margin-bottom: 1.5rem;
    object-fit: cover;
    box-shadow: 0 8px 20px rgba(0,0,0,0.4);
}

.song-detail-container h2 {
    font-size: 1.8rem;
    font-weight: 700;
    margin: 0 0 0.5rem 0;
    color: #ffffff;
}

.song-detail-container p {
    font-size: 1.1rem;
    color: #b3b3b3;
    margin: 0.2rem 0;
}

.play-from-detail-btn {
    background-color: #8b5cf6;
    color: #fff;
    border: none;
    padding: 0.8rem 2rem;
    border-radius: 0.75rem;
    font-size: 1.1rem;
    cursor: pointer;
    margin-top: 2rem;
    transition: background-color 0.3s ease, transform 0.2s ease;
    display: flex;
    align-items: center;
    justify-content: center;
}

.play-from-detail-btn:hover {
    background-color: #a78bfa;
    transform: translateY(-2px);
}

.play-from-detail-btn i {
    margin-right: 0.75rem;
    font-size: 1.3rem;
}

@media (max-width: 600px) {
    header h1 {
        font-size: 2rem;
    }
    .song-list li {
        padding: 0.8rem 1rem;
    }
    .song-list .song-info-list h3 {
        font-size: 1rem;
    }
    .music-player-box {
        max-width: 95%;
        padding: 1rem;
    }
    .player-header {
        flex-direction: column;
        align-items: center;
        text-align: center;
    }
    .album-art-player {
        width: 100px;
        height: 100px;
        margin-right: 0;
        margin-bottom: 1rem;
    }
    .track-info-player h2 {
        font-size: 1.2rem;
    }
    .lyrics-container {
        height: 150px;
        font-size: 0.9rem;
    }
    .control-btn-player { font-size: 1.4rem; }
    .control-btn-player.play-pause-player { font-size: 2rem; }
    
    .song-detail-container {
        padding: 1.5rem;
        max-width: 90%;
    }
    .detail-album-art {
        width: 150px;
        height: 150px;
    }
    .song-detail-container h2 {
        font-size: 1.5rem;
    }
    .song-detail-container p {
        font-size: 1rem;
    }
    .play-from-detail-btn {
        padding: 0.7rem 1.5rem;
        font-size: 1rem;
    }
    .secondary-controls-player {
        flex-direction: column;
        gap: 0.8rem;
    }
    .volume-control-player, .playback-speed-control {
        width: 100%;
        justify-content: center;
    }
}

.lyric-line {
    color: rgba(255, 255, 255, 0.4);
    transition: color 0.3s ease;
    display: block;
    margin-bottom: 0.2em;
}

.lyric-line.active {
    color: #ffffff;
    font-weight: bold;
}