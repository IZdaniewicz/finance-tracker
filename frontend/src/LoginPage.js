import {useEffect, useState} from "react";
import Header from "./components/Header";
import {useNavigate} from "react-router-dom";

export default function LoginPage() {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [formError,setFromError] = useState("");
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            let res = await fetch("http://localhost:8000/auth/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    username: username,
                    password: password,
                }),
            });
            let data = await res.json();
            console.log(data)
            setUsername("")
            setPassword("")
            if (res.status === 200) {
                sessionStorage.setItem("token",data.token)
                navigate("/");
            }
            if(res.status === 400)
            {
                setFromError(data.non_field_errors[0])
            }
        } catch (err) {
            console.log(err);
        }
    };

    useEffect(() => {
        if(sessionStorage.getItem("token") !== null)
        {
            navigate("/")
        }
        setFromError("")
    }, []);

  return (
    <div>
      {/* <NavBar /> */}
      <Header title="Logowanie"/>
      <main>
      <div class="container w-25">
        <form onSubmit={handleSubmit}>
          <div class="pt-5 pb-3">
            <label for="inputLogin" class="form-label">Login</label>
            <input
              type="text"
              class="form-control"
              id="inputLogin"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
          </div>
          <div class="mb-3">
            <label for="inputPassword" class="form-label">Hasło</label>
            <input
              type="password"
              class="form-control"
              id="inputPassword"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
            <p className="text-danger">{formError}</p>
          <div class="d-grid gap-2 mb-3">
              <button class="btn btn-primary" type="submit">
              <a className="nav-link" href="/">
                Zaloguj się
                </a>
              </button>
          </div>
        </form>
        <div class="text-center">
          <a href="/register">Nie masz konta? Zarejestruj się !</a>
        </div>
      </div>
      </main>
    </div>
  );
}
