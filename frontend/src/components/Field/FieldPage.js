import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { Link } from "react-router-dom";

import AnswerList from "../Answer/AnswerList";

const FieldPage = () => {

    const { field_id } = useParams();

    const [ field, setField ] = useState(null);
    const [ answers, setAnswers ] = useState([]);

    const getAnswers = () => {
        fetch(`http://127.0.0.1:8000/api/fields/${field_id}/answers/`)
        .then(response => response.json())
        .then(data => setAnswers(data));
    }

    useEffect(() => {
        fetch(`http://127.0.0.1:8000/api/fields/${field_id}/`)
        .then(response => response.json())
        .then(data => {
            setField(data);
            getAnswers();
        });
    }, [field_id]);

    return (field && (
        <div className="field-page">
            <Link to={`/assignment/${field.assignment}`}> Voltar para atividade </Link>
            
            <h2>{ field.label }</h2>
            <img className="region-image" src={field.image} alt="Imagem do campo" />

            {answers && (<AnswerList answers={answers} groupedBy='student' onAnswerModified={() => getAnswers()} />)}
        </div>
    ));
}

export default FieldPage;
