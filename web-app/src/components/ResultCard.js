function ResultCard({ result }) {
  if (!result) return null;

  const status = result?.status || "unknown";

  return (
    <div className={`card ${status}`}>
      <h2>
        {status === "fraud" ? "🚨 FRAUD DETECTED" : "✅ SAFE"}
      </h2>

      <p><b>UPI:</b> {result?.upi_id || "N/A"}</p>
      <p><b>Merchant:</b> {result?.merchant || "Unknown"}</p>
      <p><b>Provider:</b> {result?.provider || "N/A"}</p>
      <p><b>Risk Score:</b> {result?.risk_score ?? "N/A"}</p>

      <p>{result?.message || "No message available"}</p>
    </div>
  );
}

export default ResultCard;  // ✅ VERY IMPORTANT