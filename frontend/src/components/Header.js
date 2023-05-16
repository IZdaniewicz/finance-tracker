export default function Header(props) {
    return (
      <header className="bg-dark text-white py-5 text-center">
        <div className="container">
          <h1>{props.title}</h1>
          <p className="lead"></p>
        </div>
      </header>
    );
  }
  