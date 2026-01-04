import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { fetchKanjiList } from "../services/service";
import './styles/Kanji.css';
import PagePagination from "@/shared/components/layouts/PagePagination";
import Loading from "@/shared/components/layouts/Loading";

type Kanji = {
  id: number;
  character: string;
  level: string;
  hanviet: string;
  meaning_vi: string;
};

const KanjiList = () => {
  const [kanjiList, setKanjiList] = useState<Kanji[]>([]);
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

  if (loading) return <Loading isLoading={loading} />;


  return (
    <div>
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
      <PagePagination pagination={pagination} nextPageFunc={fetchKanji} />
    </div>
  );
};

export default KanjiList;
