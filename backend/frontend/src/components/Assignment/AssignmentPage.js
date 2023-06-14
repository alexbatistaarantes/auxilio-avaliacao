import { useEffect, useState } from "react";
import { useNavigate, useOutletContext } from "react-router-dom";

import { getCookie } from "../../utils/cookie";
import FieldList from "../Field/FieldList";
import NewField from "../Field/NewField";
import NewSubmissions from "../Submission/NewSubmissions";
import SubmissionList from "../Submission/SubmissionList";

const AssignmentPage = () => {

    //const { id } = useParams();
    const { assignment_id: id } = useOutletContext();
    const navigate = useNavigate();
    
    const [ assignment, setAssignment ] = useState(null);
    const [ fields, setFields ] = useState([]);
    const [ submissions, setSubmissions ] = useState([]);

    const getFields = () => {
        fetch(`/api/assignments/${id}/fields/`)
        .then(response => {
            return response.json()
        }).then(data => {
            setFields(data);
        });
    }

    const getSubmissions = () => {
        fetch(`/api/assignments/${id}/submissions/`)
        .then(response => {
            return response.json()
        }).then(data => {
            setSubmissions(data);
        });
    }

    const deleteAssignment = () => {

        if(window.confirm("Você tem certeza que deseja apagar a atividade?")){
            const csrftoken = getCookie('csrftoken');

            fetch(`/api/assignments/${id}/`, {
                method: 'DELETE',
                headers: {
                    'X-CSRFToken': csrftoken
                }
            }).then(() => {
                navigate('/');
            });
        }
    }

    const emailGrading = () => {
        if(window.confirm("Confirme que você deseja enviar a correção para os alunos")){
            fetch(`/api/email_grading/${assignment.id}`);
        }
    }

    const getSubmissionsFromEmail = () => {
        fetch(`/api/get_submissions_from_email/${assignment.id}`)
        .then(getSubmissions);
    }

    useEffect(() => {
        const getAssignment = () => {
            fetch(`/api/assignments/${id}/`)
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

    return (assignment && (
        <div className="assignment">
            <div className="assignment-infos">
                <p> Título: { assignment.title } </p>
                <p> Valor da atividade: { assignment.total_points} </p>
                <a href={`/api/get_assignment_grading_sheet/${assignment.id}`}> Baixar planilha de correção </a>
                <br />

                <button onClick={emailGrading}>Enviar correção por e-mail</button>
                <br />

                <button onClick={deleteAssignment}> Excluir Atividade </button>
                <br />

                <img id="main-document" className="document-image" src={assignment.template_image} alt="Folha de respostas" />
            </div>

            <div className="assignment-fields">
                <h3> Campos </h3>
                <NewField assignment={assignment} onNewFieldCreated={() => getFields()} />
                <FieldList fields={fields} />
            </div>

            <div className="assignment-submissions">
                <h3> Entregas </h3>

                <button onClick={getSubmissionsFromEmail}>Inserir entregas a partir do e-mail</button>

                <NewSubmissions assignment={assignment} onNewSubmissionCreated={getSubmissions} />
                <SubmissionList submissions={submissions} />
            </div>
        </div>
    ));
}

export default AssignmentPage;
