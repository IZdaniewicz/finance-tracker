import React from 'react';

function TransactionsTable({ transactions }) {
  return (
    <div class="container mt-5">
      <h2>Wydatki:</h2>
      <table class="table">
        <thead>
          <tr>
            <th scope="col">Amount</th>
            <th scope="col">Description</th>
            <th scope="col">Label</th>
            <th scope="col">Date</th>
            <th scope="col"></th>
            <th scope="col"></th>
          </tr>
        </thead>
        <tbody>
          {transactions.map((transaction, index) => (
            <tr key={index}>
              <td>{transaction.amount}</td>
              <td>{transaction.description}</td>
              <td>{transaction.label}</td>
              <td>{transaction.data}</td>
              <td>
                <button
                  type="button"
                  className="btn btn-danger"
                >
                  Usuń
                </button>
              </td>
              <td>
                <button type="button" className="btn btn-primary">
                  Modyfikuj
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default TransactionsTable;