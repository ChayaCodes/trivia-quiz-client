import React from 'react';
import './GlowOnInput.css';

const GlowOnInput = ({ type, placeholder, className }) => {
  return (
    <input type={type} placeholder={placeholder} className={`illuminatedInput ${className}`} />
  );
};

export default GlowOnInput;