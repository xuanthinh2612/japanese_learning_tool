import { useState, useEffect } from "react";
import { useParams, useNavigate  } from "react-router-dom";
import { fetchKanjiDetail } from "../services/service";
import './styles/Kanji.css';
import Loading from "@/shared/components/layouts/Loading";

type Kanji = {
  id: number;
  character: string;
  level: string;
  hanviet: string;
  meaning_vi: string;
  onyomi: string;
  kunyomi: string;
  strokes: number;
  frequency: number;
  examples: string[];
  btn_data: {
    disabled_flg: boolean;
    display_text: string;
  };
};

const KanjiDetail = () => {
  const { kanjiId } = useParams();
  const [kanji, setKanji] = useState<Kanji | null>(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate ();

  const getchKanjiDetail = async () => {
    setLoading(true);
    try {
      
      if (!kanjiId) {
        navigate("/not-found");
        return;
      }
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

  if (loading) return <Loading isLoading={loading} />;
  if (!kanji) return <div>Kanji not found.</div>;

  return (
    <div className="kanji-detail-wrapper">
      <div className="kanji-main-card">
        <div className="kanji-big">{kanji.character}</div>
        <div className="kanji-meta">
          {kanji.level && <span className="badge">JLPT { kanji.level }</span>}
          {kanji.strokes && <span className="badge">{ kanji.strokes } Nét</span>}
          {kanji.frequency && <span className="badge">Xếp hạng thông dụng: { kanji.frequency }</span>}
          {kanji.hanviet && <span className="badge">Âm hán: { kanji.hanviet }</span>}
        </div>
      </div>

      {/* <!-- Thông tin đọc --> */}
      <div className="kanji-info-card">
          <div className="info-row">
              <span className="label">Âm on</span>
              <span className="value">{ kanji.onyomi ? kanji.onyomi : "—" }</span>
          </div>

          <div className="info-row">
              <span className="label">Âm kun</span>
              <span className="value">{ kanji.kunyomi ? kanji.kunyomi : "—" }</span>
          </div>

          <div className="info-row">
              <span className="label">Ý nghĩa</span>
              <span className="value meaning">{ kanji.meaning_vi ? kanji.meaning_vi : "—" }</span>
          </div>
      </div>

      {/* Ví dụ */}
      <div className="kanji-example-card">
        <h3>📖 Ví dụ</h3>
        {kanji.examples && kanji.examples.length > 0 && (
          <ul>
            {kanji.examples.map((example, idx) => (
              <li key={idx}>
              <span className="word important-word" data-word="{ example }">{ example }</span>
              </li>
            ))}
          </ul>
        )}
      </div>

      <div className="btn-actions">
        <button className="btn primary" onClick={handleAddKanji} disabled={kanji.btn_data.disabled_flg}>
          {kanji.btn_data.display_text}
        </button>
        <button className="btn ghost" onClick={handleBack}>← Quay lại danh sách</button>
      </div>
    </div>
  );
};

export default KanjiDetail;
