import PropTypes from "prop-types";

Body.propTypes = {
  queryResult: PropTypes.shape({
    results: PropTypes.shape({
      definitions: PropTypes.object.isRequired,
      examples: PropTypes.object.isRequired,
    }).isRequired,
    word: PropTypes.string.isRequired,
    timestamp: PropTypes.string
  }).isRequired,
  languages: PropTypes.arrayOf(PropTypes.object).isRequired,
};

function Body({ queryResult, languages }) {
  if (!queryResult || !queryResult.results) return null;

  const { definitions, examples } = queryResult.results;
  if (!definitions || !examples) return null;

  return (
    <div className="results-container">
      <div className="results-grid">
        {Object.entries(definitions).map(([lang, result]) => (
          <div key={lang} className="result-card">
            <h3 className="language-title">{languages.find((l) => l.code === lang)?.name}</h3>
            <div className="definition-section">
              <p className="definition-item">
                <strong>定义：</strong>
                {result.definition}
              </p>
              <p className="phonetic-item">
                <strong>音标：</strong>
                {result.phonetic}
              </p>
            </div>
            <div className="examples-section">
              {/* <strong>示例：</strong> */}
              {examples[lang]?.map((example, index) => (
                <div key={`${lang}-${index}-${queryResult.word}`} className="example-item">
                  <p>{example.text}</p>
                  {example.audio_url && (
                    <audio
                      controls
                      key={`${lang}-${index}-${queryResult.word}-${queryResult.timestamp}-audio`}
                      className="audio-player"
                    >
                      <source src={`/api/audio/${example.audio_url}?t=${Date.now()}`} type="audio/mpeg" />
                    </audio>
                  )}
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Body;
