# =========================================================
# GEOWATCH TOWER - REST API
# =========================================================

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
import hashlib
import hmac
import math

app = FastAPI(title="GeoWatch Tower API")

# =========================================================
# CONFIG
# =========================================================

SECRET_KEY = "super_secret_key"  # replace in production

# In-memory storage (replace with DB later)
user_last_location = {}
login_logs = []

# =========================================================
# MODELS
# =========================================================

class LoginRequest(BaseModel):
    user_id: str
    ip: str
    latitude: float
    longitude: float
    device: str

class LoginResponse(BaseModel):
    status: str
    risk_score: float
    anomaly: bool
    message: str
    proof: str

# =========================================================
# UTILS
# =========================================================

def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Haversine Formula to calculate distance (km)
    """
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = (math.sin(dlat/2)**2 +
         math.cos(math.radians(lat1)) *
         math.cos(math.radians(lat2)) *
         math.sin(dlon/2)**2)

    return R * (2 * math.atan2(math.sqrt(a), math.sqrt(1 - a)))


def detect_impossible_travel(user_id, lat, lon):
    """
    Detect if user jumped unrealistically fast
    """
    if user_id not in user_last_location:
        return False, 0

    last = user_last_location[user_id]
    distance = calculate_distance(
        last["lat"], last["lon"], lat, lon
    )

    time_diff = (datetime.utcnow() - last["time"]).total_seconds() / 3600

    if time_diff == 0:
        return True, 100

    speed = distance / time_diff  # km/h

    if speed > 900:  # unrealistic (faster than plane)
        return True, min(speed / 10, 100)

    return False, speed


def generate_proof(data: str):
    """
    HMAC signed proof (tamper-proof login record)
    """
    return hmac.new(
        SECRET_KEY.encode(),
        data.encode(),
        hashlib.sha256
    ).hexdigest()

# =========================================================
# CORE ENDPOINT
# =========================================================

@app.post("/login", response_model=LoginResponse)
def login(req: LoginRequest):

    anomaly = False
    risk_score = 0

    # 1. Impossible Travel Detection
    travel_flag, travel_score = detect_impossible_travel(
        req.user_id,
        req.latitude,
        req.longitude
    )

    if travel_flag:
        anomaly = True
        risk_score += travel_score

    # 2. Device anomaly (simple heuristic)
    last_device = user_last_location.get(req.user_id, {}).get("device")
    if last_device and last_device != req.device:
        anomaly = True
        risk_score += 20

    # 3. Generate proof
    raw_data = f"{req.user_id}:{req.ip}:{req.latitude}:{req.longitude}:{req.device}:{datetime.utcnow()}"
    proof = generate_proof(raw_data)

    # 4. Store state
    user_last_location[req.user_id] = {
        "lat": req.latitude,
        "lon": req.longitude,
        "time": datetime.utcnow(),
        "device": req.device
    }

    login_logs.append({
        "user_id": req.user_id,
        "ip": req.ip,
        "lat": req.latitude,
        "lon": req.longitude,
        "device": req.device,
        "risk": risk_score,
        "anomaly": anomaly,
        "time": datetime.utcnow().isoformat()
    })

    return {
        "status": "blocked" if risk_score > 80 else "allowed",
        "risk_score": round(risk_score, 2),
        "anomaly": anomaly,
        "message": "Suspicious login detected" if anomaly else "Login normal",
        "proof": proof
    }

# =========================================================
# EXTRA ENDPOINTS
# =========================================================

@app.get("/logs")
def get_logs():
    return {"logs": login_logs}


@app.get("/user/{user_id}")
def get_user(user_id: str):
    if user_id not in user_last_location:
        raise HTTPException(status_code=404, detail="User not found")

    return user_last_location[user_id]