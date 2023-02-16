import { useEffect, useState } from "react";

import { getCookie } from "../../utils/cookie";

const AnswerGroup = ({ answerGroup, onGroupModified }) => {

    const [points, setPoints] = useState(answerGroup.points);
    const [feedback, setFeedback] = useState(answerGroup.feedback);

    const handleSubmit = (event) => {
        event.preventDefault();

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
        <form onSubmit={(event) => handleSubmit(event)}>
            <input value={points} onChange={e => setPoints(e.target.value)} min={0} max={answerGroup.field_points} name="points" id="points" placeholder="Nota" type="number" /> / {answerGroup.field_points}
            <textarea defaultValue={feedback} onChange={e => setFeedback(e.target.value)} name="feedback" id="feedback" placeholder="Comentário" cols="30" rows="1"></textarea>
            <input type="submit" value="Salvar nota" />
        </form>
    </div>
    );
}

export default AnswerGroup;
