import React from 'react';
import './HomePage.scss';  // ודא שייבאת את ה-SCSS
// import './HomePage.css'; // ייבוא CSS

import RainbowButton from '../../components/RainbowBox/RainbowButton';
import { useNavigate } from 'react-router-dom';

const HomePage = () => {
  const navigate = useNavigate();

  return (
    <div className="bodyIndex">
      <div className="regOrSign">
        <div id="reg">
          <div className="home">
            <h1>חנוכה קליק</h1>
            <h2>ברוכים הבאים לחנוכה קליק, החידון שיכניס אתכם חזק לאוירת חנוכה</h2>
            <h2>🎉 חנוכה הגיע, ואתם מוזמנים לאתגר את עצמכם בחידון חנוכה מיוחד! 🎉</h2>
            <p>
              <span>בין אם אתם מחפשים תוכנית לערב לביבות מהנה,</span><br/>
              <span>מסיבת חנוכה בכיתה, או כל הזדמנות אחרת.</span><br/>
              <span>החידון נוצר בדיוק בשבילכם, כל שעליכם לעשות הוא ללחוץ על התחברות <span className="link" onClick={() => navigate('/login')}>כאן</span></span><br/>
              <span>ומיד תוכלו לצפות בתוכן המקסים שלנו.</span><br/>
              <span>במאגר ישנם כמה שאלוני בסיס, במגוון רמות ובהתאמה לכל גיל,</span><br/>
              <span>ואתם יכולים להוסיף עליהם כיד הדמיון הטובה עליכם.</span><br/>
            </p>

            <div className="btns">
              <RainbowButton onClick={navigate('/signin')}>הרשם </RainbowButton>
              <RainbowButton onClick={() => navigate('/register')}>היכנס</RainbowButton>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HomePage;
