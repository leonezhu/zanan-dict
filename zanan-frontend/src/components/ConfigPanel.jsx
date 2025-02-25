import { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import './ConfigPanel.css';

function ConfigPanel({ isOpen, onClose }) {
  const [backendUrl, setBackendUrl] = useState('');

  useEffect(() => {
    // 从 localStorage 加载已保存的后端地址
    const savedUrl = localStorage.getItem('backendUrl');
    if (savedUrl) {
      setBackendUrl(savedUrl);
    }
  }, []);

  const handleSave = () => {
    // 验证输入的 URL 格式
    try {
      new URL(backendUrl);
      localStorage.setItem('backendUrl', backendUrl);
      onClose();
    } catch (error) {
      console.log(error)
      alert('请输入有效的 URL 地址');
    }
  };

  if (!isOpen) return null;

  return (
    <div className="config-overlay">
      <div className="config-panel">
        <h2>后端服务配置</h2>
        <div className="config-content">
          <label>
            后端服务地址：
            <input
              type="text"
              value={backendUrl}
              onChange={(e) => setBackendUrl(e.target.value)}
              placeholder="例如：http://localhost:8000"
            />
          </label>
        </div>
        <div className="config-actions">
          <button onClick={onClose}>取消</button>
          <button onClick={handleSave}>保存</button>
        </div>
      </div>
    </div>
  );
}

ConfigPanel.propTypes = {
  isOpen: PropTypes.bool.isRequired,
  onClose: PropTypes.func.isRequired,
};

export default ConfigPanel;