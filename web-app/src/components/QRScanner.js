import { useEffect, useRef, useState } from "react";
import { Html5Qrcode } from "html5-qrcode";

function QRScanner({ onScan }) {
  const scannerRef = useRef(null);
  const [scanning, setScanning] = useState(false);
const [isRunning, setIsRunning] = useState(false);


  useEffect(() => {
    scannerRef.current = new Html5Qrcode("reader");

    return () => {
      // 🔥 SAFE CLEANUP
      if (scannerRef.current && scanning) {
        scannerRef.current.stop().catch(() => {});
      }
    };
  }, [scanning]);

  const startScan = async () => {
    if (!scannerRef.current || scanning) return;

    try {
      await scannerRef.current.start(
        { facingMode: "environment" },
        { fps: 10, qrbox: 250 },
        (decodedText) => {
          onScan(decodedText);
          stopScan();
        },
        () => {}
      );

      setScanning(true);
    } catch (err) {
      console.log("Start error:", err);
    }
  };

const stopScan = async () => {
  try {
    if (scannerRef.current) {
      const state = scannerRef.current.getState();

      if (state === 2) { // 2 = scanning
        await scannerRef.current.stop();
        await scannerRef.current.clear();
        setIsRunning(false);
      }
    }
  } catch (err) {
    console.log("Safe stop:", err);
  }
};

  return (
    <div style={{ textAlign: "center" }}>
      <div id="reader" style={{ width: "300px", margin: "auto" }} />

      <div style={{ marginTop: "15px" }}>
        {!scanning ? (
          <button onClick={startScan}>📷 Start Scan</button>
        ) : (
          <button onClick={stopScan}>🛑 Stop</button>
        )}
      </div>
    </div>
  );
}

export default QRScanner;