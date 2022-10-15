import { useEffect } from "react";

const AnswerGroup = ({ answerGroup }) => {

    useEffect(() => {
        ;
    })

    return (
    <div className="answergroup">
        <h3>{ answerGroup.name }</h3>
        <div>
            { answerGroup.answers.length > 0
            ? <img className="region-image" src={ answerGroup.answers[0].image } alt="" />
            : <p> Grupo Vazio </p>
            }
        </div>
        
    </div>
    );
}

export default AnswerGroup;
