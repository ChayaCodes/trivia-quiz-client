import React from 'react';
import './FormContainer.css';

const FormContainer = ({ children }) => {
  return (
    <form className="form-container">
      {children}
    </form>
  );
};

export default FormContainer;