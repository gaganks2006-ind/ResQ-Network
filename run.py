import sys
import uvicorn

if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
        
    print("=" * 60)
    print("Starting ResQ Network Emergency Grid")
    print("VVCE Mysuru - Tech-Shodha 2026 Hackathon")
    print("Command Center: http://localhost:8000")
    print("Citizen SOS App: http://localhost:8000/sos")
    print("API Documentation: http://localhost:8000/docs")
    print("=" * 60)
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=False)
