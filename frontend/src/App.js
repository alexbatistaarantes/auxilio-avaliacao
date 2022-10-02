import { Link, BrowserRouter, Routes, Route } from "react-router-dom";

import './App.css';
import Assignment from "./components/Assignment";

import Home from './components/Home';

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
          </Routes>
        </BrowserRouter>
      </div>
    </div>
  );
}

export default App;
