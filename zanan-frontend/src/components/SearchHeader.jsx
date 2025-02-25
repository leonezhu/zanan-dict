import { useState } from "react";

import PropTypes from "prop-types";

function Header({ onSearch }) {
  Header.propTypes = {
    onSearch: PropTypes.func.isRequired,
  };
  const [word, setWord] = useState("");
  const [selectedLanguages, setSelectedLanguages] = useState(["en", "zh-yue"]);
  const [exampleCount, setExampleCount] = useState(2);
  const [isLoading, setIsLoading] = useState(false);

  const languages = [
    { code: "en", name: "英语" },
    { code: "zh-yue", name: "粤语" },
    { code: "zh", name: "普通话" },
    { code: "zh-sc", name: "四川话" },
  ];

  const handleLanguageChange = (code) => {
    setSelectedLanguages((prev) =>
      prev.includes(code)
        ? prev.filter((lang) => lang !== code)
        : [...prev, code]
    );
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (isLoading) return;
    setIsLoading(true);
    try {
      await onSearch(word, selectedLanguages, exampleCount);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="header">
      <form onSubmit={handleSubmit} className="search-form">
        <div className="input-group">
          <input
            type="text"
            value={word}
            onChange={(e) => setWord(e.target.value)}
            placeholder="请输入要查询的单词或短语"
            required
            disabled={isLoading}
          />
          <select
            value={exampleCount}
            onChange={(e) => setExampleCount(Number(e.target.value))}
            className="example-count-select"
            disabled={isLoading}
          >
            {[1, 2, 3, 4, 5].map((count) => (
              <option key={count} value={count}>
                {count}个例句
              </option>
            ))}
          </select>
          <button type="submit" disabled={isLoading}>
            {isLoading ? "查询中..." : "查询"}
          </button>
        </div>

        <div className="language-selector">
          {languages.map((lang) => (
            <label key={lang.code} className="language-option">
              <input
                type="checkbox"
                checked={selectedLanguages.includes(lang.code)}
                onChange={() => handleLanguageChange(lang.code)}
              />
              {lang.name}
            </label>
          ))}
        </div>
      </form>
    </div>
  );
}

export default Header;
