import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

import { getCookie } from "../../utils/cookie";
import AnswerList from "../Answer/AnswerList";
import AnswerGroup from "../AnswerGroup/AnswerGroup";
import NewGroup from "../AnswerGroup/NewGroup";

const FieldPage = () => {

    const { field_id } = useParams();
    const navigate = useNavigate();

    const [ field, setField ] = useState(null);
    const [ answers, setAnswers ] = useState([]);
    const [ answerGroups, setAnswerGroups ] = useState([]);
    const [ sorters, setSorters ] = useState([]);

    const [ selectedAnswers, setSelectedAnswers ] = useState([]);
    const [ selectedGroupId, setSelectedGroupId ] = useState("");

    const addSelectedAnswer = (id) => {
        const newSelectedAnswers = [...selectedAnswers, id];
        setSelectedAnswers(newSelectedAnswers);
    }
    const removeSelectedAnswer = (id) => {
        const newSelectedAnswers = selectedAnswers.filter(answerId => answerId !== id);
        setSelectedAnswers(newSelectedAnswers);
    }

    const addAnswersToGroup = () => {
        setGroupToAnswers(selectedGroupId);
    }
    const removeAnswersFromGroup = () => {
        const groupId = null;
        setGroupToAnswers(groupId);
    }
    const setGroupToAnswers = (groupId) => {
        const csrftoken = getCookie('csrftoken');

        fetch(`/api/update_answers_group`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
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

    const groupAutomatically = () => {
        const csrftoken = getCookie('csrftoken');

        fetch(`/api/sort`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({
                field: field_id,
                sorter: document.querySelector("#sorter").value
            })
        }).then(() => {
            getAnswers();
            getAnswerGroups();
            setSelectedAnswers([]);
        })
    }

    const getField = () => {
        fetch(`/api/fields/${field_id}/`)
        .then(response => response.json())
        .then(data => setField(data));
    }

    const getAnswers = () => {
        fetch(`/api/fields/${field_id}/answers/`)
        .then(response => response.json())
        .then(data => setAnswers(data));
    }

    const getAnswerGroups = () => {
        fetch(`/api/fields/${field_id}/groups/`)
        .then(response => response.json())
        .then(data => setAnswerGroups(data));
    }

    const getSorters = () => {
        fetch(`/api/sorters`)
        .then(response => response.json())
        .then(data => setSorters(data));
    }

    const deleteField = () => {

        if(window.confirm("Você tem certeza que deseja apagar o campo?")){
            const csrftoken = getCookie('csrftoken');

            fetch(`/api/fields/${field_id}/`, {
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
        getField();
        getAnswers();
        getAnswerGroups();
        getSorters();
    }, [field_id]);

    // Para selecionar o grupo só depois de carregar os grupos
    useEffect(() => {
        if(answerGroups.length > 0){
            setSelectedGroupId(answerGroups[0].id);
        }
    }, [answerGroups]);

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
            
            <div className="group-controls">
                { answerGroups && (
                    <span>
                        <button onClick={addAnswersToGroup}>{ ">" }</button>
                        <br />
                        <button onClick={removeAnswersFromGroup}>{ "<" }</button>
                        <br />
                    </span>
                )}
                <br />
                { sorters.length > 0 && (
                    <span>
                        <select name="sorter" id="sorter">
                        {sorters.map(sorter => (
                            <option value={sorter} key={sorter}>{sorter}</option>
                        ))}
                        </select>
                        <br />
                        <button onClick={groupAutomatically}>Agrupar automaticamente</button>
                    </span>
                )}
            </div>

            <div>
                <h2> Grupos </h2>
                
                <h4> Novo Grupo </h4>
                <NewGroup field={field} onNewGroupCreated={getAnswerGroups} />
                
                {selectedGroupId && (
                <div>
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
                    
                    
                    <AnswerGroup
                        answerGroup={answerGroups.filter(group => group.id === selectedGroupId)[0]}
                        onGroupModified={getAnswers}
                        key={selectedGroupId}
                    />
                    
                    <AnswerList
                        allowSelection={true}
                        onAnswerSelected={(id) => addSelectedAnswer(id)}
                        onAnswerUnselected={(id) => removeSelectedAnswer(id)}
                        answers={answers.filter(answer => answer.group === selectedGroupId)}
                        onAnswerModified={getAnswers}
                        key={answers}
                    />
                </div>
                )}
            </div>
        </div>
    ));
}

export default FieldPage;
