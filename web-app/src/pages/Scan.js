import { useState } from "react";
import QRScanner from "../components/QRScanner";
import ResultCard from "../components/ResultCard";
import Loader from "../components/Loader";
import { scanQRText } from "../services/api";

function Scan() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  // 🔊 SOUND
  const playSound = (type) => {
    const audio = new Audio(
      type === "fraud" ? "/alert.mp3" : "/success.mp3"
    );
    audio.play().catch(() => {});
  };

  // 📊 SAVE HISTORY
  const saveToHistory = (data) => {
    const existing = JSON.parse(localStorage.getItem("history")) || [];
    existing.unshift(data);
    localStorage.setItem("history", JSON.stringify(existing.slice(0, 10)));
  };

  // 📷 CAMERA
  const handleScan = async (text) => {
    setLoading(true);
    try {
      const res = await scanQRText(text);
      setResult(res);
      playSound(res.status === "fraud" ? "fraud" : "safe");
      saveToHistory(res);
    } catch {
      alert("Error scanning QR");
    }
    setLoading(false);
  };

  // 📤 UPLOAD
  const handleUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setLoading(true);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch("http://127.0.0.1:8000/api/v1/scan", {
        method: "POST",
        body: formData,
      });

      const data = await res.json();
      setResult(data);
      playSound(data.status === "fraud" ? "fraud" : "safe");
      saveToHistory(data);
    } catch {
      alert("Upload failed");
    }

    setLoading(false);
  };

  const history = JSON.parse(localStorage.getItem("history")) || [];

  return (
    <div className="container">

      {/* 🔊 ENABLE SOUND */}
      <button
        onClick={() => {
          const audio = new Audio("/success.mp3");
          audio.play();
        }}
      >
        🔊 Enable Sound
      </button>

      <h2>🔍 Scan QR Code</h2>
      <p style={{ color: "#64748b" }}>
        Scan or upload a QR to detect fraud instantly
      </p>

      {/* CAMERA */}
      <QRScanner onScan={handleScan} />

      {/* UPLOAD */}
      <div style={{ marginTop: "20px" }}>
        <p>OR</p>
        <input type="file" accept="image/*" onChange={handleUpload} />
      </div>

      {loading && <Loader />}

      <ResultCard result={result} />

      {/* HISTORY */}
      <div className="card">
        <h3>📊 Scan History</h3>

        {history.length === 0 && <p>No scans yet</p>}

        {history.map((item, index) => (
          <div key={index}>
            <b>{item.status || "unknown"}</b> — {item.upi_id || "Unknown"}
          </div>
        ))}
      </div>

    </div>
  );
}

export default Scan;