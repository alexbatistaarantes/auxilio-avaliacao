import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";

import { getCookie } from "../../utils/cookie";
import FieldList from "../Field/FieldList";
import NewField from "../Field/NewField";
import NewSubmission from "../Submission/NewSubmission";
import SubmissionList from "../Submission/SubmissionList";

const Assignment = () => {

    const { id } = useParams();
    const navigate = useNavigate();
    
    const [ assignment, setAssignment ] = useState(null);
    const [ fields, setFields ] = useState([]);
    const [ submissions, setSubmissions ] = useState([]);

    const getFields = () => {
        fetch(`http://127.0.0.1:8000/api/assignments/${id}/fields/`)
        .then(response => {
            return response.json()
        }).then(data => {
            setFields(data);
        });
    }

    const getSubmissions = () => {
        fetch(`http://127.0.0.1:8000/api/assignments/${id}/submissions/`)
        .then(response => {
            return response.json()
        }).then(data => {
            setSubmissions(data);
        });
    }

    useEffect(() => {
        const getAssignment = () => {
            fetch(`http://127.0.0.1:8000/api/assignments/${id}/`)
            .then((response) => {
                return response.json();
            }).then((data) => {
                setAssignment(data);
            });
        }

        getAssignment();
        getFields();
        getSubmissions();
    }, [id]);

    const deleteAssignment = () => {

        const csrftoken = getCookie('csrftoken');

        fetch(`http://127.0.0.1:8000/api/assignments/${id}/`, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': csrftoken
            }
        }).then(() => {
            navigate('/');
        });
    }

    return (assignment && (
        <div className="assignment">
            <h2>{ assignment.title }</h2>
            <button onClick={() => deleteAssignment()}> Excluir Atividde </button>
            <br />
            <img id="main-document" className="document-image" src={assignment.template_image} alt="Folha de respostas" />

            <div className="assignment-fields">
                <h3> Campos </h3>
                {submissions.length === 0 && (<NewField assignment={assignment} onNewFieldCreated={() => getFields()} />)}
                <FieldList fields={fields} />
            </div>

            <div className="assignment-submissions">
                <h3> Entregas </h3>
                <NewSubmission assignment={assignment} onNewSubmissionCreated={getSubmissions} />
                <SubmissionList submissions={submissions} />
            </div>
        </div>
    ));
}

export default Assignment;
