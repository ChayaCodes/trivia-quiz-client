import { useEffect } from "react";




function Timer({ setTimeOut, questionNumber, timer, setTimer, changeUsed }) {

    useEffect(() => {
        if (timer === 0) return setTimeOut(true);
        const interval = setInterval(() => {
            setTimer((prev) => prev - 1);
        }, 1000);
        return () => clearInterval(interval);
    }, [timer, setTimeOut]);

    useEffect(() => {
        setTimer(30);
    }, [questionNumber, changeUsed]);
    return timer;
}

export default Timer;