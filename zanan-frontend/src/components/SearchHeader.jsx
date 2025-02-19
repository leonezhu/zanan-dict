import { useState } from 'react'

function Header({ onSearch }) {
  const [word, setWord] = useState('')
  const [selectedLanguages, setSelectedLanguages] = useState(['en', 'zh-yue'])

  const languages = [
    { code: 'en', name: '英语' },
    { code: 'zh-yue', name: '粤语' },
    { code: 'zh', name: '普通话' },
    { code: 'zh-sc', name: '四川话' }
  ]

  const handleLanguageChange = (code) => {
    setSelectedLanguages(prev =>
      prev.includes(code)
        ? prev.filter(lang => lang !== code)
        : [...prev, code]
    )
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    onSearch(word, selectedLanguages)
  }

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
          />
          <button type="submit">查询</button>
        </div>

        <div className="language-selector">
          {languages.map(lang => (
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
  )
}

export default Header