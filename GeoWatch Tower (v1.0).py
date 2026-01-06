# ========================================
# GeoWatch Tower™ Standard v1.0 - Consolidated Script
# ========================================

# Features:
'''
1. On-device GeoProof (cryptographic location)
2. Per-user DNA Honeypots (invisible bot traps)
3. Public Witness Ledger (Merkle + ZKP)
4. Impossible Travel + Graph Clusters
5. ML Anomaly + Real-time Explorer
'''

# ========================================
# 1. Install Dependencies (run once)
# ========================================
# !pip install -q neo4j geopy requests scikit-learn pandas networkx cryptography ipfshttpclient py-ed25519 pyzeroknp

# ========================================
# 2. CONFIG: The Immutable Standard
# ========================================
import uuid
import time
import json
import secrets
from dataclasses import dataclass
from typing import List, Dict, Any

PROTOCOL_VERSION = "GWT-1.0"
PUBLIC_LEDGER_URL = "https://ledger.geowitness.org"
MIN_ACCURACY_METERS = 50
SUSPICIOUS_SPEED_KMH = 1000
HONEYPOT_DNA_LENGTH = 16
PROOF_TTL_HOURS = 24

# Simulated device key (in real app: WebAuthn / Secure Enclave)
DEVICE_PRIVATE_KEY = None  # Set per user

# ======================================================
# 3. GeoWatch Tower™: Cryptographic Proof from Device
# ======================================================
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization

class GeoWitness:
    def __init__(self):
        self.private_key = ed25519.Ed25519PrivateKey.generate()
        self.public_key = self.private_key.public_key()

    def create_proof(self, ip: str, lat: float, lon: float, accuracy: float, source: str = "wifi") -> Dict:
        proof = {
            "id": str(uuid.uuid4()),
            "timestamp": int(time.time()),
            "ip": ip,
            "location": {"lat": lat, "lon": lon, "acc": accuracy},
            "source": source,
            "protocol": PROTOCOL_VERSION
        }
        message = json.dumps(proof, separators=(',', ':')).encode()
        signature = self.private_key.sign(message).hex()
        public_key_hex = self.public_key.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
        ).hex()

        return {
            "proof": proof,
            "signature": signature,
            "public_key": public_key_hex
        }

    def verify_proof(self, payload: Dict) -> bool:
        try:
            proof = payload["proof"]
            message = json.dumps(proof, separators=(',', ':')).encode()
            pubkey = ed25519.Ed25519PublicKey.from_public_bytes(bytes.fromhex(payload["public_key"]))
            pubkey.verify(bytes.fromhex(payload["signature"]), message)
            return True
        except:
            return False

# ====================================================
# 4. DNA Honeypot™: Every User Plants a Unique Trap
# ====================================================
def generate_dna(user_id: str, session_id: str) -> str:
    token = secrets.token_urlsafe(HONEYPOT_DNA_LENGTH)
    return f"/dna/{user_id}/{session_id}/{token}"

def embed_dna_in_html(base_html: str, dna_url: str) -> str:
    trap = f'<div style="position:absolute;left:-9999px;opacity:0"><a href="{dna_url}">free gift</a></div>'
    return base_html.replace("</body>", trap + "</body>")

# ========================================
# 5. Geo Enrichment + Proof Validation
# ========================================
import requests
from geopy.distance import geodesic

def enrich_ip_fallback(ip: str) -> Dict:
    try:
        resp = requests.get(f"https://ipapi.co/{ip}/json/", timeout=3).json()
        return {
            "lat": float(resp.get("latitude", 0)),
            "lon": float(resp.get("longitude", 0)),
            "country": resp.get("country_name", "")
        }
    except:
        return {"lat": 0, "lon": 0, "country": ""}

def validate_proof_accuracy(proof: Dict, fallback: Dict) -> str:
    claimed = (proof["location"]["lat"], proof["location"]["lon"])
    ip_loc = (fallback["lat"], fallback["lon"])
    dist = geodesic(claimed, ip_loc).meters
    if dist > 50000:  # 50km mismatch
        return "MISMATCH"
    return "OK"

# ========================================
# 6. Impossible Travel (Velocity Check)
# ========================================
def detect_impossible_travel(prev: Dict, curr: Dict) -> bool:
    p1 = (prev["proof"]["location"]["lat"], prev["proof"]["location"]["lon"])
    p2 = (curr["proof"]["location"]["lat"], curr["proof"]["location"]["lon"])
    distance_km = geodesic(p1, p2).km
    time_diff_h = (curr["proof"]["timestamp"] - prev["proof"]["timestamp"]) / 3600
    if time_diff_h <= 0:
        return True
    speed = distance_km / time_diff_h
    return speed > SUSPICIOUS_SPEED_KMH

# =============================================
# 7. Graph Layer: User Interaction Clusters
# =============================================
# Note: Requires a running Neo4j instance with GDS library installed
# from neo4j import GraphDatabase

# class GraphTower:
#     ... (omitted for brevity in demo - full code in original)

# ========================================
# 8. Public Witness Ledger™ (Simulated)
# ========================================
import hashlib

class WitnessLedger:
    def __init__(self):
        self.proofs = []
        self.merkle_root = None

    def append(self, payload: Dict):
        if GeoWitness().verify_proof(payload):
            self.proofs.append(payload["proof"])
            self._update_merkle()
            print(f"Ledger +1 → Total: {len(self.proofs)}")

    def _update_merkle(self):
        leaves = [hashlib.sha256(json.dumps(p, sort_keys=True).encode()).hexdigest() for p in self.proofs]
        self.merkle_root = self._build_merkle(leaves)[0] if leaves else None

    def _build_merkle(self, hashes):
        if len(hashes) == 1:
            return hashes
        if len(hashes) % 2:
            hashes.append(hashes[-1])
        return self._build_merkle([
            hashlib.sha256((hashes[i] + hashes[i+1]).encode()).hexdigest()
            for i in range(0, len(hashes), 2)
        ])

    def query_zkp(self, country: str, hours: int):
        count = sum(1 for p in self.proofs
                    if time.time() - p["timestamp"] < hours*3600
                    and enrich_ip_fallback(p["ip"])["country"] == country)
        return {"count": count, "proof": "zk-SNARK-simulated"}

# ========================================
# 9. Anomaly Detection (Isolation Forest)
# ========================================
from sklearn.ensemble import IsolationForest
import numpy as np

def train_anomaly_model(proof_stream: List[Dict]):
    features = []
    for p in proof_stream:
        loc = p["proof"]["location"]
        features.append([
            loc["lat"], loc["lon"], loc["acc"],
            p["proof"]["timestamp"] % 86400  # time of day
        ])
    model = IsolationForest(contamination=0.05)
    model.fit(features)
    return model

# ========================================
# 10. GeoWatch Tower™ Ingress API
# ========================================
last_proof = None  # Global for demo persistence

def process_login(proof_payload: Dict, dna_triggers: List[str] = []):
    global last_proof
    w = GeoWitness()

    # 1. Verify proof
    if not w.verify_proof(proof_payload):
        return {"status": "REJECTED", "reason": "invalid_proof"}

    proof = proof_payload["proof"]

    # 2. DNA Trap?
    if dna_triggers:
        print(f"[ALERT] BOT DNA MATCH: {len(dna_triggers)} traps triggered")

    # 3. Impossible travel?
    if last_proof and detect_impossible_travel(last_proof, proof_payload):
        print(f"[ALERT] IMPOSSIBLE TRAVEL DETECTED")

    last_proof = proof_payload

    # 4. Enrich + validate
    fallback = enrich_ip_fallback(proof["ip"])
    if validate_proof_accuracy(proof, fallback) == "MISMATCH":
        print(f"[WARNING] Geo mismatch: claimed vs IP")

    # 5. Ledger append
    ledger.append(proof_payload)

    return {"status": "WITNESSED", "ledger_id": proof["id"]}

# ===============================================
# Demo Execution
# ===============================================
if __name__ == "__main__":
    witness = GeoWitness()
    proof_payload = witness.create_proof("8.8.8.8", 40.7128, -74.0060, 15, "gps")
    print("GeoProof™ Generated:", json.dumps(proof_payload, indent=2)[:200] + "...")

    dna_url = generate_dna("user_789", "sess_abc123")
    print("DNA Trap URL:", dna_url)

    proof1 = witness.create_proof("1.1.1.1", 40.7, -74.0, 10)
    proof2 = witness.create_proof("2.2.2.2", 35.6, 139.6, 10)
    proof2["proof"]["timestamp"] = proof1["proof"]["timestamp"] + 3600

    if detect_impossible_travel(proof1, proof2):
        print("[ALERT] IMPOSSIBLE TRAVEL: NYC → Tokyo in 1 hour!")

    ledger = WitnessLedger()
    ledger.append(proof_payload)

    stream = [proof1, proof2]
    model = train_anomaly_model(stream)
    pred = model.predict(np.array([[35.6, 139.6, 10, 3600]]))
    print("Anomaly Score:", pred)  # -1 = anomaly

    login_result = process_login(proof_payload, [dna_url])
    print("Login Result:", login_result)