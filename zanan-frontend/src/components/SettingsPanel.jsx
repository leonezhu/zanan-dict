import PropTypes from 'prop-types';
import './SettingsPanel.css';

function SettingsPanel({ exampleCount, onExampleCountChange, randomStyle, onRandomStyleChange }) {
  const styles = [
    { id: 'work', name: '职场' },
    { id: 'life', name: '生活' },
    { id: 'computer', name: '计算机' },
    { id: 'study', name: '学习' }
  ];

  return (
    <div className="settings-panel">
      <div className="settings-card">
        {/* <h3>查询设置</h3> */}
        <div className="settings-item example-count-wrapper">
          <label>例句数量：</label>
          <select
            value={exampleCount}
            onChange={(e) => onExampleCountChange(Number(e.target.value))}
            className="example-count-select"
          >
            {[1, 2, 3, 4, 5].map((count) => (
              <option key={count} value={count}>
                {count}个例句
              </option>
            ))}
          </select>
        </div>
        <div className="settings-item">
          <label>随机分类:</label>
          <div className="style-options">
            {styles.map((style) => (
              <label key={style.id} className="style-option">
                <input
                  type="radio"
                  name="randomStyle"
                  value={style.id}
                  checked={randomStyle === style.id}
                  onChange={(e) => onRandomStyleChange(e.target.value)}
                />
                {style.name}
              </label>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

SettingsPanel.propTypes = {
  exampleCount: PropTypes.number.isRequired,
  onExampleCountChange: PropTypes.func.isRequired,
  randomStyle: PropTypes.string.isRequired,
  onRandomStyleChange: PropTypes.func.isRequired
};

export default SettingsPanel;