import { useState, useEffect, useCallback } from "react";
import "./styles/TopWords.css";
import { fetchVocabularyList, addWordToList } from "../services/service";
import { Link } from "react-router-dom";
import PagePagination from "@/shared/components/layouts/PagePagination";
import { useAuth } from "@/features/auth/context/AuthContext";
import Loading from "@/shared/components/layouts/Loading";

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

const TopWords = () => {
  const [words, setWords] = useState<Word[]>([]);
  const [pagination, setPagination] = useState<Pagination>({
    total: 0,
    pages: 0,
    current_page: 1,
  });
  const [loading, setLoading] = useState<boolean>(false);
  const [message, setMessage] = useState<string>("");
  const { user } = useAuth(); // Giả sử bạn có context để lấy thông tin user


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

  const updateStatus = (parentCard: Element) => {
    const leaningStatus = parentCard.querySelector(".status");
    if (leaningStatus) {
      leaningStatus.className = "status learning";
      (leaningStatus as HTMLElement).innerText = "📘 Đang học";
    }
  };

  if (loading) return <Loading isLoading={loading} />;

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
            {user && (
              <>
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
              </>
            )}
          </div>
        ))}
      </div>

      {/* Phân trang */}
      <PagePagination pagination={pagination} nextPageFunc={fetchWords} />
    </div>
  );
};

export default TopWords;
