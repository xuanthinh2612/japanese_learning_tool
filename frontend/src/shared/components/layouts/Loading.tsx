// src/components/Loading.tsx

import React from 'react';
// import './Loading.css';  // (Thêm CSS cho loading spinner)

interface LoadingProps {
  isLoading: boolean;
}

const Loading: React.FC<LoadingProps> = ({ isLoading }) => {
  if (!isLoading) return null;

  return (
    <div className="loading-container">
      <svg
        width="50"
        height="50"
        viewBox="0 0 50 50"
        preserveAspectRatio="xMidYMid"
        className="spinner"
      >
        <circle
          cx="25"
          cy="25"
          r="20"
          stroke="#36d7b7"
          strokeWidth="4"
          fill="none"
          strokeLinecap="round"
        >
          <animate
            attributeName="stroke-dasharray"
            values="1,200;89,150;1,200"
            keyTimes="0;0.5;1"
            dur="1.5s"
            repeatCount="indefinite"
          />
        </circle>
      </svg>
      <div>Đang tải dữ liệu...</div>
    </div>
  );
};

export default Loading;
