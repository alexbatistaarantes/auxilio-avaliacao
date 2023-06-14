import { useState } from "react";
import { useEffect } from "react";
import { Link, Outlet, useParams } from "react-router-dom";

const Layout = () => {

    const { assignment_id } = useParams();
    
    const [assignment, setAssignment] = useState(null);

    useEffect(() => {
        const getAssignment = () => {
            fetch(`http://127.0.0.1:8000/api/assignments/${assignment_id}/`)
            .then((response) => {
                return response.json();
            }).then((data) => {
                setAssignment(data);
            });
        }

        getAssignment();
    }, [assignment_id]);

    return (assignment &&
        <div>
            <h2>
                <Link to={`/assignment/${assignment_id}`}>{ assignment.title }</Link>
            </h2>

            <Outlet context={{assignment_id}} />
        </div>
    )
}

export default Layout;
