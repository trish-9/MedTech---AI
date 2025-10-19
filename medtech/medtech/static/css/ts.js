const chooseFileBtn = document.getElementById("chooseFileBtn");
const fileInput = document.getElementById("fileInput");
const scanBtn = document.getElementById("scanBtn");
const previewImage = document.getElementById("previewImage");
const resultBox = document.getElementById("resultBox");
const diagnosisText = document.getElementById("diagnosisText");

chooseFileBtn.addEventListener("click", () => fileInput.click());

fileInput.addEventListener("change", () => {
  const file = fileInput.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = e => {
      previewImage.src = e.target.result;
      previewImage.style.display = "block";
      resultBox.style.display = "none";
    };
    reader.readAsDataURL(file);
  }
});

scanBtn.addEventListener("click", async () => {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ video: true });
    const video = document.createElement("video");
    video.srcObject = stream;
    video.play();

    const capture = confirm("Camera opened. Press OK to capture image.");
    if (capture) {
      const canvas = document.createElement("canvas");
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      const ctx = canvas.getContext("2d");
      ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

      const imageData = canvas.toDataURL("image/png");
      previewImage.src = imageData;
      previewImage.style.display = "block";
      stream.getTracks().forEach(track => track.stop());

      await sendToBackend(imageData);
    }
  } catch (error) {
    alert("Camera access denied or unavailable!");
  }
});

async function sendToBackend(imageData) {
  resultBox.style.display = "block";
  diagnosisText.textContent = "Analyzing... Please wait.";

  try {
    const response = await fetch("/api/diagnose", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ image: imageData })
    });

    const data = await response.json();
    diagnosisText.innerHTML = `
      <strong>Diagnosis:</strong> ${data.diagnosis}<br>
      <strong>Confidence:</strong> ${(data.confidence * 100).toFixed(2)}%<br>
      <em>${data.details}</em>
    `;
  } catch (err) {
    diagnosisText.textContent = "Error: Unable to fetch result from server.";
  }
}