import React, { useState, useEffect, useCallback } from "react";
import "./styles/TopWords.css";
import { fetchVocabularyList, addWordToList } from "../services/service";
import { Link } from "react-router-dom";

interface Word {
  id: string;
  text: string;
  freq: number;
  status: "none" | "learning" | "reviewing" | "mastered" | "dropped" | null;
}

interface Pagination {
  total: number;
  pages: number;
  current_page: number;
}

const TopWords: React.FC = () => {
  const [words, setWords] = useState<Word[]>([]);
  const [pagination, setPagination] = useState<Pagination>({
    total: 0,
    pages: 0,
    current_page: 1,
  });
  const [loading, setLoading] = useState<boolean>(false);
  const [message, setMessage] = useState<string>("");

  // Fetch từ vựng từ API
  const fetchWords = useCallback(async (page: number) => {
    setLoading(true);
    try {
      const data = await fetchVocabularyList(page);  // Gọi từ service
      setWords(data.words);
      setPagination({
        total: data.total,
        pages: data.pages,
        current_page: data.current_page,
      });
      setLoading(false);
    } catch (error) {
      console.error("Error fetching words:", error);
      setMessage("Có lỗi xảy ra khi tải dữ liệu.");
      setLoading(false);
    }
  }, []);

  // Lần đầu tiên load trang 1
  useEffect(() => {
    fetchWords(1);
  }, [fetchWords]);

  // Xử lý thêm từ vào danh sách học
  const handleButtonClick = async (wordId: string, button: HTMLButtonElement) => {
    try {
      const result = await addWordToList(wordId); // Gọi từ service
      setMessage(result.message);
      if (result.success) {
        // Cập nhật giao diện
        button.setAttribute("disabled", "true");
        button.innerText = "Đã thêm";
        button.classList.remove("add-btn");

        const parentCard = button.closest(".topword-card")!;
        updateStatus(parentCard);
      }
    } catch (error) {
      console.error("Error adding word:", error);
    }
  };

  const updateStatus = (parentCard: HTMLElement) => {
    const leaningStatus = parentCard.querySelector(".status");
    if (leaningStatus) {
      leaningStatus.className = "status learning";
      leaningStatus.innerText = "📘 Đang học";
    }
  };

  if (loading) {
    return (
      <div className="loading-container">
        {/* SVG Spinner */}
        <svg
          width="50"
          height="50"
          viewBox="0 0 50 50"
          preserveAspectRatio="xMidYMid"
          className="spinner"
        >
          <circle
            cx="25"
            cy="25"
            r="20"
            stroke="#36d7b7"
            strokeWidth="4"
            fill="none"
            strokeLinecap="round"
          >
            <animate
              attributeName="stroke-dasharray"
              values="1,200;89,150;1,200"
              keyTimes="0;0.5;1"
              dur="1.5s"
              repeatCount="indefinite"
            />
          </circle>
        </svg>
        <div>Đang tải dữ liệu...</div>
      </div>
    );
  }

  return (
    <div>
      {message && <div className="toast">{message}</div>}
      <div className="topword-container">
        {words.map((word) => (
          <div key={word.id} className="card topword-card">
            <div className="topword-text">
              <Link className="topword-text" to={`/word-detail/${word.text}`}>
                {word.text}
              </Link>
            </div>
            <div className="topword-freq">{word.freq} lần</div>
            <div className="topword-status">
              {word.status === null && <span className="status none">Chưa học</span>}
              {word.status === "learning" && <span className="status learning">Đang học</span>}
              {word.status === "reviewing" && <span className="status reviewing">Đang ôn</span>}
              {word.status === "mastered" && <span className="status mastered">✔ Đã thuộc</span>}
              {word.status === "dropped" && <span className="status dropped">Đã bỏ</span>}
            </div>
            <div className="topword-actions">
              {word.status === null ? (
                <button
                  className="action-btn add-btn"
                  onClick={(e) => handleButtonClick(word.id, e.currentTarget)}
                >
                  + Thêm
                </button>
              ) : (
                <button className="action-btn" disabled>
                  Đã thêm
                </button>
              )}
            </div>
          </div>
        ))}
      </div>

      {/* Phân trang */}
      {pagination.pages > 1 && (
        <div className="pagination">
          {/* Prev Button */}
          {pagination.current_page > 1 && (
            <a href="#" onClick={() => fetchWords(pagination.current_page - 1)}>
              « Prev
            </a>
          )}

          {/* Các số trang */}
          {Array.from({ length: pagination.pages }, (_, index) => {
            const pageNum = index + 1;
            return (
              <React.Fragment key={pageNum}>
                {pageNum === pagination.current_page ? (
                  <span className="current">{pageNum}</span>
                ) : (
                  <a href="#" onClick={() => fetchWords(pageNum)}>
                    {pageNum}
                  </a>
                )}
              </React.Fragment>
            );
          })}

          {/* Next Button */}
          {pagination.current_page < pagination.pages && (
            <a href="#" onClick={() => fetchWords(pagination.current_page + 1)}>
              Next »
            </a>
          )}
        </div>
      )}
    </div>
  );
};

export default TopWords;
