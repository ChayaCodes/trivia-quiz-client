const DoubleTime = ({doubleTimeUsed, setDoubleTimeUsed, timer, setTimer }) => {

    const handelClick = () => {
        setTimer(timer+30);
        setDoubleTimeUsed(true);
    };

    if(!doubleTimeUsed){
        return <button
        onClick={()=>handelClick()}>&#128336;X 2</button>
    }
    return (<div className="used">&#128336;X 2</div>);

}

export default DoubleTime;