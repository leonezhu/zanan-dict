import PropTypes from "prop-types";
import AudioPlayer from "./AudioPlayer";
import "./AudioPlayer.css";

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
              {result.pronounce_word && (
                <p className="pronounce-item">
                  <strong>发音：</strong>
                  {result.pronounce_word}
                  {result.audio_url && (
                    <AudioPlayer audioUrl={result.audio_url} />
                  )}
                </p>
              )}
            </div>
            <div className="examples-section">
              {examples[lang]?.map((example, index) => (
                <div key={`${lang}-${index}-${queryResult.word}`} className="example-item">
                  <p>{example.text}</p>
                  {example.audio_url && (
                    <AudioPlayer audioUrl={example.audio_url} variant="text" />
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
