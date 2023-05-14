import { useEffect, useState } from "react";
import NavBar from "./NavBar";

export default function Spendings() {
  const [spendings, setSpendings] = useState([]);

  const fetchUserData = () => {
    fetch("http://localhost:8000/spendings/")
      .then((response) => {
        return response.json();
      })
      .then((data) => {
        setSpendings(data);
        console.log(data)
      });
  };

  useEffect(() => {
    fetchUserData();
  }, []);

  return (
    <div>
      
    <NavBar/>
       <header className="bg-dark text-white py-5">
        <div className="container">
          <h1>Witaj w FinanceTracker</h1>
          <p className="lead"></p>
        </div>
      </header>
      
      <main>
        <section id="wydatki" className="bg-light">
          <div className="container py-5 w-50">
            <h2 className="text-center mb-4">Wydatki</h2>
            <div className="row row-cols-1 row-cols-md-2 g-4">
              {
                spendings.data.map((spending, index) => (
                <div className="col" key={index}>
                  <div className="card h-100">
                    <div className="card-body">
                      <h5 className="card-title">{spending.attributes.goal_money}PLN</h5>
                      <p className="card-text">{spending.attributes.to_go_date}</p>
                      <button
                        type="button"
                        className="btn btn-primary"
                      >
                        Szczegóły
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>
      </main> 
    </div>
  );
}
