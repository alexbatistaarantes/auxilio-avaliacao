import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";

import { getCookie } from "../utils/cookie";
import FieldList from "./FieldList";

const Assignment = () => {

    const { id } = useParams();
    const navigate = useNavigate();
    
    const [assignment, setAssignment] = useState(null);
    const [ fields, setFields ] = useState([]);


    useEffect(() => {
        const getAssignment = () => {
            fetch(`http://127.0.0.1:8000/api/assignments/${id}/`)
            .then((response) => {
                return response.json();
            }).then((data) => {
                setAssignment(data);
            });
        }

        const getFields = () => {
            fetch(`http://127.0.0.1:8000/api/assignments/${id}/fields/`)
            .then(response => {
                return response.json()
            }).then(data => {
                setFields(data);
            });
        }

        getAssignment();
        getFields();
    }, [id]);

    const deleteAssignment = () => {

        const csrftoken = getCookie('csrftoken');

        fetch(`http://127.0.0.1:8000/api/assignments/${id}/`, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': csrftoken
            }
        }).then(() => {
            navigate('/');
        });
    }

    return (assignment && (
        <div className="assignment">
            <h2>{ assignment.title }</h2>

            <button onClick={() => deleteAssignment()}> Excluir Atividde </button>
            <br />

            <img src={assignment.template_image} alt="" />

            <FieldList fields={fields} />
        </div>
    ));
}

export default Assignment;
