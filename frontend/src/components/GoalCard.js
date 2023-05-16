export default function SpendingCard({ goal }) {
  return (
    <div className="col">
      <div className="card h-100">
        <div className="card-body">
          <h5 className="card-title">{goal.attributes.goal_money}PLN</h5>
          <p className="card-text">{goal.attributes.description}</p>
          <button type="button" className="btn btn-primary">
            Szczegóły
          </button>
        </div>
      </div>
    </div>
  );
}
