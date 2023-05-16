import { useEffect } from "react";
import Header from "./components/Header";

export default function LoginPage() {

  useEffect(() => {
  }, []);

  return (
    <div>
      {/* <NavBar /> */}
      <Header title="Logowanie"/>
      <main>
      <div class="container w-25">
        <form>
          <div class="pt-5 pb-3">
            <label for="inputLogin" class="form-label">Login</label>
            <input
              type="text"
              class="form-control"
              id="inputLogin"
              required
            />
          </div>
          <div class="mb-3">
            <label for="inputPassword" class="form-label">Hasło</label>
            <input
              type="password"
              class="form-control"
              id="inputPassword"
              required
            />
          </div>
          <div class="d-grid gap-2 mb-3">
              <button class="btn btn-primary" type="submit">
              <a className="nav-link" href="/">
                Zaloguj się
                </a>
              </button>
          </div>
        </form>
        <div class="text-center">
          <a href="/register">Nie pamiętasz hasła?</a>
        </div>
      </div>
      </main>
    </div>
  );
}
