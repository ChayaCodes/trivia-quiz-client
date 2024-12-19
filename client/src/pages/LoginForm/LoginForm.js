import React, { useState } from 'react';
import FormContainer from '../../components/FormContiner/FormContainer';
import GlowOnInput from '../../components/GlowOnInput/GlowOnInput';
import RainbowButton from '../../components/RainbowBox/RainbowButton';
import api from '../../api/axiosSetup';

const LoginForm = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    
    const handleLogin = async (e) => {
        e.preventDefault();
        try {
            const response = await api.post('/auth/login', {
                email,
                password
            });
            console.log('התחברות הצליחה:', response);
            // המשך לאחר התחברות מוצלחת
        } catch (error) {
            console.error('שגיאה בהתחברות:', error);
        }
    };

    return (
        <div className='login'>
            <FormContainer>
                <h1 className="had">משתמש רשום? היכנס</h1>
                <GlowOnInput
                    type="email"
                    placeholder="אימייל"
                    className="email-input"
                    onChange={(e) => setEmail(e.target.value)}
                />
                <GlowOnInput
                    type="password"
                    placeholder="סיסמא"
                    className="password-input"
                    onChange={(e) => setPassword(e.target.value)}
                />
                <RainbowButton onClick={handleLogin}>
                    התחברות
                </RainbowButton>
            </FormContainer>
        </div>
    );
};

export default LoginForm;