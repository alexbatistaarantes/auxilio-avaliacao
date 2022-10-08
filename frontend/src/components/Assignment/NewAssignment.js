import { useState } from "react";

import { getCookie } from "../../utils/cookie";

const NewAssignment = ({ onNewAssignmentCreated }) => {

    const [title, setTitle] = useState("");
    const [templateImage, setTemplateImage] = useState("");

    const clearState = () => {
        setTitle("");
        setTemplateImage("");
    }

    const handleSubmit = (event) => {
        event.preventDefault();

        const formData = new FormData();
        formData.append('title', title);
        formData.append('template_image', templateImage);

        const csrftoken = getCookie('csrftoken');

        fetch('http://127.0.0.1:8000/api/assignments/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken
            },
            body: formData
        }).then(() => {
            clearState();
            event.target.reset();
            onNewAssignmentCreated();
        });
    }

    return (
        <div className="new-assignment">
            <h2> Nova atividade </h2>

            <form onSubmit={(event) => handleSubmit(event)} encType="multipart/form-data">
                
                <div>
                    <label htmlFor="title"> Título </label>
                    <input name="title" id="title"
                        onChange={(event) => setTitle(event.target.value)}
                        type="text"
                        required
                    />
                </div>
                <br />

                <div>
                    <label htmlFor="template-image"> Folha de resposta da Atividade </label>
                    <input name="template-image" id="template-image"
                        onChange={(event) => setTemplateImage(event.target.files[0])}
                        type="file"
                        required
                    />
                </div>
                <br />

                <input type="submit" value="Criar atividade" />
            </form>
        </div>
    );
}

export default NewAssignment;
