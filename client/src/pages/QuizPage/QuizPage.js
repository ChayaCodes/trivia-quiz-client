import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom'; // ייבוא useParams מ-react-router-dom לקבלת פרמטרים מהכתובת
import QuizQuestion from '../../components/QuizQuestion/QuizQuestion';
import WinnersPage from '../../components/WinnersPage/WinnersPage';
import api from '../../api/axiosSetup'; 
import './QuizPage.css'; // אם יש סגנונות מותאמים אישית

const QuizPage = () => {
  const { quizId } = useParams(); // שליפת ה-ID של החידון מהכתובת
  const [currentQuestion, setCurrentQuestion] = useState(null);
  const [quizStatus, setQuizStatus] = useState('');
  const [loading, setLoading] = useState(true);
  const [next, setNext] = useState(false);

  useEffect(() => {
    fetchQuizData();
    }, [next]);

  const fetchQuizData = async () => {
    try {
      const [data, statusRes] = await Promise.all([
        api.get(`/admin/get_current_question/${quizId}`), // עדכון נתיב ה-API לכלול את quizId
      ]);
        setCurrentQuestion(data.data.current_question);
        console.log('Current question:', data.data.current_question);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching quiz data:', error);
      setLoading(false);
    }
  };
  

  const handleNextQuestion = async () => {
    try{
         const data = await api.post(`/admin/go_to_next_question/${quizId}`);
         setQuizStatus(data.data.status);
         setNext(!next);
         console.log('status:', quizStatus);
         
    }catch(error){
        console.error('Error fetching quiz data:', error);
    }
  };

  const handleShowStatistics = async () => {

  };


  const handleRestartQuiz = async () => {

  };



  if (loading) {
    return <div>Loading...</div>;
  }

  if (quizStatus === 'completed') {
    return (
      <WinnersPage winners={null} onRestart={handleRestartQuiz} />
    );
  }
  


  return (
    <div className="quiz-page">
      <div className="toolbar">
        <button onClick={handleNextQuestion} className="toolbar-button">
          שאלה הבאה
        </button>
        <button onClick={handleShowStatistics} className="toolbar-button">
          הצג סטטיסטיקות
        </button>
      </div>

       
      {currentQuestion && (
          <QuizQuestion 
            question={currentQuestion.question_text} 
            answers={currentQuestion.answers} 
          />
        )}
      
    </div>
  );
};

export default QuizPage;