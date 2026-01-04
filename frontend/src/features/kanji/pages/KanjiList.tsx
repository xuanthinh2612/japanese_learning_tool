import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { fetchKanjiList } from "../services/service";
import './styles/Kanji.css';


const KanjiList = () => {
  const [kanjiList, setKanjiList] = useState([]);
  const [pagination, setPagination] = useState({
    total: 0,
    pages: 0,
    current_page: 1,
  });
  const [loading, setLoading] = useState(false);

  const fetchKanji = async (page = 1) => {
    setLoading(true);
    try {
      const response = await fetchKanjiList(page);
      setKanjiList(response.kanji_list);
      setPagination({
        total: response.total,
        pages: response.pages,
        current_page: response.current_page,
      });
    } catch (error) {
      console.error("Error fetching kanji:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchKanji(1);
  }, []);

  return (
    <div>
      {loading && <div>Loading...</div>}
      <div className="container kanji-container">
        {kanjiList.map((kanji) => (
          <Link to={`/kanji/${kanji.id}`} key={kanji.id} className="card kanji-card">
            <div className="card-tag-right-above">{kanji.level}</div>
            <div className="kanji-char">{kanji.character}</div>
            <div className="kanji-info">
              <div className="reading">{kanji.hanviet}</div>
              <div className="meaning">{kanji.meaning_vi}</div>
            </div>
          </Link>
        ))}
      </div>

      {/* Pagination */}
      <div className="pagination">
        {/* Prev Button */}
        {pagination.current_page > 1 && (
          <button onClick={() => fetchKanji(pagination.current_page - 1)}>« Prev</button>
        )}

        {/* Các số trang */}
        {[...Array(pagination.pages)].map((_, idx) => {
          const pageNum = idx + 1;

          // Xác định vị trí trang hiện tại và các trang hiển thị
          const isAdjacent =
            pageNum === pagination.current_page ||
            pageNum === pagination.current_page - 1 ||
            pageNum === pagination.current_page + 1;

          const isEdgePage =
            pageNum === 1 || pageNum === pagination.pages;

          // Kiểm tra xem dấu "..." có nên hiển thị không
          const showEllipsis =
            (pageNum === pagination.current_page - 2 && pagination.current_page > 3) ||
            (pageNum === pagination.current_page + 2 && pagination.current_page < pagination.pages - 2);

          return (
            <>
              {/* Hiển thị dấu ... */}
              {showEllipsis && <span key={`ellipsis-${pageNum}`} className="dots">...</span>}

              {/* Hiển thị các trang */}
              {(isAdjacent || isEdgePage) && (
                <button
                  key={pageNum}
                  onClick={() => fetchKanji(pageNum)}
                  className={pageNum === pagination.current_page ? "active" : ""}
                >
                  {pageNum}
                </button>
              )}
            </>
          );
        })}

        {/* Next Button */}
        {pagination.current_page < pagination.pages && (
          <button onClick={() => fetchKanji(pagination.current_page + 1)}>Next »</button>
        )}
      </div>
    </div>
  );
};

export default KanjiList;
