import React, { useState } from 'react';
import './CreateQuiz.css';

function CreateQuiz() {
    const [title, setTitle] = useState('');
    const [questions, setQuestions] = useState([
        { text: '', answers: [{ text: '', isCorrect: false }] }
    ]);

    const handleTitleChange = (e) => {
        setTitle(e.target.value);
    };

    const handleQuestionChange = (index, value) => {
        const newQuestions = [...questions];
        newQuestions[index].text = value;
        setQuestions(newQuestions);
    };

    const handleAnswerChange = (qIndex, aIndex, value) => {
        const newQuestions = [...questions];
        newQuestions[qIndex].answers[aIndex].text = value;
        setQuestions(newQuestions);
    };

    const handleIsCorrectChange = (qIndex, aIndex) => {
        const newQuestions = [...questions];
        newQuestions[qIndex].answers[aIndex].isCorrect = !newQuestions[qIndex].answers[aIndex].isCorrect;
        setQuestions(newQuestions);
    };

    const addQuestion = () => {
        setQuestions([...questions, { text: '', answers: [{ text: '', isCorrect: false }] }]);
    };

    const addAnswer = (qIndex) => {
        const newQuestions = [...questions];
        if (newQuestions[qIndex].answers.length < 4) {
            newQuestions[qIndex].answers.push({ text: '', isCorrect: false });
            setQuestions(newQuestions);
        }
    };

    const removeAnswer = (qIndex, aIndex) => {
        const newQuestions = [...questions];
        if (newQuestions[qIndex].answers.length > 1) {
            newQuestions[qIndex].answers.splice(aIndex, 1);
            setQuestions(newQuestions);
        }
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        // Validation: Ensure each question has at least one correct answer
        for (let q of questions) {
            if (!q.answers.some(a => a.isCorrect)) {
                alert('Each question must have at least one correct answer.');
                return;
            }
        }
        // Implement quiz creation logic here
        console.log({ title, questions });
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
                                value={question.text}
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
                                        value={answer.text}
                                        onChange={(e) => handleAnswerChange(qIndex, aIndex, e.target.value)}
                                        required
                                        placeholder={`תשובה ${aIndex + 1}`}
                                    />
                                    <label>
                                        <input
                                            type="checkbox"
                                            checked={answer.isCorrect}
                                            onChange={() => handleIsCorrectChange(qIndex, aIndex)}
                                        />
                                        נכונה
                                    </label>
                                    {question.answers.length > 1 && (
                                        <button type="button" className="remove-answer-button" onClick={() => removeAnswer(qIndex, aIndex)}>הסר</button>
                                    )}
                                </div>
                            ))}
                            {question.answers.length < 4 && (
                                <button type="button" className="add-answer-button" onClick={() => addAnswer(qIndex)}>הוסף תשובה</button>
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
            </form>
        </div>
    );
}

export default CreateQuiz;