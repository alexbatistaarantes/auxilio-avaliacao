import { useState } from "react";

import { getCookie } from "../../utils/cookie";

const NewGroup = ({ field, onNewGroupCreated }) => {

    const [ name, setName ] = useState("");

    const handleSubmit = (event) => {
        event.preventDefault();
        
        const csrftoken = getCookie('csrftoken');

        //fetch(`http://127.0.0.1:8000/api/fields/${field.id}/groups/`, {
        fetch(`http://127.0.0.1:8000/api/groups/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({
                field: field.id,
                name: name
            })
        }).then(() => {
            event.target.reset();
            onNewGroupCreated();
        })
    }

    return (
    <div className="new-group">
        <form onSubmit={(event) => handleSubmit(event)}>
            <input name="name" onChange={(event) => setName(event.target.value)} type="text" />

            <input value="Criar" type="submit" />
        </form>
    </div>
    );
}

export default NewGroup;
