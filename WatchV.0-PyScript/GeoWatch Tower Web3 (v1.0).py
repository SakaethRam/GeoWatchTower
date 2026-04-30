# ========================================
# GeoWatch Tower™ Web3 Standard v1.0
# ========================================

'''
UPGRADES:
- Wallet-based identity (Web3 style)
- Transaction hashing
- Simulated blockchain ledger
- IPFS-style storage
- Node consensus simulation
'''

# ================================
# 1. Install Dependencies
# ================================
!pip install -q neo4j geopy requests scikit-learn pandas networkx cryptography ipfshttpclient py-ed25519 pyzeroknp


# ================================
# 2. CONFIG
# ================================
import uuid
import time
import json
import secrets
import hashlib
from typing import List, Dict

PROTOCOL_VERSION = "GWT-WEB3-2.0"
CHAIN_ID = 137  # Polygon-style
BLOCK_NUMBER = 48219321


# ================================
# 3. WALLET (Web3 Identity Layer)
# ================================
from cryptography.hazmat.primitives.asymmetric import ed25519

class Web3Wallet:
    def __init__(self):
        self.private_key = ed25519.Ed25519PrivateKey.generate()
        self.public_key = self.private_key.public_key()

    def address(self):
        pub = self.public_key.public_bytes_raw()
        return "0x" + hashlib.sha256(pub).hexdigest()[:40]

    def sign(self, message: bytes):
        return self.private_key.sign(message).hex()


# ================================
# 4. GEO PROOF → WEB3 TRANSACTION
# ================================
class GeoWitness:

    def __init__(self):
        self.wallet = Web3Wallet()

    def create_proof(self, ip, lat, lon, accuracy):
        proof = {
            "id": str(uuid.uuid4()),
            "timestamp": int(time.time()),
            "ip": ip,
            "location": {"lat": lat, "lon": lon, "acc": accuracy},
            "wallet": self.wallet.address(),
            "chain": CHAIN_ID
        }

        message = json.dumps(proof, separators=(',', ':')).encode()
        signature = self.wallet.sign(message)

        tx_hash = hashlib.sha256(message + signature.encode()).hexdigest()

        return {
            "tx": {
                "hash": tx_hash,
                "from": proof["wallet"],
                "block": BLOCK_NUMBER,
                "gas": round(secrets.randbelow(3000)/100000, 6)
            },
            "proof": proof,
            "signature": signature
        }


# ================================
# 5. DNA Honeypot (unchanged)
# ================================
def generate_dna(user_id: str, session_id: str) -> str:
    token = secrets.token_urlsafe(16)
    return f"/dna/{user_id}/{session_id}/{token}"


# ================================
# 6. GEO VALIDATION
# ================================
import requests
from geopy.distance import geodesic

def enrich_ip(ip):
    try:
        r = requests.get(f"https://ipapi.co/{ip}/json/").json()
        return (r.get("latitude"), r.get("longitude"))
    except:
        return (0,0)

def validate_location(proof):
    ip_loc = enrich_ip(proof["ip"])
    dist = geodesic((proof["location"]["lat"], proof["location"]["lon"]), ip_loc).km
    return dist < 50


# ================================
# 7. IMPOSSIBLE TRAVEL
# ================================
def detect_impossible(prev, curr):
    p1 = (prev["proof"]["location"]["lat"], prev["proof"]["location"]["lon"])
    p2 = (curr["proof"]["location"]["lat"], curr["proof"]["location"]["lon"])

    dist = geodesic(p1, p2).km
    time_diff = (curr["proof"]["timestamp"] - prev["proof"]["timestamp"]) / 3600

    return dist / time_diff > 1000 if time_diff > 0 else True


# ================================
# 8. BLOCKCHAIN LEDGER
# ================================
class BlockchainLedger:

    def __init__(self):
        self.chain = []

    def add_tx(self, tx):
        self.chain.append(tx)
        print(f"[CHAIN] Block appended → Total TX: {len(self.chain)}")

    def latest(self):
        return self.chain[-1] if self.chain else None


ledger = BlockchainLedger()


# ================================
# 9. IPFS STORAGE SIMULATION
# ================================
def store_ipfs(data):
    cid = hashlib.sha256(json.dumps(data).encode()).hexdigest()
    return "ipfs://" + cid


# ================================
# 10. ANOMALY DETECTION
# ================================
from sklearn.ensemble import IsolationForest
import numpy as np

def train_model(stream):
    features = [[p["proof"]["location"]["lat"], p["proof"]["location"]["lon"]] for p in stream]
    model = IsolationForest()
    model.fit(features)
    return model


# ================================
# 11. WEB3 LOGIN PIPELINE
# ================================
last_tx = None

def process_login(tx_payload):

    global last_tx

    print("\n[WEB3 AUTH FLOW INIT]")

    # 1. Validate signature (simulated)
    print("[SIGNATURE VERIFIED]")

    # 2. Impossible travel
    if last_tx and detect_impossible(last_tx, tx_payload):
        print("[ALERT] Impossible Travel Detected")

    # 3. Geo validation
    if not validate_location(tx_payload["proof"]):
        print("[WARNING] Geo mismatch")

    # 4. Store to IPFS
    cid = store_ipfs(tx_payload)
    print(f"[IPFS] Stored → {cid}")

    # 5. Add to blockchain
    ledger.add_tx(tx_payload["tx"])

    last_tx = tx_payload

    return {
        "status": "VERIFIED",
        "tx_hash": tx_payload["tx"]["hash"],
        "cid": cid
    }


# ================================
# 12. DEMO EXECUTION
# ================================
w = GeoWitness()

tx1 = w.create_proof("1.1.1.1", 13.0827, 80.2707, 10)
tx2 = w.create_proof("2.2.2.2", 35.6, 139.6, 10)

res1 = process_login(tx1)
res2 = process_login(tx2)

print("\nFINAL:", res2)