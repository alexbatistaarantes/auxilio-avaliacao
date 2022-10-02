import { useState } from "react";

const NewAssignment = ({ onNewAssignmentCreated }) => {

    const [title, setTitle] = useState("");
    const [templateImage, setTemplateImage] = useState("");

    const handleSubmit = (event) => {
        event.preventDefault();

        const assignment = {title, templateImage};
        
        fetch('http://127.0.0.1:8000/api/assignments/', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(assignment)
        }).then(() => {
            setTitle("");
            setTemplateImage("");
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
                        value={title}
                        onChange={(event) => setTitle(event.target.value)}
                        type="text"
                    />
                </div>
                <br />

                <div>
                    <label htmlFor="template-image"> Folha de resposta da Atividade </label>
                    <input name="template-image" id="template-image"
                        value={templateImage}
                        onChange={(event) => setTemplateImage(event.target.value)}
                        type="file"
                    />
                </div>
                <br />

                <input type="submit" value="Criar atividade" />
            </form>
        </div>
    );
}

export default NewAssignment;
