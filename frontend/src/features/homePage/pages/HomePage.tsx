import { Link } from "react-router-dom";
import './styles/HomePage.css';  // Import file CSS chung cho toàn bộ

// Không dùng CSS Modules
const HomePage = () => {
    return (
        <>
            <div className="container-grid">
                <Link to="/top-words" className="card"><span className="icon">📚</span>Top từ thông dụng</Link>
                <Link to="/my-words" className="card"><span className="icon">📝</span>Từ của tôi</Link>
                <Link to="/kanji" className="card"><span className="icon">🎯</span>Hán tự</Link>
                <Link to="/grammar" className="card"><span className="icon">💡</span>Ngữ pháp</Link>
                <Link to="/articles" className="card"><span className="icon">📊</span>Luyện đọc blog/báo</Link>
                <Link to="/articles" className="card"><span className="icon">📊</span>Cộng đồng</Link>
                <Link to="/articles" className="card"><span className="icon">📊</span>Game học từ vựng</Link>
                <Link to="/articles" className="card"><span className="icon">📊</span>Bảng xếp hạng</Link>
                <Link to="/add-article" className="card"><span className="icon">➕</span>Add Article</Link>

            </div>
        </>
    );
};

export default HomePage;
