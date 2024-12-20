import React from 'react';
import PropTypes from 'prop-types';
import './QuizQuestion.css'; // אם יש סגנונות מותאמים אישית

const QuizQuestion = ({ question, answers }) => {
  console.log('question:', question);
  return (
    <div className="quiz-question">
      <h2 className="question-text">{question}</h2>
      <ul className="answers-list">
        {answers.map((answer, index) => (
          <li key={answer.id} className="answer-item">
            <span className="answer-number">{index + 1}.</span> {answer.option_text}
          </li>
        ))}
      </ul>
    </div>
  );
};

QuizQuestion.propTypes = {
  question: PropTypes.string.isRequired,
  answers: PropTypes.arrayOf(
    PropTypes.shape({
      id: PropTypes.number.isRequired,
      option_text: PropTypes.string.isRequired,
    })
  ).isRequired,
};

export default QuizQuestion;