import { useEffect, useState } from "react";
import NavBar from "./components/NavBar";
import SpendingCard from "./components/SpendingCard";
import GoalCard from "./components/GoalCard";
import Header from "./components/Header";

export default function MainPage() {
  const [spendings, setSpendings] = useState([]);
  const [goals, setGoals] = useState([]);

  const fetchData = (url, callback) => {
    fetch(`http://localhost:8000/${url}/`)
      .then((response) => {
        response.ok ? console.log("success") : console.log("error");
        return response.json();
      })
      .then((data) => {
        callback(data.data);
        console.log(data.data);
      });
  };

  const fetchSpendings = () => {
    fetchData("spendings", setSpendings);
  };

  const fetchGoals = () => {
    fetchData("goals", setGoals);
  };

  useEffect(() => {
    fetchSpendings();
    fetchGoals();
  }, []);

  return (
    <div>
      <NavBar />
      <Header title="Strona główna"/>
      <main>
        <section id="wydatki" className="bg-light">
          <div className="container py-5 w-50">
            <h2 className="text-center mb-4">Wydatki</h2>
            <div className="row row-cols-1 row-cols-md-2 g-4">
              {spendings.map((spending, index) => (
                <SpendingCard key={index} spending={spending} />
              ))}
            </div>
          </div>
        </section>
        <section id="cele" className="bg-light">
          <div className="container py-5 w-50">
            <h2 className="text-center mb-4">Cele</h2>
            <div className="row row-cols-1 row-cols-md-2 g-4">
              {goals.map((goal, index) => (
                <GoalCard key={index} goal={goal} />
              ))}
            </div>
          </div>
        </section>
      </main>
    </div>
  );
}
