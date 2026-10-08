from typing import List, Dict
from datetime import datetime
from backend.models import Hospital, FirstResponder, Incident, TriageLevel

# Mysuru Healthcare Ecosystem - Live Resource Registry
HOSPITALS: List[Hospital] = [
    Hospital(
        id="HOSP-01",
        name="Manipal Hospital (Columbia Asia), Mysuru",
        address="Bangalore-Mysore Ring Road Junction, Bannimantap",
        latitude=12.3489,
        longitude=76.6264,
        total_beds=180,
        available_icu_beds=7,
        ventilators_ready=4,
        cath_lab_available=True,
        trauma_level=1,
        blood_inventory={"O+": 14, "O-": 4, "A+": 9, "B+": 11, "AB+": 5},
        contact="+91 821 398 6666",
        rating=4.9
    ),
    Hospital(
        id="HOSP-02",
        name="Apollo BGS Hospitals, Mysuru",
        address="Adichunchanagiri Road, Kuvempunagar",
        latitude=12.2882,
        longitude=76.6432,
        total_beds=220,
        available_icu_beds=12,
        ventilators_ready=8,
        cath_lab_available=True,
        trauma_level=1,
        blood_inventory={"O+": 22, "O-": 6, "A+": 15, "B+": 18, "AB+": 7},
        contact="+91 821 256 8888",
        rating=4.8
    ),
    Hospital(
        id="HOSP-03",
        name="K.R. Hospital (MMCRI Apex Trauma)",
        address="Sayyaji Rao Road, Near Mysuru Palace",
        latitude=12.3168,
        longitude=76.6506,
        total_beds=1050,
        available_icu_beds=18,
        ventilators_ready=11,
        cath_lab_available=True,
        trauma_level=1,
        blood_inventory={"O+": 35, "O-": 8, "A+": 24, "B+": 30, "AB+": 12},
        contact="+91 821 242 0100",
        rating=4.6
    ),
    Hospital(
        id="HOSP-04",
        name="JSS Hospital, Mysuru",
        address="M.G. Road, Agrahara",
        latitude=12.2982,
        longitude=76.6582,
        total_beds=1800,
        available_icu_beds=24,
        ventilators_ready=14,
        cath_lab_available=True,
        trauma_level=1,
        blood_inventory={"O+": 40, "O-": 10, "A+": 32, "B+": 36, "AB+": 15},
        contact="+91 821 233 5555",
        rating=4.7
    ),
    Hospital(
        id="HOSP-05",
        name="Narayana Multispeciality Hospital",
        address="Devanur, Near Ring Road, Mysuru",
        latitude=12.3275,
        longitude=76.6908,
        total_beds=250,
        available_icu_beds=9,
        ventilators_ready=5,
        cath_lab_available=True,
        trauma_level=2,
        blood_inventory={"O+": 16, "O-": 3, "A+": 10, "B+": 12, "AB+": 4},
        contact="+91 821 712 4000",
        rating=4.7
    )
]

# Certified Citizen First-Responders (Doctors, Nurses, Trained Volunteers in Gokulam / Mysuru)
FIRST_RESPONDERS: List[FirstResponder] = [
    FirstResponder(
        id="RES-01",
        name="Dr. Sneha Hegde",
        qualification="MD Emergency Medicine (Off-Duty)",
        phone="+91 94812 34501",
        latitude=12.3371,
        longitude=76.6212,
        status="AVAILABLE",
        verified=True
    ),
    FirstResponder(
        id="RES-02",
        name="Arjun Rao",
        qualification="Final Year MBBS (MMCRI) / BLS Certified",
        phone="+91 98450 88219",
        latitude=12.3355,
        longitude=76.6198,
        status="AVAILABLE",
        verified=True
    ),
    FirstResponder(
        id="RES-03",
        name="Kavya M.",
        qualification="Critical Care Nurse, Manipal Hospital",
        phone="+91 97401 12345",
        latitude=12.3382,
        longitude=76.6225,
        status="AVAILABLE",
        verified=True
    ),
    FirstResponder(
        id="RES-04",
        name="Rohan Gowda",
        qualification="Red Cross CPR Instructor / NCC Cadet",
        phone="+91 99002 98765",
        latitude=12.3340,
        longitude=76.6180,
        status="AVAILABLE",
        verified=True
    ),
    FirstResponder(
        id="RES-05",
        name="Pooja Kulkarni",
        qualification="Physiotherapist & First Aid Certified",
        phone="+91 94480 54321",
        latitude=12.3395,
        longitude=76.6238,
        status="AVAILABLE",
        verified=True
    )
]

# Active Ambulances
AMBULANCES: List[Dict] = [
    {
        "id": "ResQ-AMB-01",
        "driver": "Manjunath (Paramedic Crew Alpha)",
        "phone": "+91 98451 00101",
        "latitude": 12.3390,
        "longitude": 76.6210,
        "status": "IDLE", # IDLE, EN_ROUTE, AT_SCENE, HOSPITAL_BOUND
        "equipment": ["Advanced Ventilator", "Defibrillator", "Oxygen", "Suction"]
    },
    {
        "id": "ResQ-AMB-02",
        "driver": "Ramesh P (Trauma Unit Beta)",
        "phone": "+91 98451 00202",
        "latitude": 12.3250,
        "longitude": 76.6350,
        "status": "IDLE",
        "equipment": ["Automated CPR Device", "Cardiac Monitor", "Trauma Splints"]
    },
    {
        "id": "ResQ-AMB-03",
        "driver": "Siddharth (Cardiac Life Support)",
        "phone": "+91 98451 00303",
        "latitude": 12.3100,
        "longitude": 76.6450,
        "status": "IDLE",
        "equipment": ["ECG Telemetry", "External Pacemaker", "IV Infusion Pumps"]
    }
]

# In-Memory Active Incidents List
INCIDENTS: List[Incident] = []

# Public AED (Automated External Defibrillator) Locations
PUBLIC_AEDS: List[Dict] = [
    {"name": "VVCE Main Admin Block AED", "lat": 12.3364, "lng": 76.6205, "location": "Ground Floor Security Desk"},
    {"name": "Gokulam 3rd Stage Post Office AED", "lat": 12.3380, "lng": 76.6215, "location": "Entrance Lobby"},
    {"name": "Vontikoppal Temple Junction Public AED", "lat": 12.3312, "lng": 76.6310, "location": "Traffic Police Booth"},
    {"name": "Mysuru City Railway Station West Gate AED", "lat": 12.3160, "lng": 76.6440, "location": "Platform 1 Helpdesk"}
]
