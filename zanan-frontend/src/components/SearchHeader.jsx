import { useState } from "react";

import PropTypes from "prop-types";

function Header({ onSearch, onRandomSearch, searchWord, setSearchWord }) {
  Header.propTypes = {
    onSearch: PropTypes.func.isRequired,
    onRandomSearch: PropTypes.func.isRequired,
    searchWord: PropTypes.string.isRequired,
    setSearchWord: PropTypes.func.isRequired,
  };
  const [selectedLanguages, setSelectedLanguages] = useState(["en", "zh-yue"]);
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
      await onSearch(searchWord, selectedLanguages);
    } finally {
      setIsLoading(false);
    }
  };

  const handleRandomClick = async () => {
    if (isLoading) return;
    setIsLoading(true);
    try {
      const randomWord = await onRandomSearch(selectedLanguages);
      if (randomWord) {
        setSearchWord(randomWord); // 更新搜索框内容为随机单词
      }
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
            value={searchWord}
            onChange={(e) => setSearchWord(e.target.value)}
            placeholder="请输入要查询的单词或短语"
            required
            disabled={isLoading}
          />
          <button type="submit" disabled={isLoading}>
            {isLoading ? "查询中..." : "查询"}
          </button>
          <button
            type="button"
            onClick={handleRandomClick}
            disabled={isLoading}
            className="random-button"
          >
            随一个
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
