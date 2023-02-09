import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { Link } from "react-router-dom";

import { getCookie } from "../../utils/cookie";
import AnswerList from "../Answer/AnswerList";
import AnswerGroup from "../AnswerGroup/AnswerGroup";
import AnswerGroupList from "../AnswerGroup/AnswerGroupList";
import NewGroup from "../AnswerGroup/NewGroup";

const FieldPage = () => {

    const { field_id } = useParams();
    const navigate = useNavigate();

    const [ field, setField ] = useState(null);
    const [ answers, setAnswers ] = useState([]);
    const [ answerGroups, setAnswerGroups ] = useState([]);
    const [ selectedAnswers, setSelectedAnswers ] = useState([]);
    const [ selectedGroupId, setSelectedGroupId ] = useState(null);
    const [ hideGrouped, setHideGrouped ] = useState(true);

    const addSelectedAnswer = (id) => {
        const newSelectedAnswers = [...selectedAnswers, id];
        setSelectedAnswers(newSelectedAnswers);
    }
    const removeSelectedAnswer = (id) => {
        const newSelectedAnswers = selectedAnswers.filter(answerId => answerId !== id);
        setSelectedAnswers(newSelectedAnswers);
    }

    const addAnswersToGroup = () => {
        const groupId = selectedGroupId;
        setGroupToAnswers(groupId);
    }
    const removeAnswersFromGroup = () => {
        const groupId = null;
        setGroupToAnswers(groupId);
    }
    const setGroupToAnswers = (groupId) => {
        //const csrftoken = getCookie('csrftoken');

        fetch(`http://127.0.0.1:8000/api/update_answers_group`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
                //'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({
                group: groupId,
                answers: selectedAnswers
            })
        }).then(() => {
            getAnswers();
            getAnswerGroups();
            setSelectedAnswers([]);
        })
    }


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

    const deleteField = () => {

        if(window.confirm("Você tem certeza que deseja apagar o campo?")){
            const csrftoken = getCookie('csrftoken');

            fetch(`http://127.0.0.1:8000/api/fields/${field_id}/`, {
                method: 'DELETE',
                headers: {
                    'X-CSRFToken': csrftoken
                }
            }).then(() => {
                navigate(`/assignment/${field.assignment}`);
            });
        }
    }

    useEffect(() => {
        fetch(`http://127.0.0.1:8000/api/fields/${field_id}/`)
        .then(response => response.json())
        .then(data => {
            setField(data)
        }).then(() => {
            getAnswers();
            getAnswerGroups();
        }).then(() => {
            setSelectedGroupId(answerGroups[0].id || null)
        });
    }, [field_id]);

    return (field && (
        <div className="field-page">
            <div>
                <h3>{ field.label }</h3>

                <button onClick={deleteField}>Deletar campo</button>

                {answers && (
                <AnswerList 
                    allowSelection={true}
                    onAnswerSelected={(id) => addSelectedAnswer(id)}
                    onAnswerUnselected={(id) => removeSelectedAnswer(id)}
                    answers={answers.filter(answer => answer.group === null)}
                    onAnswerModified={getAnswers} 
                />)}
            </div>
            
            { answerGroups && (
                <span>
                    <button onClick={addAnswersToGroup}>{ ">" }</button>
                    <br />
                    <button onClick={removeAnswersFromGroup}>{ "<" }</button>
                    <br />
                    <button>Agrupar automaticamente</button>
                </span>
            )}

            <div>
                <h2> Grupos </h2>
                
                <h4> Novo Grupo </h4>
                <NewGroup field={field} onNewGroupCreated={getAnswerGroups} />
                
                {answerGroups.length > 0 && (
                <div>
                    <h4>Selecionar grupo</h4>
                    <select name="group" id="group" value={selectedGroupId} onChange={(e) => {setSelectedGroupId(Number(e.target.value) || null)}}>
                        { answerGroups.map(group => (
                            <option value={group.id} key={group.id}>
                                { group.name }
                            </option>
                        ))}
                    </select>
                </div>
                )}
                
                {selectedGroupId && 
                    <AnswerGroup 
                        answerGroup={answerGroups.filter(group => group.id === selectedGroupId)[0]} 
                        onGroupModified={getAnswers}
                    />
                }

                <AnswerList 
                    allowSelection={true}
                    onAnswerSelected={(id) => addSelectedAnswer(id)}
                    onAnswerUnselected={(id) => removeSelectedAnswer(id)}
                    answers={selectedGroupId != null && answers.filter(answer => answer.group === selectedGroupId) || []}
                    onAnswerModified={getAnswers}
                    key={answers}
                /> 
            </div>
        </div>
    ));
}

export default FieldPage;
