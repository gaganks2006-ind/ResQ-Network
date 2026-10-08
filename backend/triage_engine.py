import re
from typing import Tuple, Dict, Any
from backend.models import TriageLevel

# Clinical Emergency Keyword Dictionary (Multi-lingual: English, Kannada, Phonetic Kannada/Hindi)
EMERGENCY_DICTIONARY = {
    "CARDIAC_ARREST": [
        "heart attack", "chest pain", "chest pressure", "cardiac", "collapsing", "unconscious",
        "no pulse", "cardiac arrest", "not breathing", "fainted suddenly", "jaw pain",
        # Kannada script & transliterated
        "ಎದೆ ನೋವು", "ಹೃದಯಾಘಾತ", "ಉಸಿರಾಟ ನಿಂತಿದೆ", "ಸ್ಪರ್ಶವಿಲ್ಲ", "ede novu", "hrudayaghata", "dil ka daura"
    ],
    "STROKE_NEURO": [
        "stroke", "facial droop", "slurred speech", "arm weakness", "paralysis", "sudden numbness",
        "seizure", "convulsions", "head injury", "bleeding from ear",
        # Kannada & transliterated
        "ಪಾರ್ಶ್ವವಾಯು", "ಮೂರ್ಛೆ", "ಮಾತು ತೊದಲುತ್ತಿದೆ", "ಬಾಯಿ ಸೊಟ್ಟಗಾಗಿದೆ", "parshwavayu", "moorche"
    ],
    "SEVERE_TRAUMA_HEMORRHAGE": [
        "profuse bleeding", "spurting blood", "severed", "deep wound", "gunshot", "stab wound",
        "high speed accident", "crush injury", "amputation", "severe burn", "bone sticking out",
        # Kannada & transliterated
        "ಭಾರಿ ರಕ್ತಸ್ರಾವ", "ಅಪಘಾತ", "ತೀವ್ರ ಗಾಯ", "ಮೂಳೆ ಮುರಿದಿದೆ", "rakthasrava", "apaghatha", "bhari gayagalu"
    ],
    "RESPIRATORY_DISTRESS": [
        "choking", "gasping for air", "cyanosis", "blue lips", "asthma attack", "anaphylaxis",
        "throat swelling", "cannot breathe", "stridor",
        # Kannada & transliterated
        "ಉಸಿರುಗಟ್ಟುವಿಕೆ", "ಉಸಿರಾಡಲು ಆಗುತ್ತಿಲ್ಲ", "usirugattuvike", "usiradata thondare"
    ],
    "URGENT_YELLOW": [
        "fracture", "broken arm", "broken leg", "dislocation", "deep cut", "high fever with rash",
        "vomiting blood", "moderate burn", "severe abdominal pain", "dog bite",
        "ಮುರಿತ", "ಕೈ ಮುರಿದಿದೆ", "ಕಾಲು ಮುರಿದಿದೆ", "ಹೊಟ್ಟೆ ನೋವು", "muritha", "hotte novu"
    ]
}

def analyze_symptoms(text: str) -> Dict[str, Any]:
    """
    Evaluates reported symptom text and assigns clinical triage level,
    recommended emergency specialty, and immediate on-scene bystander guidance.
    """
    cleaned = text.lower()
    
    # Check Code Red Categories
    for kw in EMERGENCY_DICTIONARY["CARDIAC_ARREST"]:
        if kw in cleaned:
            return {
                "triage_level": TriageLevel.CODE_RED,
                "severity_score": 98,
                "specialty_needed": "Interventional Cardiology & Intensive Care",
                "triage_reason": "Acute Cardiac Event / Suspected Myocardial Infarction or Arrest",
                "cpr_required": True,
                "bystander_guidance": (
                    "🚨 IMMEDIATELY CHECK RESPONSIVENESS AND BREATHING.\n"
                    "1. Place victim flat on their back on a firm surface.\n"
                    "2. Place heel of hand on center of chest. Interlock fingers.\n"
                    "3. Push HARD and FAST (100–120 compressions per minute) to 5-6 cm depth.\n"
                    "4. If an AED is available nearby, turn it on and attach pads immediately!"
                ),
                "bystander_guidance_kn": (
                    "🚨 ತಕ್ಷಣವೇ ಉಸಿರಾಟವನ್ನು ಪರೀಕ್ಷಿಸಿ.\n"
                    "1. ವ್ಯಕ್ತಿಯನ್ನು ಸಮತಟ್ಟಾದ ಗಟ್ಟಿ ನೆಲದ ಮೇಲೆ ಮಲಗಿಸಿ.\n"
                    "2. ಎದೆಯ ಮಧ್ಯಭಾಗದಲ್ಲಿ ಎರಡೂ ಕೈಗಳನ್ನು ಜೋಡಿಸಿ ಬಲವಾಗಿ ಮತ್ತು ವೇಗವಾಗಿ (ನಿಮಿಷಕ್ಕೆ 100-120 ಬಾರಿ) ಒತ್ತಿರಿ (CPR).\n"
                    "3. ಹತ್ತಿರದಲ್ಲಿ AED ಲಭ್ಯವಿದ್ದರೆ ತಕ್ಷಣ ಬಳಸಿ."
                )
            }
            
    for kw in EMERGENCY_DICTIONARY["STROKE_NEURO"]:
        if kw in cleaned:
            return {
                "triage_level": TriageLevel.CODE_RED,
                "severity_score": 92,
                "specialty_needed": "Comprehensive Stroke Center / Neurology",
                "triage_reason": "Acute Cerebrovascular Event / Suspected Ischemic or Hemorrhagic Stroke",
                "cpr_required": False,
                "bystander_guidance": (
                    "🧠 FAST PROTOCOL DETECTED.\n"
                    "1. Note the exact time symptoms started.\n"
                    "2. Keep the patient lying on their side (recovery position) with head slightly elevated.\n"
                    "3. Do NOT give food, water, or aspirin (risk of choking or hemorrhage)."
                ),
                "bystander_guidance_kn": (
                    "🧠 ಪಾರ್ಶ್ವವಾಯು (Stroke) ಲಕ್ಷಣಗಳು:\n"
                    "1. ಲಕ್ಷಣ ಆರಂಭವಾದ ನಿಖರ ಸಮಯವನ್ನು ಗಮನಿಸಿ.\n"
                    "2. ರೋಗಿಯನ್ನು ಒಂದು ಬದಿಗೆ ತಿರುಗಿಸಿ ಮಲಗಿಸಿ (ಚೇತರಿಕೆ ಭಂಗಿ).\n"
                    "3. ಯಾವುದೇ ಆಹಾರ ಅಥವಾ ನೀರನ್ನು ನೀಡಬೇಡಿ."
                )
            }

    for kw in EMERGENCY_DICTIONARY["SEVERE_TRAUMA_HEMORRHAGE"]:
        if kw in cleaned:
            return {
                "triage_level": TriageLevel.CODE_RED,
                "severity_score": 95,
                "specialty_needed": "Apex Trauma Surgery & Massive Transfusion Service",
                "triage_reason": "High-Grade Trauma / Life-Threatening Hemorrhage",
                "cpr_required": False,
                "bystander_guidance": (
                    "🩸 BLEEDING CONTROL PROTOCOL:\n"
                    "1. Apply direct firm continuous pressure on the wound using clean cloth or trauma dressing.\n"
                    "2. If severe limb arterial bleeding does not stop, apply a tourniquet 2-3 inches above the wound.\n"
                    "3. Keep the patient warm and lying down to prevent hypovolemic shock."
                ),
                "bystander_guidance_kn": (
                    "🩸 ರಕ್ತಸ್ರಾವ ನಿಯಂತ್ರಣ:\n"
                    "1. ಗಾಯದ ಮೇಲೆ ಸ್ವಚ್ಛ ಬಟ್ಟೆಯಿಂದ ಬಲವಾಗಿ ನೇರ ಒತ್ತಡ ಹಾಕಿ.\n"
                    "2. ಕಾಲು ಅಥವಾ ಕೈಯಿಂದ ರಕ್ತಸ್ರಾವ ನಿಲ್ಲದಿದ್ದರೆ ಗಾಯದ 2-3 ಇಂಚು ಮೇಲೆ ಬಿಗಿಯಾಗಿ ಕಟ್ಟಿ.\n"
                    "3. ರೋಗಿಯನ್ನು ಬೆಚ್ಚಗಿರಿಸಿ."
                )
            }

    for kw in EMERGENCY_DICTIONARY["RESPIRATORY_DISTRESS"]:
        if kw in cleaned:
            return {
                "triage_level": TriageLevel.CODE_RED,
                "severity_score": 89,
                "specialty_needed": "Pulmonology & Intensive Care Unit",
                "triage_reason": "Acute Respiratory Distress / Airway Obstruction",
                "cpr_required": False,
                "bystander_guidance": (
                    "🫁 AIRWAY RESCUE:\n"
                    "1. If patient is choking and conscious, perform Heimlich maneuver (abdominal thrusts).\n"
                    "2. Loosen all tight clothing around neck and chest.\n"
                    "3. Keep patient in upright sitting position to maximize oxygen airflow."
                ),
                "bystander_guidance_kn": (
                    "🫁 ಉಸಿರಾಟದ ಬಿಕ್ಕಟ್ಟು:\n"
                    "1. ಗಂಟಲಿನಲ್ಲಿ ಏನಾದರೂ ಸಿಲುಕಿದ್ದರೆ ಹೊಟ್ಟೆಯ ಮೇಲ್ಭಾಗದಲ್ಲಿ ಒಳಮುಖವಾಗಿ ಒತ್ತಿರಿ (ಹೇಮ್ಲಿಕ್ ವಿಧಾನ).\n"
                    "2. ಕುತ್ತಿಗೆಯ ಬಟ್ಟೆಗಳನ್ನು ಸಡಿಲಗೊಳಿಸಿ ಮತ್ತು ನೇರವಾಗಿ ಕುಳ್ಳಿರಿಸಿ."
                )
            }

    for kw in EMERGENCY_DICTIONARY["URGENT_YELLOW"]:
        if kw in cleaned:
            return {
                "triage_level": TriageLevel.CODE_YELLOW,
                "severity_score": 65,
                "specialty_needed": "Orthopedics & Emergency Triage",
                "triage_reason": "Urgent Trauma / Unstable Fracture / Severe Pain",
                "cpr_required": False,
                "bystander_guidance": (
                    "⚠️ URGENT CARE PROTOCOL:\n"
                    "1. Immobilize the injured limb; do NOT attempt to straighten or force bones back.\n"
                    "2. Apply ice pack wrapped in cloth to reduce swelling.\n"
                    "3. Keep patient calm and stationary until paramedic crew arrives."
                ),
                "bystander_guidance_kn": (
                    "⚠️ ತುರ್ತು ಕಾಳಜಿ:\n"
                    "1. ಮುರಿದ ಕೈ ಅಥವಾ ಕಾಲನ್ನು ಅಲುಗಾಡಿಸಬೇಡಿ.\n"
                    "2. ಊತ ಕಡಿಮೆ ಮಾಡಲು ಐಸ್ ಬಟ್ಟೆಯನ್ನು ಇಡಿ. ಶಾಂತವಾಗಿರಿ."
                )
            }

    # Default fallback: Non-urgent or standard triage
    return {
        "triage_level": TriageLevel.CODE_GREEN,
        "severity_score": 35,
        "specialty_needed": "General Emergency Medicine",
        "triage_reason": "Sub-acute Condition / Minor Injury / General Medical Assessment",
        "cpr_required": False,
        "bystander_guidance": (
            "ℹ️ GENERAL CARE:\n"
            "1. Keep patient resting comfortably in a quiet area.\n"
            "2. Monitor vital signs (breathing and alertness) until medical team arrives."
        ),
        "bystander_guidance_kn": (
            "ℹ️ ಸಾಮಾನ್ಯ ಕಾಳಜಿ:\n"
            "1. ರೋಗಿಯನ್ನು ಆರಾಮದಾಯಕವಾಗಿ ಕೂರಿಸಿ.\n"
            "2. ವೈದ್ಯಕೀಯ ತಂಡ ಬರುವವರೆಗೆ ರೋಗಿಯ ಪ್ರಜ್ಞೆಯನ್ನು ಗಮನಿಸಿ."
        )
    }
