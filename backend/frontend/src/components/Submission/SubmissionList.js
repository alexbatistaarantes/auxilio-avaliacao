import { Link } from "react-router-dom";

const SubmissionList = ({ submissions }) => {

    return (
        <div className="submission-list document-list">
            <ul>
            {submissions.map((submission) => (
                <li key={ submission.id } >
                    <Link to={`submission/${submission.id}`}>
                        <div className="document-preview submission-preview">
                            <h3>{ submission.studentId }</h3>
                            <img className="document-image" src={ submission.image } alt="Folha de resposta" />
                        </div>
                    </Link>
                    <a href={`/api/download_submission_grading/${submission.id}`} target='_blank'> Correção </a>
                </li>
            ))}
            </ul>
        </div>
    );
}

export default SubmissionList;
