import { Link, BrowserRouter, Routes, Route } from "react-router-dom";

import Home from './components/Home';
import Assignment from "./components/Assignment/Assignment";
import Submission from "./components/Submission/Submission";
import FieldPage from "./components/Field/FieldPage";
import AnswerGroupPage from "./components/AnswerGroup/AnswerGroupPage";

function App() {
  return (
    <div id="app">
      <div id="content">
        <BrowserRouter>
          <nav>
            <Link to='/'> <h1> Auxílio Avaliação </h1> </Link>
          </nav>
          <Routes>
            <Route path='/' element={<Home />} />
            <Route path='assignment/:id' element={<Assignment />} />
            <Route path='assignment/:assignment_id/submission/:submission_id' element={<Submission />} />
            <Route path='assignment/:assignment_id/field/:field_id' element={<FieldPage />} />
            <Route path='assignment/:assignment_id/group/:group_id' element={<AnswerGroupPage />} />
          </Routes>
        </BrowserRouter>
      </div>
    </div>
  );
}

export default App;
