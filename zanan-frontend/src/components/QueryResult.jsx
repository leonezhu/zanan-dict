import React from 'react'

function Body({ queryResult, languages }) {
  if (!queryResult) return null

  return (
    <div className="results">
      <h2>查询结果：{queryResult.word}</h2>
      {Object.entries(queryResult.results.definitions).map(([lang, result]) => (
        <div key={lang} className="result-card">
          <h3>{languages.find(l => l.code === lang)?.name}</h3>
          <p><strong>定义：</strong>{result.definition}</p>
          <p><strong>音标：</strong>{result.phonetic}</p>
          <p><strong>示例：</strong>{queryResult.results.examples[lang]}</p>
        </div>
      ))}
    </div>
  )
}

export default Body