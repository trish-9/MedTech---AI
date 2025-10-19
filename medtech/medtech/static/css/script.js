async function fetchVitals() {
  const res = await fetch('/api/vitals');
  const data = await res.json();
  updateTable(data);
  drawChart(data);
  loadInsight();
}

function updateTable(data) {
  const tbody = document.querySelector('#vitalsTable tbody');
  tbody.innerHTML = '';
  data.forEach(v => {
    tbody.innerHTML += `<tr>
      <td>${v.date}</td>
      <td>${v.bp}</td>
      <td>${v.hr}</td>
      <td>${v.spo2}</td>
    </tr>`;
  });
}

let chart;
function drawChart(data) {
  const ctx = document.getElementById('vitalsChart').getContext('2d');
  const labels = data.map(v => v.date);
  const bp = data.map(v => v.bp);
  const hr = data.map(v => v.hr);
  const spo2 = data.map(v => v.spo2);

  if (chart) chart.destroy();
  chart = new Chart(ctx, {
    type: 'line',
    data: {
      labels,
      datasets: [
        { label: 'BP', data: bp, borderColor: '#5bc0be', tension: 0.4 },
        { label: 'Heart Rate', data: hr, borderColor: '#f6ae2d', tension: 0.4 },
        { label: 'SpO₂', data: spo2, borderColor: '#d81159', tension: 0.4 }
      ]
    },
    options: { responsive: true, scales: { y: { beginAtZero: false } } }
  });
}

async function addVital() {
  const bp = document.getElementById('bp').value;
  const hr = document.getElementById('hr').value;
  const spo2 = document.getElementById('spo2').value;

  await fetch('/api/add', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ bp, hr, spo2 })
  });
  fetchVitals();
}

async function simulate() {
  await fetch('/api/simulate');
  fetchVitals();
}

async function loadInsight() {
  const res = await fetch('/api/insight');
  const data = await res.json();
  document.getElementById('insight').innerHTML = `
    <h3>Health Score: ${data.score}/100</h3>
    <ul>${data.advice.map(a => `<li>${a}</li>`).join('')}</ul>
  `;
}

window.onload = fetchVitals;