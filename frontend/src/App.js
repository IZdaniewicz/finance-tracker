import Spendings from "./components/Spendings";
import NoHome from "./components/NoHome";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

function App() {
  return (
    <Router>
      <Routes>
        <Route exact path="/" element={<Spendings />} />
        <Route exact path="/nohome" element={<NoHome />} />
      </Routes>
    </Router>
  );
}

export default App;