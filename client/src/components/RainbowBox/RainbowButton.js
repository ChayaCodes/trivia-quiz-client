import React from 'react';
import './RainbowButton.css';

const RainbowButton = ({ children, onClick, width = '200px', height = '50px', href}) => {
  return (
    <button
      className="glow-on-hover button"
      onClick={onClick}
      style={{ width, height }}
      href={href}
    >
      {children}
    </button>
  );
};

export default RainbowButton;