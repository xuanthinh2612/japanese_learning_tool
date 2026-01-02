import React from "react";
import { Link } from "react-router-dom";
import { useNavigate } from "react-router-dom";
import { useAuth } from "@/features/auth/context/AuthContext";


type Props = {
  onToggleSidebar: () => void;
};

const Header = ({ onToggleSidebar }: Props) => {
  const navigate = useNavigate();
  const { user, setUser} = useAuth();
  

  const handleLogout = () => {
    localStorage.removeItem("token");
    setUser(null);
    navigate("/login", { replace: true });
  };

  return (
    <div className="navbar">
      <div className="logo">
        <button className="menu-toggle" onClick={onToggleSidebar}>☰</button>
        <Link to="/">toihoctiengnhat.com</Link>
      </div>
      <div className="search-div">
        <div className="search-box">
          <input id="key_search" type="text" placeholder="🔍 Tìm từ, kanji, nghĩa..." />
          <button type="button" id="search-btn">Tìm Kiếm</button>
        </div>
        <div id="search-suggest" className="search-suggest hidden"></div>
      </div>

      <div className="user-actions">
        {/* Tình trạng người dùng: đã đăng nhập hay chưa */}
        { user ? (
          <>
            <span className="username">👤&nbsp;&nbsp;{`${user.username}`}</span>
            <a href="#" onClick={handleLogout} >🚪 Đăng Xuất</a>
          </>
        ) : (
          <>
            <Link to="/login">🚪 Đăng Nhập</Link>
          </>
        ) }
        
      </div>
    </div>
  );
};

export default Header;
