import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { Link } from "react-router-dom";

import { getCookie } from "../../utils/cookie";
import AnswerList from "../Answer/AnswerList";
import AnswerGroupList from "../AnswerGroup/AnswerGroupList";
import NewGroup from "../AnswerGroup/NewGroup";

const FieldPage = () => {

    const { field_id } = useParams();

    const [ field, setField ] = useState(null);
    const [ answers, setAnswers ] = useState([]);
    const [ answerGroups, setAnswerGroups ] = useState([]);
    const [ selectedAnswers, setSelectedAnswers ] = useState([]);
    const [ hideGrouped, setHideGrouped ] = useState(true);

    const getAnswers = () => {
        fetch(`http://127.0.0.1:8000/api/fields/${field_id}/answers/`)
        .then(response => response.json())
        .then(data => setAnswers(data));
    }

    const getAnswerGroups = () => {
        fetch(`http://127.0.0.1:8000/api/fields/${field_id}/groups/`)
        .then(response => response.json())
        .then(data => setAnswerGroups(data));
    }

    const addSelectedAnswer = (id) => {
        const newSelectedAnswers = [...selectedAnswers, id];
        setSelectedAnswers(newSelectedAnswers);
    }
    
    const removeSelectedAnswer = (id) => {
        const newSelectedAnswers = selectedAnswers.filter(answerId => answerId !== id);
        setSelectedAnswers(newSelectedAnswers);
    }

    const addAnswersToGroup = (event) => {
        event.preventDefault();

        const group_id = event.target.group.value || null;

        const csrftoken = getCookie('csrftoken');

        fetch(`http://127.0.0.1:8000/api/update_group`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({
                group: group_id,
                answers: selectedAnswers
            })
        }).then(() => {
            getAnswers();
            getAnswerGroups();
        })
    }

    useEffect(() => {
        fetch(`http://127.0.0.1:8000/api/fields/${field_id}/`)
        .then(response => response.json())
        .then(data => {
            setField(data);
            getAnswers();
            getAnswerGroups();
        });
    }, [field_id]);

    return (field && (
        <div className="field-page">
            <div>
                <h2>
                    <Link to={`/assignment/${field.assignment}`}>{ field.assignment_title }</Link>
                </h2>
                <h2>{ field.label }</h2>

                { answerGroups && 
                <form onSubmit={addAnswersToGroup}>
                    <select name="group" id="group">
                        <option value={""}> --- </option>
                    { answerGroups.map(group => (
                        <option value={group.id} key={group.id}>
                            { group.name }
                        </option>
                    ))}
                    </select>

                    <input type="submit" value="Definir para grupo" />
                </form>
                }

                <label htmlFor="hide-grouped"> Esconder respostas agrupadas </label>
                <input checked={hideGrouped} onChange={() => setHideGrouped(!hideGrouped)} name="hide-grouped" id="hide-grouped" type="checkbox" />

                {answers && (
                <AnswerList 
                    allowSelection={true}
                    onAnswerSelected={(id) => addSelectedAnswer(id)}
                    onAnswerUnselected={(id) => removeSelectedAnswer(id)}
                    answers={(!hideGrouped && answers) || answers.filter(answer => answer.group === null)}
                    onAnswerModified={getAnswers} 
                />)}
            </div>
            <div>
                <h2> Grupos </h2>
                <NewGroup field={field} onNewGroupCreated={getAnswerGroups} />
                <AnswerGroupList groups={answerGroups} />
            </div>
        </div>
    ));
}

export default FieldPage;
