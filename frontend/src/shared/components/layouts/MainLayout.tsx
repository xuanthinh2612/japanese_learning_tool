import React from "react";
import Header from "./Header";
import Sidebar from "./Sidebar";
import Footer from "./Footer";
import './styles/MainLayout.css';  // Import CSS chung cho toàn bộ

const MainLayout: React.FC<{ children: React.ReactNode }> = ({ children }) => {

  return (
    <div className="layout">
      <Sidebar />
      <div className="main-content">
        <Header />
        <main>
          {children}
        </main>
        <Footer />
      </div>
    </div>
  );
};

export default MainLayout;
