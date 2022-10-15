import { useState } from "react";
import { Link } from "react-router-dom";

const FieldList = ({ fields }) => {
    
    const [ showSubmission, setShowSubmission ] = useState(false);

    return (
        <div className="field-list region-list">
            <button onClick={() => setShowSubmission(!showSubmission)}> Mostrar </button>
            <ul>
            {fields.map((field) => (
                <li key={ field.id } >
                    <Link to={`/assignment/${field.assignment}/field/${field.id}`}>
                        <div className="field-preview">
                            <h4>{ field.label }</h4>
                            { showSubmission && <img className="document-crop region-image" src={ field.assignment_image } alt="" />}
                        </div>
                    </Link>
                </li>
            ))}
            </ul>
        </div>
    );
}

export default FieldList;
