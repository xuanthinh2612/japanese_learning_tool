import React from "react";
import { useState } from "react";
import Header from "./Header";
import Sidebar from "./Sidebar";
import Footer from "./Footer";
import './styles/MainLayout.css';  // Import CSS chung cho toàn bộ

const MainLayout: React.FC<{ children: React.ReactNode }> = ({ children }) => {

  const [isSidebarOpen, setIsSidebarOpen] = useState(true);
  
  const toggleSidebar = () => {
    setIsSidebarOpen((prev) => !prev);
  };

  return (
    <div className="layout">
      <Sidebar isOpen={isSidebarOpen}/>
      <div className="main-content">
        <Header onToggleSidebar={toggleSidebar} />
        <main>
          {children}
        </main>
        <Footer />
      </div>
    </div>
  );
};

export default MainLayout;
