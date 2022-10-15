import { Link, BrowserRouter, Routes, Route } from "react-router-dom";

import Assignment from "./components/Assignment/Assignment";
import FieldPage from "./components/Field/FieldPage";

import Home from './components/Home';
import Submission from "./components/Submission/Submission";

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
          </Routes>
        </BrowserRouter>
      </div>
    </div>
  );
}

export default App;
