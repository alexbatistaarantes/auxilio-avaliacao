import { useState } from "react";

import Field from "./Field";

const FieldList = ({ fields }) => {
    
    const [ showSubmission, setShowSubmission ] = useState(false);

    return (
        <div className="field-list region-list">
            <button onClick={() => setShowSubmission(!showSubmission)}> Mostrar </button>
            <ul>
            {fields.map((field) => (
            <li key={ field.id } >
                <Field field={field} />
            </li>
            ))}
            </ul>
        </div>
    );
}

export default FieldList;
