import { Link } from "react-router-dom";

const SubmissionList = ({ submissions }) => {

    return (
        <div className="submission-list">
            <ul>
            {submissions.map((submission) => (
                <li key={ submission.id } >
                    <div className="submission-preview">
                        <h3>{ submission.studentId }</h3>
                        <img className="document" src={ submission.image } alt="Folha de resposta" />
                    </div>
                </li>
            ))}
            </ul>
        </div>
    );
}

export default SubmissionList;
