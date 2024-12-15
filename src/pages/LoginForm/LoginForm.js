import React from 'react';
import './LoginForm.css';
import FormContainer from '../../components/FormContiner/FormContainer';
import GlowOnInput from '../../components/GlowOnInput/GlowOnInput';
import RainbowButton from '../../components/RainbowBox/RainbowButton';

const LoginForm = () => {
  return (
  <div className='login'>
    <FormContainer>
      <h1 className="had">משתמש רשום? היכנס</h1>
      <GlowOnInput type="text" placeholder="שם משתמש" className="user-name" />
      <p className="namemes mes"></p>
      <GlowOnInput type="password" placeholder="סיסמה" className="psbord" />
      <p className="passmes mes"></p>
      
      <RainbowButton>לכניסה לחץ כאן</RainbowButton>
      <p className='auth-p' >עדיין לא נרשמת? <a href="/register" className="auth-link">הירשם כאן</a></p>
    </FormContainer>
  </div>
  );
};

export default LoginForm;