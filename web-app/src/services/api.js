export const scanQRText = async (text) => {
  try {
    const response = await fetch("http://127.0.0.1:8000/api/v1/scan-text", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ data: text }),
    });

    return await response.json();
  } catch (err) {
    console.error(err);
    throw err;
  }
};