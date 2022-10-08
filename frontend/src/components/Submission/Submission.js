import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

import AnswerList from "../Answer/AnswerList";

const Submission = () => {

    const { submission_id } = useParams();
    
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

    return (submission && (
        <div className="submission">

            <a href="../"> Voltar para atividade </a>

            <h2>{ submission.studentId }</h2>
            <br />
            <img id="main-document" className="document-image" src={submission.image} alt="Folha de respostas" />

            <AnswerList answers={answers} onAnswerModified={() => getAnswers()}/>
        </div>
    ));
}

export default Submission;
