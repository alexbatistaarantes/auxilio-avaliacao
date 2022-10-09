import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { Link, useNavigate } from "react-router-dom";

import { getCookie } from "../../utils/cookie";
import AnswerList from "../Answer/AnswerList";

const Submission = () => {

    const { submission_id } = useParams();
    const navigate = useNavigate();
    
    const [ submission, setSubmission ] = useState(null);
    const [ answers, setAnswers ] = useState([]);

    const getAnswers = () => {
        fetch(`http://127.0.0.1:8000/api/submissions/${submission_id}/answers/`)
        .then(response => {
            return response.json()
        }).then(data => {
            setAnswers(data);
        });
    }

    useEffect(() => {
        const getSubmission = () => {
            fetch(`http://127.0.0.1:8000/api/submissions/${submission_id}/`)
            .then((response) => {
                return response.json();
            }).then((data) => {
                setSubmission(data);
            });
        }

        getSubmission();
        getAnswers();
    }, [submission_id]);

    const deleteSubmission = () => {

        if(window.confirm("Você tem certeza que deseja apagar a entrega?")){
            const csrftoken = getCookie('csrftoken');

            fetch(`http://127.0.0.1:8000/api/submissions/${submission_id}/`, {
                method: 'DELETE',
                headers: {
                    'X-CSRFToken': csrftoken
                }
            }).then(() => {
                navigate(`/assignment/${submission.assignment}`);
            });
        }
    }

    return (submission && (
        <div className="submission">
            <Link to={`/assignment/${submission.assignment}`}> Voltar para atividade </Link>
            <br />

            <div className="submission-infos">
                <h2>{ submission.studentId }</h2>
                <button onClick={() => deleteSubmission()}> Excluir entrega </button>
                <br />
                <img id="main-document" className="document-image" src={submission.image} alt="Folha de respostas" />
            </div>

            <AnswerList answers={answers} onAnswerModified={() => getAnswers()}/>
        </div>
    ));
}

export default Submission;
