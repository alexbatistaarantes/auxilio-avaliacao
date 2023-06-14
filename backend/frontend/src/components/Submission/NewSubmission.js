import { useEffect, useState } from "react";
import { getCookie } from "../../utils/cookie";

const NewSubmission = ({ assignment, onNewSubmissionCreated }) => {

    const [ documentImage, setDocumentImage ] = useState("");
    const [ studentId, setStudentId ] = useState("");

    const clearState = () => {
        setDocumentImage("");
        setStudentId("");
    }

    const handleSubmit = (event) => {
        event.preventDefault();

        const formData = new FormData();
        formData.append('assignment', assignment.id);
        formData.append('studentId', studentId);
        formData.append('image', documentImage);
        
        const csrfToken = getCookie('csrfToken');

        fetch(`/api/submissions/`, {
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
        setDocumentImage(files[0]);
        setStudentId(documentImage.name);
    }

    return (
        <div className="new-submission">
            <h4> Nova Entrega </h4>

            <form onSubmit={(event) => handleSubmit(event)} encType="multipart/form-data">

                <input name="studentId" id="studentId"
                    onChange={(event) => setStudentId(event.target.value)}
                    type="text"
                    required
                />

                <input name="submission" id="submission"
                    onChange={(event) => onFileChange(event.target.files)}
                    type="file"
                    accept="image/png, image/jpeg"
                    required
                />

                <input value="Criar" type="submit" />
            </form>
        </div>
    );
}

export default NewSubmission;
