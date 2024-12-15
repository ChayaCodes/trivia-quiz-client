import React from 'react';
import './FlipBox.css';

const FlipBox = ({ front, back }) => {
  return (
    <div className="flip-box">
      <div className="flip-box-inner">
        <div className="flip-box-front">
          {front}
        </div>
        <div className="flip-box-back">
          {back}
        </div>
      </div>
    </div>
  );
};

export default FlipBox;