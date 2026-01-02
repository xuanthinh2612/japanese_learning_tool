import React from "react";
import { Link } from "react-router-dom";

type Props = {
  onToggleSidebar: () => void;
};

const Header = ({ onToggleSidebar }: Props) => {

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
        <span className="username">👤&nbsp;&nbsp;Tên người dùng</span>
        <Link to="/login">🚪 Đăng Nhập</Link>
        <Link to="/logout">🚪 Đăng Xuất</Link>
      </div>
    </div>
  );
};

export default Header;
