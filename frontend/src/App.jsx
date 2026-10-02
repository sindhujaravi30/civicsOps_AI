import Header from "./components/Header";
import ApiStatus from "./components/ApiStatus";
import Chat from "./components/Chat";

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
            CivicOps AI provides an extensible
            foundation for bilingual AI-assisted
            government services.
          </p>

        </section>


        <ApiStatus />

        <Chat />

      </main>

    </div>
  );
}


export default App;