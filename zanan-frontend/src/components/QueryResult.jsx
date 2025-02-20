import React from 'react'

function Body({ queryResult, languages }) {
  if (!queryResult || !queryResult.results) return null

  const { definitions, examples } = queryResult.results
  if (!definitions || !examples) return null

  return (
    <div className="results">
      <h2>查询结果：{queryResult.word}</h2>
      {Object.entries(definitions).map(([lang, result]) => (
        <div key={lang} className="result-card">
          <h3>{languages.find(l => l.code === lang)?.name}</h3>
          <p><strong>定义：</strong>{result.definition}</p>
          <p><strong>音标：</strong>{result.phonetic}</p>
          <div>
            <strong>示例：</strong>
            {examples[lang]?.map((example, index) => (
              <div key={index} className="example-item">
                <p>{example.text}</p>
                {example.audio_url && (
                  <audio controls>
                    <source src={example.audio_url} type="audio/mpeg" />
                  </audio>
                )}
              </div>
            ))} 
          </div>
        </div>
      ))}
    </div>
  )
}

export default Body