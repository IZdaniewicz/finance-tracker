import { useEffect, useState } from "react";
import Header from "./components/Header";

export default function RegisterPage() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      let res = await fetch("http://localhost:8000/register/", {
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
      if (res.status === 200) {
        console.log("user created!");
      }
    } catch (err) {
      console.log(err);
    }
  };

  useEffect(() => {}, []);

  return (
    <div>
      <Header title="Rejestracja" />
      <main>
        <div className="container w-50">
        <form onSubmit={handleSubmit}>
            <div className="row mb-3 mt-5">
              <label htmlFor="inputLogin" className="col-sm-2 col-form-label">
                Login
              </label>
              <div className="col-sm-10">
                <input
                  type="login"
                  className="form-control"
                  id="username"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  required
                />
              </div>
            </div>
            <div className="row mb-3">
              <label htmlFor="inputPassword" className="col-sm-2 col-form-label">
                Hasło
              </label>
              <div className="col-sm-10">
                <input
                  type="password"
                  className="form-control"
                  id="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                />
              </div>
            </div>
            <div className="row mb-3">
            <div className="col-sm-10 offset-sm-2">
                <button type="submit" className="btn btn-primary">
                    Zarejestruj się
              </button>
            </div>
          </div>
          </form>
        </div>
      </main>
    </div>
  );
}
