import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom"; // Import useParams từ React Router
// import { WordDetailData } from "../types/wordTypes";
import { fetchWordDetail } from "../services/service";
import "./styles/WordDetail.css"
import Loading from "@/shared/components/layouts/Loading";


type WordDetailData = {
  word_id: string;
  forms: string[];
  level: string | null;
  readings: string[];
  senses: {
    examples?: {
      sentence: string;
      translation_vi?: string;
    }[];
    pos?: string;
    meanings: {
      vi: string[];
    };
  }[];
  articles: {
    title: string;
    source: string;
    count: number;
    content: string;
  }[];
  btn_data: {
    disabled_flg: boolean;
    display_text: string;
  };
};


const WordDetail = () => {
  const { wordText } = useParams(); // Lấy tham số word_text từ URL
  const [wordData, setWordData] = useState<WordDetailData | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchWord = async () => {
      try {
        if (!wordText) return;
        const response = await fetchWordDetail(wordText);
        const data = response;
        setWordData(data);
      } catch (err) {
        console.error(err);
      }
    };

    fetchWord();
  }, [wordText]);

  const goBack = () => {
    navigate(-1);
  };

  if (!wordData) return <Loading isLoading={true} />;

  return (
    <div className="grammar-detail-wrapper">
      {/* ===================== HEADER ===================== */}
      <div className="grammar-header">
        <div className="main-word">
          {wordData.forms.join("・")}
        </div>
        {wordData.level && (
          <div className="grammar-level-badge">{wordData.level}</div>
        )}
      </div>

      {/* ===================== READING ===================== */}
      {wordData.readings.length > 0 && (
        <div className="grammar-section">
          <h3>🔤 Cách đọc</h3>
          <p>{wordData.readings.join("・")}</p>
        </div>
      )}

      {/* ===================== MEANINGS ===================== */}
      {wordData.senses.map((sense, index) => (
        <div key={index} className="grammar-section">
          <h3>📖 Nghĩa {sense.pos && `(${sense.pos})`}</h3>
          {sense.meanings.vi && (
            <p>{sense.meanings.vi.join("; ")}</p>
          )}
          {sense.examples && sense.examples.length > 0 && (
            <div className="grammar-section">
              <h3>✏ Ví dụ</h3>
              <ul className="grammar-examples">
                {sense.examples.map((ex, idx) => (
                  <li key={idx}>
                    <b>{ex.sentence}</b>
                    {ex.translation_vi && <p>{ex.translation_vi}</p>}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      ))}

      {/* ===================== ARTICLE CONTEXT ===================== */}
      {wordData.articles.length > 0 && (
        <div className="grammar-section">
          <h3>📰 Sử dụng trong thực tế</h3>
          <ul className="grammar-examples">
            {wordData.articles.map((article, idx) => (
              <li key={idx}>
                <b>{article.title}</b>
                <p>{article.source} · {article.count} times</p>
                <div dangerouslySetInnerHTML={{ __html: article.content }} />

              </li>
            ))}
          </ul>
        </div>
      )}

      {/* ===================== ACTIONS ===================== */}
      <div className="btn-actions">
        <button
          className="btn primary add-word-btn"
          disabled={wordData.btn_data.disabled_flg}
          onClick={() => addWordToMyList(wordData.word_id)}
        >
          {wordData.btn_data.display_text}
        </button>
        <button className="btn ghost" onClick={() => goBack()}>← Quay lại danh sách</button>
      </div>
    </div>
  );
};

// Function to add word to learning list (stub for the button)
const addWordToMyList = async (wordId: string) => {
  try {
    const response = await fetch(`/add_to_learning/${wordId}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
    });
    const result = await response.json();
    if (result.success) {
      alert("Đã thêm vào danh sách học!");
    }
  } catch (err) {
    console.error(err);
  }
};

export default WordDetail;
