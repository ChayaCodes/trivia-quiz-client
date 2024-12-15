import React, { useState } from "react";
import useSound from "use-sound";
import correct from "../asset/sounds/Correct Answer Sound Effect.mp3";
import wrong from "../asset/sounds/Wrong Answer sound effect.mp3";


const Questionnaire = ({
    data: { question, correct_answer, answers },
    handleAnswer,


}) => {
    const [selectedAnswer, setSelectedAnswer] = useState(null);
    const [className, setClassName] = useState("answer");
    const [correctAnswer] = useSound(correct);
    const [wrongAnswer] = useSound(wrong);




    const delay = (duration, callback) => {
        setTimeout(() => {
            callback();
        }, duration);
    };

    const handleClick = (answer) => {
        setSelectedAnswer(answer);
        setClassName("answer active");
        delay(1000, () => {
            setClassName(answer === correct_answer ? "answer correct" : "answer wrong");
        });

        delay(2000, () => {
            if (answer === correct_answer) {
                correctAnswer();
                delay(2000, () => {
                    setSelectedAnswer(null);
                    handleAnswer(answer);
                });

            } else {
                wrongAnswer();
                delay(2000, () => {
                    setSelectedAnswer(null);
                    handleAnswer(answer);
                });


            }

        })
    };


    return (
        // Questionnaire main container
        <div className="questionnaire">

            {/* question container */}
            <div className="question row">

                <h2
                    dangerouslySetInnerHTML={{ __html: question }}
                />

            </div>

            {/* answers container */}
            <div className='answers row'>

                {answers.map((answer, idx) => {
                    return (
                        <button
                            key={idx}
                            dangerouslySetInnerHTML={{ __html: answer }}
                            className={selectedAnswer === answer ? className : "answer"}
                            onClick={() => !selectedAnswer && handleClick(answer)}
                        />
                    );
                })}

            </div>

        </div>
    );
};

export default Questionnaire;