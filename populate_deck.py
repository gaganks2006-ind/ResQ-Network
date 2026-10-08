import sys
from pptx import Presentation

def update_presentation():
    input_pptx = r"C:\Users\Gagan K S\Documents\hackothon\Tech Shodha\Tech-Shodha_Presentation_Template.pptx"
    output_pptx = r"C:\Users\Gagan K S\Documents\hackothon\Tech Shodha\Tech-Shodha_ResQ_Network_Final_Presentation.pptx"
    
    prs = Presentation(input_pptx)
    
    # Slide 1 mapping
    slide1_map = {
        "Project title": "ResQ Network\nAI Emergency Medical Grid",
        "Team name": "Team EcoLogic",
        "Team members": "Gagan K S (Lead)  |  AI Dispatch, IoT Mesh, Cloud Telemetry, Legal Tech",
        "College or institution": "Vidyavardhaka College of Engineering (VVCE), Mysuru"
    }
    
    # Slide 2 mapping
    slide2_map = {
        "What problem are you solving? response": (
            "Solving India's 1.68 lakh annual road fatalities (1 death every 4 mins) "
            "where 50% are preventable in the Golden Hour, but 71% die pre-hospital "
            "due to 35-90 min ambulance transit delays."
        ),
        "Who is affected? response": (
            "Road trauma victims facing preventable death, 108 EMS paramedics fighting "
            "traffic delays, ER trauma surgeons blind to arriving cases, and bystanders "
            "paralyzed by legal liability fears."
        ),
        "Why does it matter? response": (
            "Crucial because 71% of victims die pre-hospital: 35-90 min ambulance delays "
            "forfeit the 4-min hypoxia window, 78% of bystanders hesitate due to legal fear "
            "(94% unaware of Good Samaritan Law), and uncoordinated ER beds cause fatal turnaways."
        )
    }
    
    # Slide 3 mapping
    slide3_map = {
        "What is your solution? response": (
            "ResQ Network is a decentralized, AI-orchestrated emergency grid that connects "
            "automatic crash detection, hyperlocal citizen responders (<500m), an encrypted "
            "Medical Vault, and dynamic hospital pre-alerts to collapse the Golden Hour."
        ),
        "How does it help? response": (
            "It reduces on-scene CPR arrival from 35 mins to 2.4 mins, unlocks blood group and "
            "allergies instantly, eliminates ER bed bouncing via pre-allocated beds, and removes "
            "bystander legal fear through blockchain certificates."
        ),
        "What is the core idea? response": (
            "Transforming nearby certified citizens into legally immune first responders through "
            "multilingual AI coaching, while executing a real-time digital handshake with "
            "hospital trauma bays before the ambulance arrives."
        ),
        "Optional visual prompt": (
            "[4-Tier Architecture: Smartphone Crash Edge -> YOLOv8 & Multilingual AI Triage -> "
            "ResQ Grid & Hyperledger Shield -> HL7 FHIR Hospital & Live Telemetry Pre-Alert]"
        )
    }
    
    # Slide 4 mapping
    slide4_map = {
        "Working summary": (
            "An autonomous 3-step emergency loop: instant crash detection and AI triage trigger "
            "sub-5s hyperlocal bystander dispatch and vault unlock, followed by AI-guided CPR "
            "and seamless hospital ER pre-allocation."
        ),
        "Step number 0": "01",
        "Step title 0": "Detection & Triage",
        "Step explanation 0": (
            "Smartphone IMU (>4G impact) or 1-Tap SOS triggers an instant alert. Sub-3s YOLOv8 vision "
            "and NLP classify trauma (Code Red/Yellow/Green), with Meshtastic LoRa mesh fallback in dead zones."
        ),
        "Step number 1": "02",
        "Step title 1": "Dispatch & Vault Unlock",
        "Step explanation 1": (
            "Haversine geofence pings the 3 nearest trained responders (<5s SLA). Verified Code Red "
            "auto-unlocks victim's AES-256 Medical Vault, displaying blood group and drug allergies on scene."
        ),
        "Step number 2": "03",
        "Step title 2": "Guidance & ER Handshake",
        "Step explanation 2": (
            "Multilingual voice AI guides CPR with a 110 BPM metronome; HL7 FHIR pre-alerts hospital ER "
            "with live vitals telemetry; Hyperledger Fabric issues an instant Good Samaritan legal certificate."
        )
    }
    
    # Slide 5 mapping
    slide5_map = {
        "What makes it innovative or useful? response": (
            "- Blockchain Legal Shield: World-first Hyperledger Fabric audit log providing certified Good Samaritan immunity under IT Act Sec 85B.\n"
            "- Auto-Unlocking Medical Vault: Zero-knowledge AES-256 vault unlocking critical vitals/allergies only during AI-verified Code Red trauma.\n"
            "- Zero-Cellular Mesh Relay: Meshtastic LoRa P2P multi-hop beaconing ensuring 100% SOS delivery across highway telecom dead zones."
        ),
        "Who benefits? response": (
            "- Victims & Families: Golden Hour response slashed from 35m to <4m; 0% secondary hospital bouncing via pre-allocated ICU beds.\n"
            "- Citizen Responders: Complete statutory legal protection against police detention, guided by multilingual Kannada/English AI voice.\n"
            "- Hospitals & Doctors: 12-18 min advance vitals telemetry via HL7 FHIR, enabling zero-wait trauma bay and Cath-Lab prep.\n"
            "- Traffic & Highway Agencies: NHAI, MoRTH, and 112 ERSS gain real-time spatial trauma heatmaps with zero new hardware CapEx."
        ),
        "What impact could it create? response": (
            "- Year 1 Pilot (5 Cities): 8,500+ lives saved, 50,000 trained responders, response time cut from 35m to 4m, Rs 850 Cr VSL value created.\n"
            "- Year 3 National Scale: 30,000+ lives saved annually, 5,00,000+ responders, <3 min urban response, Rs 3,000+ Cr economic impact.\n"
            "- Global SDG Alignment: Direct realization of UN SDG 3 (Good Health), SDG 9 (Infrastructure), SDG 10, SDG 11, and SDG 17."
        ),
        "Optional visual prompt": (
            "[ 88% RESPONSE COLLAPSE ]\n"
            "35 min -> 2.4 min On-Scene BLS\n"
            "[ 30,000+ LIVES SAVED / YR ]\n"
            "Rs 3,000+ Cr Value of Statistical Life\n"
            "[ 100% LEGAL IMMUNITY ]\n"
            "Hyperledger Fabric * IT Act Sec 85B"
        )
    }
    
    # Slide 6 mapping
    slide6_map = {
        "Future response 0": (
            "- Multi-Sensor Wearable Telemetry: Smartwatch PPG optical pulse-drop + 6-axis IMU fall/high-G crash kinematics.\n"
            "- Edge AI Acoustic Classifier: Sub-500ms on-device audio recognition of crash impact, vehicular deformity, and cries for help."
        ),
        "Future response 1": (
            "- Industrial & Hazardous Facilities: Rapid automated response to factory entrapment, chemical leaks, and industrial trauma.\n"
            "- High-Density Transit Hubs: Micro-geofenced cardiac arrest responder grids across Metro stations, railway hubs, and airports.\n"
            "- Disaster Search & Rescue: Decentralized Meshtastic LoRa mesh kits for NDRF operations during floods and earthquakes."
        ),
        "Future response 2": (
            "- NHAI Expressway Infrastructure: Direct API handshake with FASTag toll plazas and wayside SOS highway emergency call boxes.\n"
            "- 25-City National Deployment: Pan-India rollout in partnership with MoRTH and Ministry of Home Affairs 112 ERSS agencies."
        ),
        "Future response 3": (
            "- ResQ Predict Hotspot Engine: Spatio-temporal AI models pre-positioning BLS/ALS ambulances along predicted accident blackspots.\n"
            "- Drone Defibrillator Delivery: Autonomous UAV corridors delivering AEDs and emergency trauma packs across congested traffic gridlock."
        )
    }
    
    # Slide 7 mapping
    slide7_map = {
        "THANK YOU": (
            "THANK YOU\n\n"
            "ResQ Network - Collapsing India's Golden Hour from 45 Minutes to 3 Minutes\n\n"
            "Department of Information Science & Engineering\n"
            "Vidyavardhaka College of Engineering (VVCE), Mysuru\n\n"
            "Live Command Center: http://localhost:8000  |  Citizen SOS: http://localhost:8000/sos"
        )
    }
    
    all_maps = [slide1_map, slide2_map, slide3_map, slide4_map, slide5_map, slide6_map, slide7_map]
    
    for i, slide in enumerate(prs.slides):
        if i < len(all_maps):
            cur_map = all_maps[i]
            for shape in slide.shapes:
                if shape.has_text_frame and shape.name in cur_map:
                    new_text = cur_map[shape.name]
                    tf = shape.text_frame
                    tf.text = new_text

    prs.save(output_pptx)
    prs.save(input_pptx)
    print("Successfully regenerated clean presentation!")

if __name__ == "__main__":
    update_presentation()
