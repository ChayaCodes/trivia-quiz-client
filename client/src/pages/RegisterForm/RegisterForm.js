import React from 'react';
import './RegisterForm.css';
import FormContainer from '../../components/FormContiner/FormContainer';
import GlowOnInput from '../../components/GlowOnInput/GlowOnInput';
import RainbowButton from '../../components/RainbowBox/RainbowButton';

const RegisterForm = () => {
  return (
  <div className='register'>
    <FormContainer>
      <h1 className="had">משתמש חדש? נשמח להכיר אותך!</h1>
      <GlowOnInput type="text" placeholder=":שם משתמש" className="nameR" />
      <p className="namemes mes"></p>
      <GlowOnInput type="password" placeholder=":סיסמה" className="psbord" />
      <p className="passmes mes"></p>
      <GlowOnInput type="password" placeholder="אימות סיסמה " className="Apsbord" />
      <p className="Apassmes mes"></p>
      <GlowOnInput type="email" placeholder=":מייל" className="email" />
      <p className="emailmes mes"></p>
      <RainbowButton type="submit">הרשם</RainbowButton>
      <p className='auth-p' >כבר יש לך חשבון? <a href="/login" className="auth-link">היכנס כאן</a></p>
    </FormContainer>
    </div>
  );
};

export default RegisterForm;