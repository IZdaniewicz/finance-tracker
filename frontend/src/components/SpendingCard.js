export default function SpendingCard({ spending }) {
  return (
    <div className="col">
      <div className="card h-100">
        <div className="card-body">
          <h5 className="card-title">{spending.attributes.goal_money}PLN</h5>
          <p className="card-text">{spending.attributes.to_go_date}</p>
          <button type="button" className="btn btn-primary">
            Szczegóły
          </button>
        </div>
      </div>
    </div>
  );
}
