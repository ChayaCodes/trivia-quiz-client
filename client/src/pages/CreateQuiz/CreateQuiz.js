import React, { useState } from 'react';
import './CreateQuiz.css';
import api from "../../api/axiosSetup";

function CreateQuiz() {
    const [title, setTitle] = useState('');
    const [questions, setQuestions] = useState([
        { question: '', answers: ['', ''], correctAnswer: '' }
    ]);
    const [errorMessage, setErrorMessage] = useState('');

    const handleTitleChange = (e) => {
        setTitle(e.target.value);
    };

    const handleQuestionChange = (index, value) => {
        const newQuestions = [...questions];
        newQuestions[index].question = value;
        setQuestions(newQuestions);
    };

    const handleAnswerChange = (qIndex, aIndex, value) => {
        const newQuestions = [...questions];
        newQuestions[qIndex].answers[aIndex] = value;
        setQuestions(newQuestions);
    };

    const handleCorrectAnswerChange = (qIndex, aIndex) => {
        const newQuestions = [...questions];
        newQuestions[qIndex].correctAnswer = newQuestions[qIndex].answers[aIndex];
        setQuestions(newQuestions);
    };

    const addQuestion = () => {
        setQuestions([...questions, { question: '', answers: ['', ''], correctAnswer: '' }]);
    };

    const addAnswer = (qIndex) => {
        const newQuestions = [...questions];
        if (newQuestions[qIndex].answers.length < 4) {
            newQuestions[qIndex].answers.push('');
            setQuestions(newQuestions);
        }
    };

    const removeAnswer = (qIndex, aIndex) => {
        const newQuestions = [...questions];
        if (newQuestions[qIndex].answers.length > 2) {
            const removedAnswer = newQuestions[qIndex].answers.splice(aIndex, 1)[0];
            // אם התשובה המוסרת הייתה התשובה הנכונה, אפס את correctAnswer
            if (removedAnswer === newQuestions[qIndex].correctAnswer) {
                newQuestions[qIndex].correctAnswer = '';
            }
            setQuestions(newQuestions);
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        try {
            // אימות שכל שאלה מכילה בדיוק תשובה אחת נכונה
            for (let i = 0; i < questions.length; i++) {
                const q = questions[i];
                const correctCount = q.answers.filter(ans => ans === q.correctAnswer).length;
                if (correctCount !== 1) {
                    throw new Error(`שאלה ${i + 1} חייבת להכיל בדיוק תשובה אחת נכונה.`);
                }
            }

            // המרת הנתונים למבנה שהשרת מצפה לו
            const quizData = {
                title: title,
                questions: questions.map(q => ({
                    question: q.question,
                    answers: q.answers,
                    correctAnswer: q.correctAnswer
                })),
            };

            // שליחת הנתונים לשרת
            const response = await api.post('/admin/create_quiz', quizData);

            // טיפול בהצלחה
            console.log('חידון נוצר בהצלחה:', response.data);
            // איפוס הטופס
            setTitle('');
            setQuestions([
                { question: '', answers: ['', ''], correctAnswer: '' }
            ]);
            setErrorMessage('');
        } catch (error) {
            console.error('שגיאה ביצירת החידון:', error);
            if (error.response && error.response.data && error.response.data.error) {
                setErrorMessage(error.response.data.error);
            } else if (error.message) {
                setErrorMessage(error.message);
            } else {
                setErrorMessage('שגיאה לא צפויה ביצירת החידון.');
            }
        }
    };

    return (
        <div className="create-quiz-container">
            <h2>צור חידון חדש</h2>
            <form onSubmit={handleSubmit}>
                <div className="form-group">
                    <label>כותרת החידון:</label>
                    <input
                        type="text"
                        value={title}
                        onChange={handleTitleChange}
                        required
                        placeholder="הכנס כותרת"
                    />
                </div>
                {questions.map((question, qIndex) => (
                    <div className="question-group" key={qIndex}>
                        <div className="form-group">
                            <label>שאלה {qIndex + 1}:</label>
                            <input
                                type="text"
                                value={question.question}
                                onChange={(e) => handleQuestionChange(qIndex, e.target.value)}
                                required
                                placeholder="הכנס שאלה"
                            />
                        </div>
                        <div className="answers-group">
                            {question.answers.map((answer, aIndex) => (
                                <div className="answer-item" key={aIndex}>
                                    <input
                                        type="text"
                                        value={answer}
                                        onChange={(e) => handleAnswerChange(qIndex, aIndex, e.target.value)}
                                        required
                                        placeholder={`תשובה ${aIndex + 1}`}
                                    />
                                    <label>
                                        <input
                                            type="radio"
                                            name={`correctAnswer-${qIndex}`}
                                            checked={question.correctAnswer === answer}
                                            onChange={() => handleCorrectAnswerChange(qIndex, aIndex)}
                                            required
                                        />
                                        נכונה
                                    </label>
                                    {question.answers.length > 2 && (
                                        <button
                                            type="button"
                                            className="remove-answer-button"
                                            onClick={() => removeAnswer(qIndex, aIndex)}
                                        >
                                            הסר
                                        </button>
                                    )}
                                </div>
                            ))}
                            {question.answers.length < 4 && (
                                <button
                                    type="button"
                                    className="add-answer-button"
                                    onClick={() => addAnswer(qIndex)}
                                >
                                    הוסף תשובה
                                </button>
                            )}
                        </div>
                    </div>
                ))}
                <button type="button" className="add-question-button" onClick={addQuestion}>
                    הוסף שאלה
                </button>
                <button type="submit" className="submit-button">
                    צור חידון
                </button>
                {errorMessage && (
                    <p className="error-message" style={{ color: 'red' }}>
                        {errorMessage}
                    </p>
                )}
            </form>
        </div>
    );
}

export default CreateQuiz;