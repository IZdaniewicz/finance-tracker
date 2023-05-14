export default function NavBar()
{
    return (
        <nav className="navbar navbar-expand-lg navbar-light bg-light">
        <div className="container">
          <a className="navbar-brand" href="#">
            FinanceTracker
          </a>
          <div
            className="collapse navbar-collapse justify-content-end"
            id="navbarNav"
          >
            <ul className="navbar-nav">
              <li className="nav-item">
                <a className="nav-link" href="/index.html">
                  Home
                </a>
              </li>
              <li className="nav-item">
                <a className="nav-link" href="/page1.html">
                  Transactions
                </a>
              </li>
              <li className="nav-item">
                <a className="nav-link" href="/login.html">
                  Settings
                </a>
              </li>
            </ul>
          </div>
        </div>
      </nav>
    )
}