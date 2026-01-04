import React, { useState, useEffect } from "react";
import { useParams, useNavigate  } from "react-router-dom";
import { fetchKanjiDetail } from "../services/service";
import './styles/Kanji.css';


const KanjiDetail = () => {
  const { kanjiId } = useParams();
  const [kanji, setKanji] = useState(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate ();

  const getchKanjiDetail = async () => {
    setLoading(true);
    try {
      const response = await fetchKanjiDetail(kanjiId);
      setKanji(response);
    } catch (error) {
      console.error("Error fetching kanji detail:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    getchKanjiDetail();
  }, [kanjiId]);

  const handleBack = () => {
    navigate("/kanji");
  };

  const handleAddKanji = async () => {
    // Handle adding Kanji to user's list (Similar to "Add to List" button in your HTML)
  };

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <div className="kanji-detail">
      <div className="kanji-main">
        <h2>{kanji.character}</h2>
        <div className="kanji-meta">
          {kanji.onyomi && <span>Onyomi: {kanji.onyomi}</span>}
          {kanji.kunyomi && <span>Kunyomi: {kanji.kunyomi}</span>}
          {kanji.meaning_vi && <span>Meaning: {kanji.meaning_vi}</span>}
        </div>
      </div>

      <div className="kanji-examples">
        {kanji.examples && kanji.examples.length > 0 && (
          <ul>
            {kanji.examples.map((example, idx) => (
              <li key={idx}>{example}</li>
            ))}
          </ul>
        )}
      </div>

      <div className="kanji-actions">
        <button onClick={handleAddKanji} disabled={kanji.btn_data.disabled_flg}>
          {kanji.btn_data.display_text}
        </button>
        <button onClick={handleBack}>Back to List</button>
      </div>
    </div>
  );
};

export default KanjiDetail;
