import { Link, BrowserRouter, Routes, Route } from "react-router-dom";

import './App.css';
import Assignment from "./components/Assignment/Assignment";

import Home from './components/Home';
import Submission from "./components/Submission/Submission";

function App() {
  return (
    <div id="app">
      <h1> Auxílio Avaliação </h1>

      <div id="content">
        <BrowserRouter>
          <nav>
            <Link to='/'> Home </Link>
          </nav>
          <Routes>
            <Route path='/' element={<Home />} />
            <Route path='assignment/:id' element={<Assignment />} />
            <Route path='assignment/:assignment_id/submission/:submission_id' element={<Submission />} />
          </Routes>
        </BrowserRouter>
      </div>
    </div>
  );
}

export default App;
