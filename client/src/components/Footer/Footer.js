import React from 'react';
import './Footer.css'; // וודא שהנתיב נכון

function Footer() {
  return (
    <footer className="footer">
      <div className="footer-content">
        <span className="footer-info">
          פותח באהבה ❤️ על ידי חיה קרמר | צור קשר: chaya41182@gmail.com | טלפון: 058-3241182
        </span>
        <div className="footer-links">
          <a
            href="https://github.com/ChayaCodes/trivia-quiz/graphs/contributors"
            target="_blank"
            rel="noopener noreferrer"
          >
            רשימת תורמים
          </a>
          |
          <a
            href="https://github.com/ChayaCodes/trivia-quiz"
            target="_blank"
            rel="noopener noreferrer"
          >
             קוד מקור ב - GitHub
          </a>
          |
          <a
            href="https://github.com/ChayaCodes/trivia-quiz/issues/new"
            target="_blank"
            rel="noopener noreferrer"
          >
            דיווח על תקלה
          </a>
        </div>
      </div>
    </footer>
  );
}

export default Footer;