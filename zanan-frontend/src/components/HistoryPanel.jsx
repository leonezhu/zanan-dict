import React from 'react'

function HistoryPanel({ isOpen, onClose, queryHistory, languages, onRecordClick }) {
  const formatTime = (timestamp) => {
    return new Date(timestamp).toLocaleString('zh-CN')
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
              style={{ cursor: 'pointer' }}
            >
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