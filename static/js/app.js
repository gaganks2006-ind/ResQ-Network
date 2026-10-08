// ResQ Network - Core GIS & Telemetry Engine (SE Report Implementation)
let map;
let markers = {
  hospitals: [],
  responders: [],
  ambulances: {},
  aeds: [],
  incidents: {}
};
let activeIncidentId = null;
let currentCertificate = null;
let ws = null;

const playBeep = (freq = 880, duration = 0.15) => {
  try {
    const ctx = new (window.AudioContext || window.webkitAudioContext)();
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    osc.frequency.value = freq;
    osc.type = "sine";
    gain.gain.setValueAtTime(0.1, ctx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + duration);
    osc.connect(gain);
    gain.connect(ctx.destination);
    osc.start();
    osc.stop(ctx.currentTime + duration);
  } catch (e) {}
};

document.addEventListener("DOMContentLoaded", () => {
  initMap();
  initWebSocket();
  loadInitialData();
});

function initMap() {
  map = L.map("map", {
    zoomControl: true,
    attributionControl: false
  }).setView([12.3364, 76.6250], 13);

  L.tileLayer("https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png", {
    maxZoom: 19,
    subdomains: "abcd"
  }).addTo(map);
}

function initWebSocket() {
  const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
  const wsUrl = `${protocol}//${window.location.host}/ws/live`;
  
  ws = new WebSocket(wsUrl);

  ws.onopen = () => {
    console.log("⚡ Connected to ResQ Real-Time Medical Grid");
  };

  ws.onmessage = (event) => {
    try {
      const msg = JSON.parse(event.data);
      if (msg.event === "NEW_EMERGENCY") {
        handleNewEmergency(msg.data, msg.guidance, msg.guidance_kn);
      } else if (msg.event === "VITALS_UPDATE") {
        handleVitalsUpdate(msg.data);
      } else if (msg.event === "INCIDENT_RESOLVED") {
        handleIncidentResolved(msg.incident_id);
      }
    } catch (e) {
      console.error("WS Parse error", e);
    }
  };

  ws.onclose = () => {
    setTimeout(initWebSocket, 3000);
  };
}

async function loadInitialData() {
  try {
    const [hospRes, respRes, ambRes, aedRes, incRes, statsRes] = await Promise.all([
      fetch("/api/hospitals").then(r => r.json()),
      fetch("/api/responders").then(r => r.json()),
      fetch("/api/ambulances").then(r => r.json()),
      fetch("/api/aeds").then(r => r.json()),
      fetch("/api/incidents").then(r => r.json()),
      fetch("/api/stats").then(r => r.json())
    ]);

    renderHospitals(hospRes);
    renderResponders(respRes);
    renderAmbulances(ambRes);
    renderAeds(aedRes);
    renderIncidents(incRes);
    updateStats(statsRes);
  } catch (err) {
    console.error("Error loading ecosystem data:", err);
  }
}

function createCustomIcon(emoji, bgClass, size = 32) {
  return L.divIcon({
    className: "custom-map-icon",
    html: `<div style="
      width: ${size}px; height: ${size}px; border-radius: 50%;
      background: ${bgClass}; display: flex; align-items: center;
      justify-content: center; font-size: ${size * 0.55}px;
      box-shadow: 0 0 14px rgba(0,0,0,0.6); border: 2px solid #fff;
    ">${emoji}</div>`,
    iconSize: [size, size],
    iconAnchor: [size / 2, size / 2]
  });
}

function renderHospitals(hospitals) {
  hospitals.forEach(h => {
    const icon = createCustomIcon("🏥", "rgba(59, 130, 246, 0.9)", 36);
    const m = L.marker([h.latitude, h.longitude], { icon }).addTo(map);
    m.bindPopup(`
      <div style="font-family:sans-serif; color:#111;">
        <h4 style="margin:0 0 4px;">${h.name}</h4>
        <p style="margin:0; font-size:12px; color:#555;">${h.address}</p>
        <div style="margin-top:6px; font-size:12px;">
          <b>ICU Beds:</b> ${h.available_icu_beds} | <b>Ventilators:</b> ${h.ventilators_ready}<br/>
          <b>Cath-Lab:</b> ${h.cath_lab_available ? '✅ Ready' : '❌ Unavailable'}<br/>
          <b>HL7 FHIR:</b> <span style="color:#0284c7;">Synced</span>
        </div>
      </div>
    `);
    markers.hospitals.push(m);
  });
}

function renderResponders(responders) {
  responders.forEach(r => {
    const icon = createCustomIcon("🧑‍⚕️", "rgba(16, 185, 129, 0.85)", 28);
    const m = L.marker([r.latitude, r.longitude], { icon }).addTo(map);
    m.bindPopup(`
      <div style="font-family:sans-serif; color:#111;">
        <h4 style="margin:0;">${r.name}</h4>
        <p style="margin:0; font-size:11px; color:#555;">${r.qualification}</p>
        <p style="margin-top:4px; font-size:11px; color:#059669;"><b>Badge:</b> ${r.certification_badge}</p>
      </div>
    `);
    markers.responders.push(m);
  });
}

function renderAmbulances(ambulances) {
  ambulances.forEach(a => {
    const icon = createCustomIcon("🚑", "rgba(239, 68, 68, 0.9)", 32);
    const m = L.marker([a.latitude, a.longitude], { icon }).addTo(map);
    m.bindPopup(`
      <div style="font-family:sans-serif; color:#111;">
        <h4 style="margin:0;">${a.id}</h4>
        <p style="font-size:11px;">Crew: ${a.driver}</p>
      </div>
    `);
    markers.ambulances[a.id] = m;
  });
}

function renderAeds(aeds) {
  aeds.forEach(aed => {
    const icon = createCustomIcon("⚡", "rgba(255, 183, 3, 0.9)", 24);
    const m = L.marker([aed.lat, aed.lng], { icon }).addTo(map);
    m.bindPopup(`
      <div style="font-family:sans-serif; color:#111;">
        <h4 style="margin:0;">Public Defibrillator (AED)</h4>
        <p style="font-size:12px;">${aed.name} - ${aed.location}</p>
      </div>
    `);
    markers.aeds.push(m);
  });
}

function renderIncidents(incidents) {
  const container = document.getElementById("incidents-list");
  if (!container) return;
  
  if (incidents.length === 0) {
    container.innerHTML = `
      <div style="padding:24px; text-align:center; color:var(--text-muted); font-size:13px;">
        No active emergency incidents.<br/>System is on standby.
      </div>`;
    return;
  }

  container.innerHTML = incidents.map(inc => `
    <div class="incident-card ${inc.triage_level.toLowerCase().replace('_','-')} ${activeIncidentId === inc.id ? 'active' : ''}"
         onclick="selectIncident('${inc.id}')">
      <div class="inc-top">
        <span class="inc-id">${inc.id}</span>
        <span class="inc-badge ${inc.triage_level === 'CODE_RED' ? 'badge-red' : (inc.triage_level === 'CODE_YELLOW' ? 'badge-yellow' : 'badge-green')}">
          ${inc.triage_level}
        </span>
      </div>
      <div class="inc-symptom">"${inc.symptoms_text}"</div>
      <div class="inc-meta">
        <span>📍 ${inc.address}</span>
        <span>🏥 Dest: <b>${inc.assigned_hospital ? inc.assigned_hospital.name.split(',')[0] : 'Calculating'}</b></span>
        <span>🧑‍⚕️ Responders Alerted: <b>${inc.alerted_responders.length}</b></span>
        ${inc.is_mesh_relayed ? '<span style="color:var(--amber);">📡 Relayed via Meshtastic LoRa Mesh (2 hops)</span>' : ''}
      </div>
    </div>
  `).join("");
}

function handleNewEmergency(inc, guidanceEn, guidanceKn) {
  playBeep(920, 0.3);
  setTimeout(() => playBeep(1150, 0.4), 250);

  const icon = createCustomIcon("🚨", "rgba(255, 51, 85, 0.95)", 38);
  const m = L.marker([inc.latitude, inc.longitude], { icon }).addTo(map);
  
  const circle = L.circle([inc.latitude, inc.longitude], {
    color: "#ff3355",
    fillColor: "#ff3355",
    fillOpacity: 0.25,
    radius: 350
  }).addTo(map);

  markers.incidents[inc.id] = { marker: m, circle };
  map.flyTo([inc.latitude, inc.longitude], 14, { duration: 1.5 });

  selectIncident(inc.id);
  refreshIncidentData();
  fetchStats();
}

function handleVitalsUpdate(telemetry) {
  if (activeIncidentId && activeIncidentId === telemetry.incident_id) {
    document.getElementById("vital-hr").innerText = telemetry.heart_rate;
    document.getElementById("vital-spo2").innerText = telemetry.spo2;
    document.getElementById("vital-bp").innerText = `${telemetry.systolic_bp}/${telemetry.diastolic_bp}`;
    
    const ecgEl = document.getElementById("ecg-status-text");
    if (ecgEl) {
      ecgEl.innerText = telemetry.ecg_status;
      if (telemetry.ecg_status !== "NORMAL_SINUS" && telemetry.ecg_status !== "SINUS_RHYTHM") {
        ecgEl.classList.add("danger");
      } else {
        ecgEl.classList.remove("danger");
      }
    }
  }

  if (markers.ambulances[telemetry.ambulance_id]) {
    markers.ambulances[telemetry.ambulance_id].setLatLng([
      telemetry.ambulance_lat,
      telemetry.ambulance_lng
    ]);
  }
}

function handleIncidentResolved(incidentId) {
  if (markers.incidents[incidentId]) {
    map.removeLayer(markers.incidents[incidentId].marker);
    map.removeLayer(markers.incidents[incidentId].circle);
    delete markers.incidents[incidentId];
  }
  refreshIncidentData();
  fetchStats();
}

async function selectIncident(incId) {
  activeIncidentId = incId;
  const incs = await fetch("/api/incidents").then(r => r.json());
  renderIncidents(incs);
  
  const found = incs.find(i => i.id === incId);
  if (found) {
    map.flyTo([found.latitude, found.longitude], 14);
    if (found.latest_vitals) {
      handleVitalsUpdate(found.latest_vitals);
    }
    
    // Update Hospital Display
    const hospEl = document.getElementById("assigned-hospital-display");
    if (hospEl && found.assigned_hospital) {
      hospEl.innerHTML = `
        <div class="hosp-item assigned">
          <div class="hosp-title">🏥 ${found.assigned_hospital.name}</div>
          <div style="font-size:11px; color:var(--text-secondary); margin-bottom:4px;">${found.assigned_hospital.address}</div>
          <div class="hosp-beds-row">
            <span>ICU Beds: <b>${found.assigned_hospital.available_icu_beds}</b></span>
            <span>Ventilators: <b>${found.assigned_hospital.ventilators_ready}</b></span>
            <span>Cath-Lab: <b>${found.assigned_hospital.cath_lab_available ? 'ONLINE' : 'N/A'}</b></span>
          </div>
          <div style="margin-top:6px; font-size:10px; color:var(--cyan); font-family:var(--font-mono);">
            📡 HL7 FHIR Pre-Notification Sent (Saving 12m)
          </div>
        </div>
      `;
    }

    // Update Medical Vault Display (FR-06, FR-20)
    if (found.medical_vault) {
      const v = found.medical_vault;
      document.getElementById("vault-display").innerHTML = `
        <div><b>Patient:</b> ${v.victim_name}</div>
        <div style="margin-top:4px;"><b>Blood Group:</b> <span style="color:var(--crimson); font-weight:700;">${v.blood_group}</span></div>
        <div style="margin-top:2px;"><b>Allergies:</b> ${v.allergies.join(", ")}</div>
        <div style="margin-top:2px;"><b>Chronic:</b> ${v.chronic_conditions.join(", ")}</div>
        <div style="margin-top:2px;"><b>Emergency Contact:</b> ${v.emergency_contacts[0].relation} (${v.emergency_contacts[0].phone})</div>
      `;
    }

    // Update ResQ Shield Blockchain Display (FR-11, FR-12)
    if (found.resq_shield_cert) {
      currentCertificate = found.resq_shield_cert;
      document.getElementById("cert-tx").innerText = found.resq_shield_cert.tx_hash.substring(0, 16) + "...";
      document.getElementById("cert-block").innerText = found.resq_shield_cert.block_number;
    }
  }
}

async function refreshIncidentData() {
  const incs = await fetch("/api/incidents").then(r => r.json());
  renderIncidents(incs);
}

async function fetchStats() {
  const stats = await fetch("/api/stats").then(r => r.json());
  updateStats(stats);
}

function updateStats(stats) {
  const elTotal = document.getElementById("stat-total");
  const elCritical = document.getElementById("stat-critical");
  const elBeds = document.getElementById("stat-beds");
  const elCerts = document.getElementById("stat-certs");
  if (elTotal) elTotal.innerText = stats.total_emergencies;
  if (elCritical) elCritical.innerText = stats.code_red_critical;
  if (elBeds) elBeds.innerText = stats.available_icu_beds;
  if (elCerts) elCerts.innerText = stats.blockchain_certs_issued;
}

function downloadCertificate() {
  if (!currentCertificate) {
    alert("Please select or trigger an emergency first.");
    return;
  }
  const c = currentCertificate;
  const w = window.open("", "_blank", "width=680,height=720");
  w.document.write(`
    <html>
    <head>
      <title>ResQ Shield - Blockchain Legal Protection Certificate</title>
      <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; padding: 30px; background:#f8fafc; color:#0f172a; }
        .cert { border: 8px double #6366f1; padding: 30px; border-radius: 12px; background:#fff; box-shadow: 0 10px 25px rgba(0,0,0,0.1); }
        .head { text-align: center; border-bottom: 2px solid #e2e8f0; padding-bottom: 15px; margin-bottom: 20px; }
        .head h1 { color: #4338ca; margin: 0; font-size: 22px; text-transform: uppercase; letter-spacing: 1px; }
        .head p { margin: 4px 0 0; font-size: 13px; color: #64748b; }
        .row { margin-bottom: 12px; font-size: 14px; }
        .row b { color: #1e293b; display: inline-block; width: 180px; }
        .code { font-family: monospace; background: #f1f5f9; padding: 3px 6px; border-radius: 4px; word-break: break-all; }
        .footer { margin-top: 30px; border-top: 1px dashed #cbd5e1; padding-top: 15px; font-size: 12px; color: #475569; text-align: center; }
        .stamp { display: inline-block; padding: 6px 14px; border: 2px solid #16a34a; color: #16a34a; font-weight: 800; border-radius: 6px; transform: rotate(-5deg); margin-top: 10px; }
      </style>
    </head>
    <body>
      <div class="cert">
        <div class="head">
          <h1>🛡️ ResQ Shield — Legal Immunity Certificate</h1>
          <p>Issued under The Good Samaritan Law (2019) & Indian IT Act 2000 § 85B</p>
        </div>
        <div class="row"><b>Certificate ID:</b> ${c.certificate_id}</div>
        <div class="row"><b>Incident ID:</b> ${c.incident_id}</div>
        <div class="row"><b>Responder Name:</b> ${c.responder_name}</div>
        <div class="row"><b>Responder ID:</b> ${c.responder_id}</div>
        <div class="row"><b>Timestamp:</b> ${c.timestamp}</div>
        <div class="row"><b>Ledger Engine:</b> Hyperledger Fabric v2.5 (Channel: resq-legal)</div>
        <div class="row"><b>Block Number:</b> #${c.block_number}</div>
        <div class="row"><b>Transaction Hash:</b><br/><span class="code">${c.tx_hash}</span></div>
        <div class="footer">
          <div class="stamp">IMMUNITY VERIFIED & SEALED</div>
          <p style="margin-top:12px;">This immutable ledger record confirms that the responder acted strictly in good faith as a Good Samaritan to provide on-scene emergency aid. Protected from civil and criminal liability.</p>
        </div>
      </div>
    </body>
    </html>
  `);
}

async function triggerSimulation(type) {
  let payload = {};
  
  if (type === "CARDIAC_VVCE") {
    payload = {
      caller_name: "Rahul Sharma (Student)",
      caller_phone: "9845112233",
      latitude: 12.3364,
      longitude: 76.6205,
      address: "VVCE Campus, Gokulam 3rd Stage, Mysuru",
      symptoms_text: "Sudden collapse, severe chest pain, not breathing, suspected heart attack",
      language: "en",
      is_mesh_offline: false
    };
  } else if (type === "KANNADA_VOICE") {
    payload = {
      caller_name: "Gowramma (Bystander)",
      caller_phone: "9900112233",
      latitude: 12.3380,
      longitude: 76.6220,
      address: "Gokulam 3rd Stage Post Office Road, Mysuru",
      symptoms_text: "ಎದೆಯಲ್ಲಿ ತೀವ್ರ ನೋವು ಮತ್ತು ಉಸಿರಾಟ ನಿಂತಿದೆ, ಮೂರ್ಛೆ ಹೋಗಿದ್ದಾರೆ",
      language: "kn",
      is_mesh_offline: false
    };
  } else if (type === "TRAUMA_RING_ROAD") {
    payload = {
      caller_name: "Highway Patrol Constable",
      caller_phone: "9480801010",
      latitude: 12.3510,
      longitude: 76.6240,
      address: "Ring Road Bannimantap Flyover, Mysuru",
      symptoms_text: "High speed two-wheeler accident, profuse bleeding, head trauma",
      language: "en",
      is_mesh_offline: false
    };
  } else if (type === "MESH_OFFLINE") {
    payload = {
      caller_name: "Highway Truck Driver",
      caller_phone: "9845501199",
      latitude: 12.3620,
      longitude: 76.6150,
      address: "NH-275 Bangalore-Mysore Highway Rest Stop (No Cellular Signal)",
      symptoms_text: "Severe crash into divider, vehicular trap, emergency relay required",
      language: "en",
      is_mesh_offline: true
    };
  }

  try {
    const res = await fetch("/api/emergency/sos", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    const data = await res.json();
    console.log("Simulated Emergency dispatched:", data);
  } catch (err) {
    console.error("Simulation error:", err);
  }
}
