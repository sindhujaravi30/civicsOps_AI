import { useEffect, useState } from "react";
import { getHealth } from "../services/api";


function ApiStatus() {
  const [status, setStatus] = useState("checking");
  const [service, setService] = useState("");
  const [version, setVersion] = useState("");
  const [error, setError] = useState("");


  useEffect(() => {
    async function checkApiHealth() {
      try {
        const data = await getHealth();

        setStatus(data.status);
        setService(data.service);
        setVersion(data.version);
      } catch (err) {
        setStatus("unhealthy");
        setError(err.message);
      }
    }

    checkApiHealth();
  }, []);


  if (status === "checking") {
    return (
      <section className="status-card">
        <div className="status-dot checking"></div>

        <div>
          <h2>API Status</h2>
          <p>Checking backend...</p>
        </div>
      </section>
    );
  }


  if (status === "unhealthy") {
    return (
      <section className="status-card">
        <div className="status-dot unhealthy"></div>

        <div>
          <h2>API Status</h2>
          <p>Backend unavailable</p>

          {error && (
            <small>{error}</small>
          )}
        </div>
      </section>
    );
  }


  return (
    <section className="status-card">
      <div className="status-dot healthy"></div>

      <div>
        <h2>API Status</h2>

        <p>
          Backend is <strong>healthy</strong>
        </p>

        <div className="service-details">
          <span>Service: {service}</span>
          <span>Version: {version}</span>
        </div>
      </div>
    </section>
  );
}

export default ApiStatus;