import "./App.css";
// setting up REact router dom
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import StoryLoader from "./components/StoryLoader";

function App() {
  return (
    // settinng up router application
    <Router>
      <div className="app-container">
        <header>
          <h1>Interactive Story Weaver</h1>
        </header>

        <main>
          {/* using Routes for grouping all the seperate route  */}
          <Routes>
            {/* Seperate Route defined */}
            {/* :id -- dynamic value  */}
            <Route path={"/story/:id"} element={<StoryLoader />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
