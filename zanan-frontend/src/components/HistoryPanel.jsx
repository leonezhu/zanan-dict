import PropTypes from "prop-types";
import  { useState } from "react";

function HistoryPanel({
  isOpen,
  onClose,
  queryHistory,
  onRecordClick,
  onDelete,
}) {
  const [isDeleting, setIsDeleting] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  HistoryPanel.propTypes = {
    isOpen: PropTypes.bool.isRequired,
    onClose: PropTypes.func.isRequired,
    queryHistory: PropTypes.arrayOf(
      PropTypes.shape({
        word: PropTypes.string.isRequired,
        timestamp: PropTypes.number.isRequired,
      })
    ).isRequired,
    languages: PropTypes.array,
    onRecordClick: PropTypes.func.isRequired,
    onDelete: PropTypes.func.isRequired,
  };

  const formatTime = (timestamp) => {
    return new Date(timestamp).toLocaleString("zh-CN");
  };

  const handleDelete = async (record, e) => {
    e.stopPropagation();
    if (isDeleting) return;
    
    if (window.confirm(`确定要删除「${record.word}」的查询记录吗？`)) {
      setIsDeleting(true);
      try {
        const timestamp = new Date(record.timestamp).getTime() / 1000;
        await onDelete(timestamp);
      } finally {
        setIsDeleting(false);
      }
    }
  };

  const handleRecordClick = async (record) => {
    if (isLoading) return;
    setIsLoading(true);
    try {
      await onRecordClick(record);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className={`sidebar ${isOpen ? "open" : ""}`}>
      <button className="close-button" onClick={onClose}>
        &times;
      </button>
      <div className="history-section">
        <h2>查询历史</h2>
        <div className="history-list">
          {queryHistory.map((record, index) => (
            <div
              key={index}
              className={`history-card ${isLoading || isDeleting ? "disabled" : ""}`}
              onClick={() => handleRecordClick(record)}
              style={{ cursor: isLoading || isDeleting ? "not-allowed" : "pointer", position: "relative" }}
            >
              <button
                className="delete-button"
                onClick={(e) => handleDelete(record, e)}
                disabled={isDeleting || isLoading}
                style={{
                  position: "absolute",
                  top: "8px",
                  right: "8px",
                  background: "none",
                  border: "none",
                  cursor: isDeleting || isLoading ? "not-allowed" : "pointer",
                  fontSize: "16px",
                  color: isDeleting || isLoading ? "#999" : "#666",
                  padding: "4px 8px",
                  borderRadius: "4px",
                  transition: "background-color 0.2s, color 0.2s",
                }}
              >
                ×
              </button>
              <h3>{record.word}</h3>
              <p className="history-time">{formatTime(record.timestamp)}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default HistoryPanel;
