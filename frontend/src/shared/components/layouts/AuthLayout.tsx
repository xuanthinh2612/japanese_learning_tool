import React from 'react';
import './styles/AuthLayout.css';  // Import file CSS chung cho toàn bộ
import { Link } from 'react-router-dom';
// import styles from './styles/AuthLayout.module.css';

const AuthLayout: React.FC<{children: React.ReactNode}> = ({ children }) => {
    return (
        <>
            <div className="navbar">
                <Link to="/" className="logo">toihoctiengnhat.com</Link>
            </div>
            <div className="auth-container">
                <div className="main-card">
                    {children}
                </div>
            </div>
        </>
    );
};

export default AuthLayout;
