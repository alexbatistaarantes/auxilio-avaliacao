import { Link } from "react-router-dom";

const Field = ({ field }) => {

    return (
    <div className="field">
        <Link to={`/assignment/${field.assignment}/field/${field.id}`}>
            <h4>{ field.label }</h4>
        </Link>
        <p>{ field.points } points</p>
    </div>
    )
}

export default Field;
