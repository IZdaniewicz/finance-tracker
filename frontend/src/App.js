import MainPage from "./MainPage";
import TransactionPage from "./TransactionPage";
import LoginPage from "./LoginPage";
import RegisterPage from "./RegisterPage";
import {BrowserRouter as Router, Routes, Route, useNavigate} from "react-router-dom";
import {useEffect} from "react";

function Logout()
{
    const navigate = useNavigate()
    useEffect(() => {
        if(sessionStorage.getItem("token") !== null)
        {
            sessionStorage.removeItem("token")
        }
        navigate("/login")
    }, []);
    return (<div></div>)
}

function App() {
  return (
    <Router>
      <Routes>
        <Route exact path="/" element={<MainPage />} />
        <Route exact path="/transactions" element={<TransactionPage />} />
        <Route exact path="/login" element={<LoginPage />} />
        <Route exact path="/register" element={<RegisterPage />} />
          <Route exact path="/logout" element={<Logout />} />
      </Routes>
    </Router>
  );
}

export default App;
