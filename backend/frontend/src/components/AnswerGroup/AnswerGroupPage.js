import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";

import AnswerList from "../Answer/AnswerList";

const AnswerGroupPage = () => {

    const { assignment_id, group_id } = useParams();

    const [ group, setGroup ] = useState(null);

    useEffect(() => {

        fetch(`http://127.0.0.1:8000/api/groups/${group_id}/`)
        .then(response => response.json())
        .then(data => {
            setGroup(data);
        });
    }, [group_id]);

    const handleSubmit = (event) => {
        event.preventDefault();
    }

    return (
    <div className="answergroup-page">

        <h2>
            <Link to={`/assignment/${assignment_id}`}>{ group.assignment_title }</Link>
        </h2>
        <h2>{ group.name } ({group.field_label})</h2>

        <form onSubmit={(event) => handleSubmit(event)}>
            <input name="points" id="points" defaultValue={group.points} min={0} max={group.field_points} placeholder="Nota" type="number" /> / {group.field_points}
            <textarea name="feedback" id="feedback" defaultValue={group.feedback} placeholder="Comentário" cols="30" rows="1"></textarea>
            <input type="submit" value="Salvar nota" />
        </form>

        <div>
            <AnswerList answers={group.answers} answerTitle='studentId' allowSelection={true} />
        </div>

    </div>
    )
}

export default AnswerGroupPage;