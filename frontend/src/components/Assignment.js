import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

const Assignment = () => {

    const { id } = useParams();
    const [assignment, setAssignment] = useState(null);

    useEffect(() => {
        const getAssignment = () => {
            fetch(`http://127.0.0.1:8000/api/assignments/${id}/`)
            .then((response) => {
                return response.json();
            }).then((data) => {
                setAssignment(data);
            });
        }

        getAssignment();
    }, [id]);

    return (assignment && (
        <div className="assignment">
            <h2>{ assignment.title }</h2>

            <img src={assignment.template_image} alt="" />
        </div>
    ));
}

export default Assignment;
