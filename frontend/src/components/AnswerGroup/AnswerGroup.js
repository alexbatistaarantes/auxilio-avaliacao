import { useEffect } from "react";

import { getCookie } from "../../utils/cookie";

const AnswerGroup = ({ answerGroup, onGroupModified }) => {

    const handleSubmit = (event) => {
        event.preventDefault();

        const points = event.target.points.value;
        const feedback = event.target.feedback.value;

        const csrfToken = getCookie('csrfToken');

        fetch(`http://127.0.0.1:8000/api/groups/${answerGroup.id}/`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({
                points: points,
                feedback: feedback
            })
        }).then(() => {
            onGroupModified();
        })
    }

    return (
    <div className="answergroup">
        <h3>{ answerGroup.name }</h3>
        
        <div>
            { answerGroup.answers.length > 0
            ? <img className="region-image" src={ answerGroup.answers[0].image } alt="" />
            : <p> Grupo Vazio </p>
            }
        </div>
        
        <form onSubmit={(event) => handleSubmit(event)}>
            <input name="points" id="points" defaultValue={answerGroup.points} min={0} max={answerGroup.field_points} placeholder="Nota" type="number" /> / {answerGroup.field_points}
            <textarea name="feedback" id="feedback" defaultValue={answerGroup.feedback} placeholder="Comentário" cols="30" rows="1"></textarea>
            <input type="submit" value="Salvar nota" />
        </form>
    </div>
    );
}

export default AnswerGroup;
