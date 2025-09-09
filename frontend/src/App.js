import React, { useState } from "react";
import axios from "axios";

function App() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);

  const backendURL = "http://127.0.0.1:8000";

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleProcessImage = async () => {
    if (!file) return alert("Odaberi sliku prvo.");

    const formData = new FormData();
    // Backend očekuje polje "file", ne "image"
    formData.append("file", file);

    try {
      const res = await axios.post(
        `${backendURL}/process_parking_image/`,
        formData,
        {
          headers: { "Content-Type": "multipart/form-data" },
          responseType: "blob", // backend vraća sliku (StreamingResponse)
        }
      );

      // Pretvori primljeni blob u URL za prikaz slike
      const imageURL = URL.createObjectURL(res.data);
      setResult({ image: imageURL });
    } catch (err) {
      console.error(err);
      alert("Greška prilikom slanja slike.");
    }
  };

  const handleGetLastResult = async () => {
    try {
      const res = await axios.get(`${backendURL}/last-result`);
      setResult(res.data);
    } catch (err) {
      console.error(err);
      alert("Greška kod dohvaćanja zadnjeg rezultata.");
    }
  };

  const handleRenderAndDownload = async () => {
    if (!file) return alert("Odaberi video fajl prvo.");

    const formData = new FormData();
    formData.append("file", file); // backend očekuje "file"

    try {
      const res = await axios.post(
        `${backendURL}/render-and-download`,
        formData,
        { responseType: "blob" }
      );

      const url = window.URL.createObjectURL(new Blob([res.data]));
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", "parking_result.mp4");
      document.body.appendChild(link);
      link.click();
    } catch (err) {
      console.error(err);
      alert("Greška kod renderanja ili preuzimanja.");
    }
  };

  return (
    <div style={{ padding: "2rem" }}>
      <h1>Parking Detection App</h1>

      <input type="file" onChange={handleFileChange} />
      <br />
      <br />

      <button onClick={handleProcessImage}>📤 Pošalji sliku</button>
      <button onClick={handleGetLastResult}>📊 Zadnji rezultat</button>
      <button onClick={handleRenderAndDownload}>⬇️ Render i preuzmi</button>

      <div style={{ marginTop: "2rem" }}>
        {result?.image && (
          <img
            src={result.image}
            alt="Processed parking"
            style={{ maxWidth: "100%", border: "1px solid #ccc" }}
          />
        )}
        {result?.free_slots !== undefined && (
          <pre
            style={{
              background: "#f0f0f0",
              padding: "1rem",
              marginTop: "1rem",
            }}
          >
            {JSON.stringify(result, null, 2)}
          </pre>
        )}
      </div>
    </div>
  );
}

export default App;
