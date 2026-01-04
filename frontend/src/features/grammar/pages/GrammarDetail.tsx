// GrammarDetail.tsx
import React, { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { fetchGrammarDetail } from "../services/service";
import './styles/Grammar.css';
import Loading from "@/shared/components/layouts/Loading";

interface Example {
  sentence: string;
  furigana: string;
  translation: string;
}

interface Usage {
  pattern: string;
  meaning: string;
  explanation: string;
  examples: Example[];
}

interface GrammarDetail {
  id: number;
  pattern: string;
  meaning: string;
  level: string;
  usages: Usage[];
}

interface BtnData {
  disabled_flg: boolean;
  display_text: string;
}

const GrammarDetail: React.FC = () => {
  const { grammarId } = useParams<{ grammarId: string }>();
  const [grammar, setGrammar] = useState<GrammarDetail | null>(null);
  const [btnData, setBtnData] = useState<BtnData | null>(null);
  const navigate = useNavigate();

  // Fetch grammar detail by ID
  const getGrammarDetail = async (id: string) => {
    const response = await fetchGrammarDetail(id);
    setGrammar(response.grammar);
    setBtnData(response.btn_data);
  }

  useEffect(() => {
    getGrammarDetail(grammarId!);
  }, [grammarId]);

  const handleAddGrammar = () => {
    fetch(`/api/add-grammar/${grammarId}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
    })
      .then((response) => response.json())
      .then((data) => {
        alert(data.message);
        if (data.success && btnData) {
          setBtnData({
            disabled_flg: true,
            display_text: "Đã thêm vào danh sách",
          });
        }
      });
  };

  const handleGoBack = () => {
    navigate(-1);
  };

  if (!grammar) return <Loading isLoading={true} />;

  return (
    <div className="grammar-detail-wrapper">
      <div className="grammar-header">
        <div className="grammar-pattern-large">{grammar.pattern}</div>
        <div className="grammar-level-badge">{grammar.level}</div>
      </div>

      <div className="grammar-section">
        <h3>📖 Meaning</h3>
        <p>{grammar.meaning}</p>
      </div>

      <div className="grammar-section">
        <h3>🧠 Explanation</h3>
        {grammar.usages.map((usage, index) => (
          <div key={index}>
            <p>{usage.pattern}</p>
            <p>{usage.meaning}</p>
            <p>{usage.explanation}</p>
            {/* <p>{{ usage.h_note }}</p>
              <p>{{ usage.note }}</p> */}
            <div className="grammar-section">
              <h3>✏ Examples {index + 1}</h3>
              <ul className="grammar-examples">
                {usage.examples.map((ex, idx) => (
                  <>
                    <li key={idx}>
                      <b>{ex.sentence}</b>
                    </li>
                    <p>{ex.furigana}</p>
                    <p>{ex.translation}</p>
                  </>)
                )}
              </ul>

            </div>
          </div>
        ))}
      </div>

      <div className="btn-actions">
        <button
          className="btn primary"
          onClick={handleAddGrammar}
          disabled={btnData?.disabled_flg}
        >
          {btnData?.display_text || "⭐ Thêm vào danh sách học"}
        </button>

        <button className="btn ghost" onClick={handleGoBack}>
          ← Quay lại danh sách
        </button>
      </div>
    </div>
  );
};

export default GrammarDetail;
