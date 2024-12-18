import React, { useState } from 'react';
import axios from 'axios';
import './LoginForm.css';
import FormContainer from '../../components/FormContiner/FormContainer';
import GlowOnInput from '../../components/GlowOnInput/GlowOnInput';
import RainbowButton from '../../components/RainbowBox/RainbowButton';

const LoginForm = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const handleLogin = async (e) => {
    e.preventDefault();
    const userData = {
      username,
      password,
    };

    try {
      const response = await axios.post('http://localhost:5000/auth/login', userData, {
        withCredentials: true
      });
      console.log('Response:', response.data);
      alert('Hello')
    } catch (error) {
      console.error('Error:', error.response ? error.response.data : error);
    }
  }

  return (
    <div className='login'>
      <FormContainer>
        <h1 className="had">משתמש רשום? היכנס</h1>
        <GlowOnInput type="text" placeholder=" שם משתמש / סיסמא" className="user-name" onChange={(e) => setUsername(e.target.value)}
        />
        <p className="namemes mes"></p>
        <GlowOnInput type="password" placeholder="סיסמה" className="psbord" onChange={(e) => setPassword(e.target.value)}
        />
        <p className="passmes mes"></p>
        <RainbowButton onClick={handleLogin}>לכניסה לחץ כאן</RainbowButton>
        <p className='auth-p' >עדיין לא נרשמת? <a href="/register" className="auth-link">הירשם כאן</a></p>
      </FormContainer>
    </div>
  );
};

export default LoginForm;