import { Link } from "react-router-dom";

const AssignmentList = ({ title, assignments }) => {

    return (
        <div className="assignment-list document-list">
            <h2>{ title }</h2>

            <ul>
            {assignments.map((assignment) => (
                <li key={ assignment.id } >
                    <Link to={`assignment/${assignment.id}`}>
                        <div className="assignment-preview document-preview">
                            <h3>{ assignment.title }</h3>
                            <img className="document-image" src={ assignment.template_image } alt="Folha de resposta" />
                        </div>
                    </Link>
                </li>
            ))}
            </ul>
        </div>
    );
}

export default AssignmentList;
