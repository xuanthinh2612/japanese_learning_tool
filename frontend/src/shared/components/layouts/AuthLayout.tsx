import React from 'react';
import './styles/AuthLayout.css';  // Import file CSS chung cho toàn bộ

const AuthLayout: React.FC<{children: React.ReactNode}> = ({ children }) => {
    return (
        <>
            <div className="navbar">
                <a href="/" className="logo">WordApp</a>
            </div>

            <div className="auth-container">
                {children}
            </div>
        </>
    );
};

export default AuthLayout;
