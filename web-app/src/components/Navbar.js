import React from "react";
import { Link } from "react-router-dom";

function Navbar() {
  return (
    <div className="navbar">
      <h2>QR Shield 🔒</h2>
      <div>
        <Link to="/" style={{ color: "white", marginRight: 10 }}>Home</Link>
        <Link to="/scan" style={{ color: "white" }}>Scan</Link>
      </div>
    </div>
  );
}

export default Navbar;