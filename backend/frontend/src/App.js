import { Link, BrowserRouter, Routes, Route } from "react-router-dom";

import Home from './components/Home';
import AssignmentPage from "./components/Assignment/AssignmentPage";
import SubmissionPage from "./components/Submission/SubmissionPage";
import FieldPage from "./components/Field/FieldPage";
import AnswerGroupPage from "./components/AnswerGroup/AnswerGroupPage";
import Layout from "./components/Layout";

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

            <Route path='assignment/:assignment_id' element={<Layout />}>
              <Route index path='' element={<AssignmentPage />} />
              <Route path='submission/:submission_id' element={<SubmissionPage />} />
              <Route path='field/:field_id' element={<FieldPage />} />
              <Route path='assignment/:assignment_id/group/:group_id' element={<AnswerGroupPage />} />
            </Route>
            
          </Routes>

        </BrowserRouter>

      </div>
    </div>
  );
}

export default App;
