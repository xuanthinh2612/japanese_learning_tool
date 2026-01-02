import React from "react";
import { Link, useLocation } from "react-router-dom";
import clsx from "clsx";


type Props = {
  isOpen: boolean;
};

const Sidebar = ({ isOpen }: Props) => {
  const location = useLocation();

  return (
    <aside className={clsx("sidebar", !isOpen && "collapsed")}>
      <h3>Menu</h3>
      <ul>
        <li>
          <Link className={location.pathname === '/' ? 'active' : ''} to="/">🏠 Trang chủ</Link>
        </li>
        <li>
          <Link className={location.pathname.startsWith('/top-words') ? 'active' : ''} to="/top-words">📚 Từ vựng thông dụng</Link>
        </li>
        <li>
          <Link className={location.pathname.startsWith('/kanji') ? 'active' : ''} to="/kanji">🈶 Kanji</Link>
        </li>
        <li>
          <Link className={location.pathname.startsWith('/grammar') ? 'active' : ''} to="/grammar">✍️ Ngữ pháp</Link>
        </li>
      </ul>
      <hr />
      <ul>
        <li>
          <Link className={location.pathname.startsWith('/my-words') ? 'active' : ''} to="/my-words">✍️ Từ vựng của tôi</Link>
        </li>
        <li>
          <Link className={location.pathname.startsWith('/my-grammars') ? 'active' : ''} to="/my-grammars">✍️ Ngữ pháp của tôi</Link>
        </li>
        <li>
          <Link className={location.pathname.startsWith('/my-kanji') ? 'active' : ''} to="/my-kanji">✍️ Kanji của tôi</Link>
        </li>
      </ul>
      <hr />
      <ul>
        <li><Link to="/top-words">📚 Bảng xếp hạng</Link></li>
        <li><Link to="/articles">🈶 Bài viết</Link></li>
        <li><Link to="/articles">🈶 Cộng đồng</Link></li>
        <li><Link to="/">📖 Game học từ</Link></li>
      </ul>
    </aside>
  );
};

export default Sidebar;
