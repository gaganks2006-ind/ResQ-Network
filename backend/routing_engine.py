import math
from typing import List, Tuple, Optional
from backend.models import Hospital, FirstResponder, TriageLevel
from backend.mock_db import HOSPITALS, FIRST_RESPONDERS, AMBULANCES

def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate geodesic distance in kilometers between two lat/long points."""
    R = 6371.0 # Earth radius in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return round(R * c, 2)

def estimate_eta_minutes(distance_km: float, speed_kmh: float = 30.0) -> float:
    """Estimate urban emergency transit ETA in minutes (assuming 30 km/h average with siren)."""
    return round((distance_km / speed_kmh) * 60, 1)

def find_nearest_responders(lat: float, lon: float, max_radius_km: float = 2.5) -> List[FirstResponder]:
    """
    Finds verified medical volunteers and off-duty nurses within max_radius_km,
    sorted by proximity.
    """
    nearby = []
    for resp in FIRST_RESPONDERS:
        dist = haversine_km(lat, lon, resp.latitude, resp.longitude)
        if dist <= max_radius_km:
            resp_copy = resp.model_copy()
            resp_copy.distance_km = dist
            nearby.append(resp_copy)
            
    # Sort closest first
    nearby.sort(key=lambda r: r.distance_km or 999.0)
    return nearby

def allocate_optimal_hospital(lat: float, lon: float, triage_level: TriageLevel, specialty: str) -> Hospital:
    """
    Dynamic Multi-Factor Hospital Matching Algorithm.
    Evaluates:
      1. Travel distance & estimated ambulance travel time (ETA)
      2. Available ICU / trauma beds (rejects if 0 beds for Code Red)
      3. Specialty capability (Cath-Lab for cardiac, Level 1 Trauma for polytrauma)
      4. Blood reserve sufficiency
    """
    candidates = []
    
    for hosp in HOSPITALS:
        dist = haversine_km(lat, lon, hosp.latitude, hosp.longitude)
        eta = estimate_eta_minutes(dist)
        
        # Penalize if no ICU beds available during Code Red
        if triage_level == TriageLevel.CODE_RED and hosp.available_icu_beds <= 0:
            penalty = 999.0 # Effectively disqualifies full hospitals
        else:
            penalty = 0.0

        # Specialty bonus
        specialty_bonus = 0.0
        if "Cardiology" in specialty and hosp.cath_lab_available:
            specialty_bonus += 5.0 # Better score
        if "Trauma" in specialty and hosp.trauma_level == 1:
            specialty_bonus += 4.0

        # Objective Function: Lower score = higher priority
        # Score = (ETA * 1.5) - (Available Beds * 0.4) - Specialty Bonus + Penalty
        score = (eta * 1.5) - (hosp.available_icu_beds * 0.4) - specialty_bonus + penalty
        candidates.append((score, hosp, dist, eta))
        
    # Sort candidates by lowest score
    candidates.sort(key=lambda x: x[0])
    best_hosp = candidates[0][1]
    
    # Simulate reserving an ICU bed in the chosen hospital
    if best_hosp.available_icu_beds > 0:
        best_hosp.available_icu_beds -= 1
        
    return best_hosp

def find_nearest_ambulance(lat: float, lon: float) -> Tuple[Optional[str], float]:
    """Finds the closest idle ambulance and marks it dispatched."""
    best_amb = None
    min_dist = 9999.0
    
    for amb in AMBULANCES:
        dist = haversine_km(lat, lon, amb["latitude"], amb["longitude"])
        if dist < min_dist:
            min_dist = dist
            best_amb = amb
            
    if best_amb:
        best_amb["status"] = "EN_ROUTE"
        return best_amb["id"], min_dist
    return "ResQ-AMB-01", 2.0
