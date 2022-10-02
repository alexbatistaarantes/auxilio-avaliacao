import { Link } from "react-router-dom";

const AssignmentList = ({ title, assignments }) => {
    
    return (
        <div className="assignment-list">
            <h2>{ title }</h2>

            <ul>
            {assignments.map((assignment) => (
                <li key={ assignment.id } >
                    <Link to={`assignment/${assignment.id}`}>
                        <div className="assignment-preview">
                            <h3>{ assignment.title }</h3>
                            <img src={ assignment.template_image } alt="" />
                        </div>
                    </Link>
                </li>
            ))}
            </ul>
        </div>
    );
}

export default AssignmentList;
