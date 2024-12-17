import React from 'react';
import './GlowOnInput.css';

const GlowOnInput = ({ type, placeholder, className, onChange }) => {
  return (
    <input 
      type={type} 
      placeholder={placeholder} 
      className={`illuminatedInput ${className}`} 
      onChange={onChange} 
    />
  );
};

export default GlowOnInput;
