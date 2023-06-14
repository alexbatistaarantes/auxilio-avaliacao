import { useEffect, useState } from "react";
import AssignmentList from "./Assignment/AssignmentList";
import NewAssignment from "./Assignment/NewAssignment";

const Home = () => {

    const [assignments, setAssignments] = useState([]);

    const getAssignments = () => {
        fetch("http://127.0.0.1:8000/api/assignments/")
        .then((response) => {
            return response.json();
        })
        .then((data) => {
            setAssignments(data);
        });
    }
    
    useEffect(() => {
        getAssignments();
    }, []);

    return (
        <div id="home">
            <hr />
            <NewAssignment onNewAssignmentCreated={() => getAssignments()} />
            <hr />
            <AssignmentList title="Todas as atividades" assignments={assignments} />
        </div>
    );
}

export default Home;
