import React from "react";

export default function Timesup({ userName, setTimeOut, handleNextQuestion, questionNumber, setGameOver }) {

    const handleClick = () => {
        setTimeOut(false);
        if (questionNumber === 10) {
            setGameOver(true);
        }
        handleNextQuestion(true);
    };

    return (
        <div className="timesup">
            <h1>Time's UP &#128336;! <span className="big"> {userName}</span> Try Faster!</h1><br/>
            <h1>click <span className="big">2 times</span> to continue</h1><br/>
            <p>*as a penalty you will lose 1 question 😈*</p>
            <button className="col-6 mt-6 btn btn-dark btn-lg" data-bs-toggle="button"
                onClick={handleClick}
            >Continue</button>
        </div>

    );
}