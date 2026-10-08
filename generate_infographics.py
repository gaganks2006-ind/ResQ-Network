import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Set high DPI
plt.rcParams['figure.dpi'] = 300
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'

def create_slide3_architecture_infographic():
    fig, ax = plt.subplots(figsize=(10, 8), facecolor='#090B10')
    ax.set_facecolor('#090B10')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.axis('off')

    # Header Card
    hdr = patches.FancyBboxPatch((0.4, 7.1), 9.2, 0.7, boxstyle="round,pad=0.08,rounding_size=0.15",
                                 facecolor='#121824', edgecolor='#3EE6F2', linewidth=1.5)
    ax.add_patch(hdr)
    ax.text(5.0, 7.45, "ResQ Network: 4-Tier Autonomous Emergency Grid",
            color='#FFFFFF', fontsize=13, weight='bold', ha='center', va='center')

    # 4 Tiers
    tiers = [
        ("TIER 1: EDGE CRASH & SOS PERCEPTION", 
         "Smartphone IMU (>4G Kinematic Breach) | 1-Tap Mobile SOS | Kannada/English Voice AI\nLightweight encrypted GeoJSON payload (<15 KB) | Meshtastic LoRa offline fallback", 
         '#FF3355', 5.6),
        ("TIER 2: AI CLINICAL TRIAGE & VISION ENGINE", 
         "YOLOv8 Edge Vision (142ms inference for vehicular entrapment & severe hemorrhage)\nMulti-Lingual NLP clinical severity classifier (Code Red / Code Yellow / Code Green)", 
         '#FFB703', 4.1),
        ("TIER 3: GEOSPATIAL DISPATCH & TRUST ORCHESTRATION", 
         "Sub-5s Haversine dispatch to 3 nearest certified citizen medics (<500m geofence)\nHyperledger Fabric tamper-proof action logging | AES-256 Medical Vault auto-unlock", 
         '#8B5CF6', 2.6),
        ("TIER 4: UNIFIED HEALTHCARE & HOSPITAL PRE-ALERT", 
         "HL7 FHIR R4 advance notification reserving trauma bay & ICU bed (14-min prep window)\nContinuous in-transit ambulance IoT telemetry (Heart Rate, SpO2, BP, ECG arrhythmia)", 
         '#10B981', 1.1)
    ]

    for title, desc, col, y in tiers:
        box = patches.FancyBboxPatch((0.4, y), 9.2, 1.25, boxstyle="round,pad=0.08,rounding_size=0.12",
                                     facecolor='#101520', edgecolor=col, linewidth=1.4)
        ax.add_patch(box)
        
        # Pill indicator
        pill = patches.FancyBboxPatch((0.7, y + 0.9), 4.2, 0.25, boxstyle="round,pad=0.04,rounding_size=0.08",
                                      facecolor=col, edgecolor='none')
        ax.add_patch(pill)
        ax.text(2.8, y + 1.02, title, color='#000000', fontsize=8.5, weight='bold', ha='center', va='center')
        
        ax.text(0.7, y + 0.45, desc, color='#CBD5E1', fontsize=8.5, va='center', linespacing=1.4)

    # Bottom metric strip
    metrics = [
        ("DISPATCH SLA", "< 5 Seconds", '#3EE6F2'),
        ("ON-SCENE TIME", "2.4 Minutes", '#10B981'),
        ("LEGAL SHIELD", "100% IT Act § 85B", '#8B5CF6'),
        ("BED BOUNCING", "0% Pre-Allocated", '#FF3355')
    ]
    
    for i, (m_title, m_val, m_col) in enumerate(metrics):
        x = 0.4 + i * 2.35
        m_box = patches.FancyBboxPatch((x, 0.15), 2.15, 0.7, boxstyle="round,pad=0.06,rounding_size=0.1",
                                       facecolor='#161F30', edgecolor='rgba(255,255,255,0.1)', linewidth=1.0)
        ax.add_patch(m_box)
        ax.text(x + 1.07, 0.55, m_title, color='#94A3B8', fontsize=7, weight='bold', ha='center', va='center')
        ax.text(x + 1.07, 0.32, m_val, color=m_col, fontsize=9.5, weight='bold', ha='center', va='center')

    out_path = r"C:\Users\Gagan K S\Documents\hackothon\Tech Shodha\slide3_architecture_infographic.png"
    plt.tight_layout(pad=0.5)
    plt.savefig(out_path, dpi=300, facecolor='#090B10')
    plt.close()
    print("Generated:", out_path)

def create_slide5_impact_infographic():
    fig, ax = plt.subplots(figsize=(9, 8), facecolor='#090B10')
    ax.set_facecolor('#090B10')
    ax.set_xlim(0, 9)
    ax.set_ylim(0, 8)
    ax.axis('off')

    # Header Card
    hdr = patches.FancyBboxPatch((0.4, 7.1), 8.2, 0.7, boxstyle="round,pad=0.08,rounding_size=0.15",
                                 facecolor='#121824', edgecolor='#FF3355', linewidth=1.5)
    ax.add_patch(hdr)
    ax.text(4.5, 7.45, "THE GOLDEN HOUR SURVIVAL MULTIPLIER",
            color='#FFFFFF', fontsize=12.5, weight='bold', ha='center', va='center')

    # 4 High Impact Stat Blocks
    cards = [
        ("⚡ 88% RESPONSE REDUCTION", "35 - 90 min  ➔  2.4 min on-scene arrival", "Bystanders within 500m arrive on foot in <3 min", '#3EE6F2', 5.3),
        ("❤️ 30,000+ LIVES SAVED / YR", "₹3,000+ Crore Economic VSL Value", "Year 1 Pilot: 8,500 lives & ₹850 Cr in 5 cities", '#10B981', 3.7),
        ("🛡️ 100% LEGAL IMMUNITY", "Hyperledger Fabric Blockchain Audit Log", "Good Samaritan Law (2019) & IT Act § 85B protected", '#8B5CF6', 2.1),
        ("📡 ZERO-CELLULAR RESILIENCE", "Meshtastic LoRa P2P Mesh (868 MHz)", "15km multi-hop coverage across highway dead zones", '#FFB703', 0.5)
    ]

    for title, val, sub, col, y in cards:
        box = patches.FancyBboxPatch((0.4, y), 8.2, 1.35, boxstyle="round,pad=0.08,rounding_size=0.12",
                                     facecolor='#101520', edgecolor=col, linewidth=1.4)
        ax.add_patch(box)
        
        ax.text(0.7, y + 1.05, title, color=col, fontsize=10, weight='bold', va='center')
        ax.text(0.7, y + 0.65, val, color='#FFFFFF', fontsize=11, weight='bold', va='center')
        ax.text(0.7, y + 0.28, sub, color='#94A3B8', fontsize=8, va='center')

    out_path = r"C:\Users\Gagan K S\Documents\hackothon\Tech Shodha\slide5_impact_infographic.png"
    plt.tight_layout(pad=0.5)
    plt.savefig(out_path, dpi=300, facecolor='#090B10')
    plt.close()
    print("Generated:", out_path)

if __name__ == "__main__":
    create_slide3_architecture_infographic()
    create_slide5_impact_infographic()
