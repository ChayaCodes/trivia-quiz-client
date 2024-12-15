const Change = ({ changeUsed, setChangeUsed, handleNextQuestion }) => {

    const handelClick = () => {
        setChangeUsed(true);
        handleNextQuestion(false);
    };

    if(!changeUsed){
        return <button
        onClick={()=>handelClick()}>&#9851;</button>
    }

    return (<div className="used">&#9851;</div>);


}

export default Change;