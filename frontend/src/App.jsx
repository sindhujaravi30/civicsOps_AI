import Header from "./components/Header";
import ApiStatus from "./components/ApiStatus";
import "./App.css";


function App() {
  return (
    <div className="app">
      <Header />

      <main className="main-content">
        <section className="hero">
          <p className="eyebrow">
            Civic technology platform
          </p>

          <h2>
            Intelligent government services,
            <br />
            powered by AI.
          </h2>

          <p className="description">
            CivicOps AI will provide bilingual,
            reliable AI assistance for government
            services and workflows.
          </p>
        </section>

        <ApiStatus />
      </main>
    </div>
  );
}

export default App;