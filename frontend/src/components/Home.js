import { useEffect, useState } from "react";
import AssignmentList from "./AssignmentList";
import NewAssignment from "./NewAssignment";

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
            <NewAssignment onNewAssignmentCreated={() => getAssignments()} />
            <AssignmentList title="Todas as atividades" assignments={assignments} />
        </div>
    );
}

export default Home;
