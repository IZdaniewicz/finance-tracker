import { useEffect, useState } from "react";
import NavBar from "./components/NavBar";
import Header from "./components/Header";
import TransactionsTable from "./components/TransactionsTable";

export default function TransactionsPage() {
  const [transactions, setTransactions] = useState([]);

  const fetchData = (url, callback) => {
    fetch(`http://localhost:8000/${url}`)
      .then((response) => {
        response.ok ? console.log("success") : console.log("error");
        return response.json();
      })
      .then((data) => {
        callback(data);
        console.log(data);
      });
  };

  const fetchTransactions = () => {
    fetchData("transaction", setTransactions);
  };

  useEffect(() => {
    fetchTransactions();
  }, []);

  return (
    <div>
      <NavBar />
      <Header title="Witaj w FinanceTracker"/>
      <main>
        <TransactionsTable transactions={transactions} />
      </main>
    </div>
  );
}
