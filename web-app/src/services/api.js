// 🔗 Backend Base URL (REPLACE with your Render URL)
const BASE_URL = "https://final-project-evuj.onrender.com";

// 📷 Scan QR Text (Camera input)
export const scanQRText = async (text) => {
  try {
    const response = await fetch(`${BASE_URL}/api/v1/scan-text`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ data: text }),
    });

    if (!response.ok) {
      throw new Error("Failed to scan QR text");
    }

    return await response.json();
  } catch (err) {
    console.error("QR Text Scan Error:", err);
    throw err;
  }
};

// 📤 Scan QR Image (Upload)
export const scanQRImage = async (file) => {
  try {
    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch(`${BASE_URL}/api/v1/scan`, {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      throw new Error("Failed to scan QR image");
    }

    return await response.json();
  } catch (err) {
    console.error("QR Image Scan Error:", err);
    throw err;
  }
};

// ❤️ Health Check (optional)
export const checkHealth = async () => {
  try {
    const response = await fetch(`${BASE_URL}/health`);

    if (!response.ok) {
      throw new Error("Backend not healthy");
    }

    return await response.json();
  } catch (err) {
    console.error("Health Check Error:", err);
    throw err;
  }
};