import { useState } from "react";
import { getCookie } from "../../utils/cookie";

const NewSubmissions = ({ assignment, onNewSubmissionCreated }) => {

    const [ imageFiles, setImageFiles ] = useState([]);

    const clearState = () => {
        setImageFiles([]);
    }

    const handleSubmit = (event) => {
        event.preventDefault();

        const formData = new FormData();
        formData.append('assignment', assignment.id);
        Array.from(imageFiles).forEach((imageFile) => {
            formData.append('images', imageFile);
        });
        
        const csrfToken = getCookie('csrfToken');

        fetch(`http://127.0.0.1:8000/api/submissions/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken
            },
            body: formData
        }).then(() => {
            clearState();
            event.target.reset();
            onNewSubmissionCreated();
        })
    }

    const onFileChange = (files) => {
        setImageFiles(files);
    }

    return (
        <div className="new-submission">
            <h4> Nova Entrega </h4>

            <form onSubmit={(event) => handleSubmit(event)} encType="multipart/form-data">

                <input name="submission" id="submission"
                    onChange={(event) => onFileChange(event.target.files)}
                    type="file"
                    multiple
                    required
                />

                <input value="Criar" type="submit" />
            </form>
        </div>
    );
}

export default NewSubmissions;
