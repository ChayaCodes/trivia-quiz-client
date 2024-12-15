import React from 'react';
import './HomePage.css';
import RainbowButton from '../../components/RainbowBox/RainbowButton';
import { useNavigate } from 'react-router-dom';

const HomePage = () => {
  const navigate = useNavigate();





  return (
    <div className="bodyIndex">
      <div className="regOrSign">
        <div id="reg">
          <h1 className="had">היכנס או הירשם</h1>
          <div className='btns'>
          <RainbowButton onClick={navigate('/signin')}>הרשם </RainbowButton>
          <RainbowButton onClick={() => navigate('/register')}>היכנס</RainbowButton>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HomePage;