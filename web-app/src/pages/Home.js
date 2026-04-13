import { Link } from "react-router-dom";

function Home() {
  return (
    <div className="container">
      <h1>🔐 QR Payment Security</h1>

      <p style={{ color: "#475569", marginTop: "10px" }}>
        Scan QR codes and detect fraud using AI-powered analysis
      </p>

      <div style={{ marginTop: "30px" }}>
        <Link to="/scan">
          <button>🚀 Start Scanning</button>
        </Link>
      </div>
    </div>
  );
}

export default Home;