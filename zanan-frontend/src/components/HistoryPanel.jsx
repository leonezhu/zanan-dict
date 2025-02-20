import React, { useState } from 'react'

import PropTypes from 'prop-types';

function HistoryPanel({ isOpen, onClose, queryHistory, languages, onRecordClick, onDelete }) {
  const [deletingRecord, setDeletingRecord] = useState(null);

  HistoryPanel.propTypes = {
    isOpen: PropTypes.bool.isRequired,
    onClose: PropTypes.func.isRequired,
    queryHistory: PropTypes.arrayOf(
      PropTypes.shape({
        word: PropTypes.string.isRequired,
        timestamp: PropTypes.number.isRequired
      })
    ).isRequired,
    languages: PropTypes.array,
    onRecordClick: PropTypes.func.isRequired,
    onDelete: PropTypes.func.isRequired
  };

  const formatTime = (timestamp) => {
    return new Date(timestamp).toLocaleString('zh-CN')
  }

  const handleDelete = async (record, e) => {
    e.stopPropagation();
    // if (window.confirm(`确定要删除「${record.word}」的查询记录吗？`)) {
      const timestamp = new Date(record.timestamp).getTime() / 1000; // 转换为秒级时间戳
      await onDelete(timestamp);
    // }
  }

  return (  
    <div className={`sidebar ${isOpen ? 'open' : ''}`}>
      <button className="close-button" onClick={onClose}>
        &times;
      </button>
      <div className="history-section">
        <h2>查询历史</h2>
        <div className="history-list">
          {queryHistory.map((record, index) => (
            <div 
              key={index} 
              className="history-card" 
              onClick={() => onRecordClick(record)}
              style={{ cursor: 'pointer', position: 'relative' }}
            >
              <button
                className="delete-button"
                onClick={(e) => handleDelete(record, e)}
                style={{
                  position: 'absolute',
                  top: '8px',
                  right: '8px',
                  background: 'none',
                  border: 'none',
                  cursor: 'pointer',
                  fontSize: '16px',
                  color: '#666',
                  padding: '4px 8px',
                  borderRadius: '4px',
                  transition: 'background-color 0.2s'
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
  )
}

export default HistoryPanel