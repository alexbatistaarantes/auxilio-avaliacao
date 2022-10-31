import { useState } from "react";

import { getCookie } from "../../utils/cookie";

import SelectionTool from '../SelectionTool';

const NewField = ({ assignment, onNewFieldCreated }) => {

    const defaultCrop = {
        unit: '%',
        x: 30,
        y: 10,
        width: 40,
        height: 10
    };

    const [crop, setCrop] = useState(defaultCrop);

    const clearState = () => {
        setCrop(defaultCrop);
    }

    const handleSubmit = (event) => {
        event.preventDefault();

        const label = event.target.label.value;
        const points = event.target.points.value;
        const x = parseInt(assignment.width * (crop.x/100))
        const y = parseInt(assignment.height * (crop.y/100))
        const width = parseInt(assignment.width * (crop.width/100))
        const height = parseInt(assignment.height * (crop.height/100))

        const csrftoken = getCookie('csrftoken');

        fetch('http://127.0.0.1:8000/api/fields/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({
                'assignment': assignment.id,
                'label': label,
                'points': points,
                'x': x,
                'y': y,
                'width': width,
                'height': height
            })
        }).then(() => {
            clearState();
            event.target.reset();
            onNewFieldCreated();
        });
    }

    return (
        <div className="new-field">
            <h4> Novo campo </h4>

            <form onSubmit={(event) => handleSubmit(event)}>
                
                <div>
                    <input name="label" id="label" placeholder="Legenda"
                        type="text"
                        required
                    />

                    <input name="points" id="points" placeholder="Points" type="number" />
                </div>
                <input type="submit" value="Criar campo" />
                <br />

                <SelectionTool
                    crop={crop}
                    src={assignment.template_image}
                    onCropChange={(newCrop) => setCrop(newCrop)}
                />
            </form>
        </div>
    );
}

export default NewField;
