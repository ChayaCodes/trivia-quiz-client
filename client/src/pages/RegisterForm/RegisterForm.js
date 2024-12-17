import React, { useState } from 'react';
import './RegisterForm.css';
import FormContainer from '../../components/FormContiner/FormContainer';
import GlowOnInput from '../../components/GlowOnInput/GlowOnInput';
import RainbowButton from '../../components/RainbowBox/RainbowButton';
import axios from 'axios';


const RegisterForm = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [email, setEmail] = useState('');
  const [errorMessage, setErrorMessage] = useState('');

  const handleRegister = async (e) => {
    e.preventDefault();

    console.log("Username:", username);
    console.log("Password:", password);
    console.log("Confirm Password:", confirmPassword);
    console.log("Email:", email);

    if (username.trim() === '' || password.trim() === '' || email.trim() === '') {
      setErrorMessage('כל השדות חייבים להיות מלאים');
      return;
    }

    if (password !== confirmPassword) {
      setErrorMessage('הסיסמאות אינן תואמות');
      return;
    }

    setErrorMessage('');
    const userData = {
      username,
      password,
      email
    };

    try {
      const response = await axios.post('http://localhost:5000/auth/register', userData, {
        withCredentials: true
      });
      console.log('Response:', response.data);
      setUsername('');
      setPassword('');
      setConfirmPassword('');
      setEmail('');
      console.log('נרשמת בהצלחה!', { username, password, email });
      alert('נרשמת בהצלחה!');
    } catch (error) {
      console.error('Error:', error.response ? error.response.data : error);
      alert('Error')
    }
  };

  return (
    <div className='register'>
      <FormContainer>
        <h1 className="had">משתמש חדש? נשמח להכיר אותך!</h1>

        <GlowOnInput
          type="text"
          placeholder=":שם משתמש"
          className="nameR"
          onChange={(e) => setUsername(e.target.value)}
        />
        <GlowOnInput
          type="password"
          placeholder=":סיסמה"
          className="psbord"
          onChange={(e) => setPassword(e.target.value)}
        />
        <GlowOnInput
          type="password"
          placeholder="אימות סיסמה"
          className="Apsbord"
          onChange={(e) => setConfirmPassword(e.target.value)}
        />
        <GlowOnInput
          type="email"
          placeholder=":מייל"
          className="email"
          onChange={(e) => setEmail(e.target.value)}
        />

        {errorMessage && <p className="error-message">{errorMessage}</p>}

        <RainbowButton onClick={handleRegister}>הרשם</RainbowButton>
        <p className='auth-p'>כבר יש לך חשבון?
          <a href="/login" className="auth-link">היכנס כאן</a>
        </p>
      </FormContainer>
    </div>
  );
};

export default RegisterForm;
