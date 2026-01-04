// GrammarList.tsx
import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import './styles/Grammar.css';
import { fetchGrammarList } from "../services/service";
import Loading from "@/shared/components/layouts/Loading";


interface Grammar {
  id: number;
  pattern: string;
  meaning: string;
  level: string;
}

// interface Pagination {
//   pages: number;
//   current_page: number;
//   has_prev: boolean;
//   has_next: boolean;
//   prev_num?: number;
//   next_num?: number;
// }

const GrammarList = () => {
  const [grammarList, setGrammarList] = useState<Grammar[]>([]);
  // const [pagination, setPagination] = useState<Pagination | null>(null);


  const [loading, setLoading] = useState(false);

  const fetchGrammar = async (page = 1) => {
    setLoading(true);
    try {
      const response = await fetchGrammarList(page);
      setGrammarList(response.grammar_list);
      // setPagination(response.pagination);
      console.log(response);

    }
    catch (error) {
      console.error("Error fetching grammar list:", error);
    }
    finally {
      setLoading(false);
    }
  }

  // Fetch Grammar List
  useEffect(() => {
    fetchGrammar(1);
  }, []);



  // Handle page change
  // const handlePageChange = (pageNum: number) => {
  //   fetchGrammar(pageNum);
  // };

  if (loading) return <Loading isLoading={loading} />;

  return (
    <div className="container grammar-container">
      {grammarList.map((grammar) => (
        <Link to={`/grammar/${grammar.id}`} key={grammar.id} className="card grammar-card">
          <div className="grammar-pattern">{grammar.pattern}</div>
          <div className="grammar-meaning">{grammar.meaning}</div>
          <div className="grammar-level">{grammar.level}</div>
        </Link>
      ))}
      {/* Pagination controls would go here */}
    </div>
  );
};

export default GrammarList;
