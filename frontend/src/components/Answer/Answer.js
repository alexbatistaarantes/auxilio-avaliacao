import { useState } from "react";

import { getCookie } from "../../utils/cookie";
import SelectionTool from "../SelectionTool";

const Answer = ({answer, allowModification=true, onAnswerModified}) => {

    const [ toggleModification, setToggleModification ] = useState(false);
    const [ cropRegion, setCropRegion ] = useState({
        unit: '%',
        x: (answer.x / answer.submission_width) * 100,
        y: (answer.y / answer.submission_height) * 100,
        width: (answer.width / answer.submission_width) * 100,
        height: (answer.height / answer.submission_height) * 100,
    });
    
    const saveModification = () => {

        const body = {
            id: answer.id,
            x: parseInt((cropRegion.x/100) * answer.submission_width),
            y: parseInt((cropRegion.y/100) * answer.submission_height),
            width: parseInt((cropRegion.width / 100) * answer.submission_width),
            height: parseInt((cropRegion.height / 100) * answer.submission_height),

            modified: true
        };

        const csrftoken = getCookie('csrfToken');

        fetch(`http://127.0.0.1:8000/api/answers/${answer.id}/`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify(body)
        }).then(() => {
            onAnswerModified();
            setToggleModification(false);
        });
    }

    return (
        <div className="answer">
            <h2> { answer.field_label } </h2>
            <img className="region-image" src={ answer.image } alt="" />
            
            {allowModification && (
            <button onClick={() => setToggleModification(!toggleModification)}>
                {!toggleModification && ("Editar")}
                {toggleModification && ("Cancelar edição")}
            </button>
            )}
            
            {allowModification && toggleModification && (
            <div>
                <button onClick={() => saveModification()}> Salvar edição </button>
                <SelectionTool
                    src={answer.submission_image}
                    crop={cropRegion}
                    onCropChange={(c) => setCropRegion(c)}
                />
            </div>
            )}
        </div>
    );
}

export default Answer;
