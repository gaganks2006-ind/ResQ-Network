from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from enum import Enum
from datetime import datetime

class TriageLevel(str, Enum):
    CODE_RED = "CODE_RED"       # Immediate threat to life (Cardiac, Stroke, Severe Hemorrhage)
    CODE_YELLOW = "CODE_YELLOW" # Urgent, potentially life-threatening if delayed (Fracture, Moderate Burn)
    CODE_GREEN = "CODE_GREEN"   # Non-urgent, stable condition

class MedicalVault(BaseModel):
    user_id: str
    victim_name: str = "Praveen Kumar"
    blood_group: str = "O Positive (O+)"
    allergies: List[str] = ["Penicillin", "Sulfa drugs"]
    chronic_conditions: List[str] = ["Type-2 Diabetes", "Hypertension"]
    current_medications: List[str] = ["Metformin 500mg", "Amlodipine 5mg"]
    emergency_contacts: List[Dict[str, str]] = [
        {"relation": "Spouse (Deepa)", "phone": "+91 98450 91823"},
        {"relation": "Brother (Vijay)", "phone": "+91 94812 44556"}
    ]
    is_unlocked: bool = False
    unlocked_at: Optional[str] = None

class ResQShieldCertificate(BaseModel):
    certificate_id: str
    incident_id: str
    responder_id: str
    responder_name: str
    tx_hash: str # Hyperledger Fabric SHA-256 hash
    block_number: int
    timestamp: str
    legal_statute: str = "The Good Samaritan Law (2019) & Indian IT Act 2000 Section 85B"
    verified: bool = True

class SceneAssessment(BaseModel):
    severity_score: int # 1 - 100
    detected_objects: List[str] = ["Deformed Vehicle", "Active Hemorrhage", "Unconscious Pedestrian"]
    ai_confidence: float = 0.94
    hazard_level: str = "HIGH_CRITICAL"
    tflite_latency_ms: int = 142

class IncidentCreate(BaseModel):
    caller_name: str = "Bystander"
    caller_phone: str = "9876543210"
    latitude: float
    longitude: float
    address: Optional[str] = "Gokulam 3rd Stage, Mysuru"
    symptoms_text: str
    language: str = "en"
    patient_estimated_age: Optional[int] = 30
    patient_gender: Optional[str] = "Unknown"
    is_mesh_offline: bool = False # Meshtastic LoRa relay simulation

class VitalsTelemetry(BaseModel):
    incident_id: str
    heart_rate: int = 88
    spo2: int = 98
    systolic_bp: int = 120
    diastolic_bp: int = 80
    ecg_status: str = "NORMAL_SINUS"
    ambulance_id: str
    ambulance_lat: float
    ambulance_lng: float
    timestamp: str

class Hospital(BaseModel):
    id: str
    name: str
    address: str
    latitude: float
    longitude: float
    total_beds: int
    available_icu_beds: int
    ventilators_ready: int
    cath_lab_available: bool
    trauma_level: int # 1 = Apex Tertiary, 2 = Secondary
    blood_inventory: Dict[str, int]
    contact: str
    rating: float = 4.8
    hl7_fhir_endpoint: str = "https://fhir.resq.org/v1/Hospital"

class FirstResponder(BaseModel):
    id: str
    name: str
    qualification: str
    phone: str
    latitude: float
    longitude: float
    distance_km: Optional[float] = 0.0
    status: str = "AVAILABLE" # AVAILABLE, DISPATCHED, ON_SCENE
    verified: bool = True
    certification_badge: str = "ResQ Certified BLS Level 2"

class Incident(BaseModel):
    id: str
    caller_name: str
    caller_phone: str
    latitude: float
    longitude: float
    address: str
    symptoms_text: str
    triage_level: TriageLevel
    triage_reason: str
    cpr_guidance_required: bool
    assigned_hospital: Optional[Hospital] = None
    assigned_ambulance_id: Optional[str] = None
    alerted_responders: List[FirstResponder] = []
    status: str = "DISPATCHED" # DETECTED, ASSESSING, DISPATCHING, RESPONDING, TRANSFERRING, CLOSED
    created_at: str
    medical_vault: Optional[MedicalVault] = None
    resq_shield_cert: Optional[ResQShieldCertificate] = None
    scene_assessment: Optional[SceneAssessment] = None
    is_mesh_relayed: bool = False
    mesh_hop_count: int = 0
    auto_escalated_112: bool = False
    latest_vitals: Optional[VitalsTelemetry] = None
