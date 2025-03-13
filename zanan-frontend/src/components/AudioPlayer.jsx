import PropTypes from "prop-types";
import { useState, useRef, useEffect } from "react";

function AudioPlayer({ audioUrl, variant = "icon" }) {
  const [isPlaying, setIsPlaying] = useState(false);
  const audioRef = useRef(null);

  useEffect(() => {
    return () => {
      if (audioRef.current) {
        audioRef.current.pause();
        audioRef.current = null;
      }
    };
  }, []);

  useEffect(() => {
    if (audioRef.current) {
      audioRef.current.pause();
      audioRef.current = null;
      setIsPlaying(false);
    }
  }, [audioUrl]);

  if (variant === "text") {
    return (
      <audio
        controls
        src={`/api/audio/${audioUrl}?t=${Date.now()}`}
        className="audio-player"
      >
        您的浏览器不支持音频播放
      </audio>
    );
  }

  const handlePlayPause = () => {
    if (!audioRef.current) {
      audioRef.current = new Audio(`/api/audio/${audioUrl}?t=${Date.now()}`);
      audioRef.current.addEventListener('ended', () => {
        setIsPlaying(false);
      });
    }

    if (isPlaying) {
      audioRef.current.pause();
    } else {
      audioRef.current.play();
    }
    setIsPlaying(!isPlaying);
  };

  return (
    <button
      onClick={handlePlayPause}
      className="audio-button"
      title={isPlaying ? "暂停" : "播放发音"}
    >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        width="16"
        height="16"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
      >
        <path d="M11 5L6 9H2v6h4l5 4V5z" />
        <path d="M15.54 8.46a5 5 0 0 1 0 7.07" />
      </svg>
    </button>
  );
}

AudioPlayer.propTypes = {
  audioUrl: PropTypes.string.isRequired,
  variant: PropTypes.oneOf(["icon", "text"])
};

export default AudioPlayer;