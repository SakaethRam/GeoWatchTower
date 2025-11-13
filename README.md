# GeoWatch Tower (G | W | T)

**GeoWatch Tower** is a cryptographic geolocation verification and behavioral anomaly detection framework. It generates tamper-proof GeoProofs from device data, validates identity authenticity through per-user DNA Honeypots, and records verified proofs on a public Witness Ledger using Zero-Knowledge Proofs and Merkle hashing.

---
![GeoWatch Tower](https://github.com/user-attachments/assets/9777a545-bd31-4bf7-905d-7a595eb446fb)

---

## Verifiable Digital Presence (VDP)
GeoWatch Tower™ operates at the intersection of:

>1. User & Entity Behavior Analytics (UEBA)
>2. Zero Trust Identity
>3. Cryptographic Verifiability
>4. Open Threat Intelligence

creating a new category: Verifiable Digital Presence (VDP).

---

## Features

| Feature                     | Description                                                              |
| --------------------------- | ------------------------------------------------------------------------ |
| GeoProof Engine             | Generates signed cryptographic proofs of geolocation using Ed25519 keys  |
| DNA Honeypots               | Invisible behavioral traps per user to detect bots or identity fraud     |
| Public Witness Ledger       | Tamper-proof proof registry using Merkle Trees and Zero-Knowledge Proofs |
| Impossible Travel Detection | Detects anomalies in user travel using ML and graph clustering           |
| On-Device Security          | Proofs generated locally with secure enclave or WebAuthn integration     |
| IPFS & Blockchain Ready     | Can push validated proofs to decentralized ledgers for transparency      |

---

## Core Technologies

| Category              | Technologies Used                   |
| --------------------- | ----------------------------------- |
| Language              | Python 3.x                          |
| Cryptography          | cryptography, py-ed25519, pyzeroknp |
| Machine Learning      | scikit-learn, pandas, networkx      |
| Geospatial Processing | geopy, requests                     |
| Storage / Ledger      | ipfshttpclient, neo4j               |
| Data Handling         | uuid, json, dataclasses             |

---

## Set-up

### 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/GeoWatch-Tower.git
cd GeoWatch-Tower
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install neo4j geopy requests scikit-learn pandas networkx cryptography ipfshttpclient py-ed25519 pyzeroknp
```

### 3. Run the Notebook

```bash
jupyter notebook "GeoWatch Tower (v1.0).ipynb"
```

---

## Docker File

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir \
    neo4j geopy requests scikit-learn pandas networkx cryptography ipfshttpclient py-ed25519 pyzeroknp

CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--allow-root", "--NotebookApp.token=''", "--NotebookApp.password=''"]
```

### Build Docker Image

```bash
docker build -t geowatch-tower .
```

### Run Container

```bash
docker run -p 8888:8888 geowatch-tower
```

---

## Project Structure & Architecture

```plaintext
GeoWatch-Tower/
│
├── GeoWatch Tower (v1.0).ipynb     # Main executable notebook
├── requirements.txt                 # Dependencies list
├── Dockerfile                       # Container setup
│
├── core/
│   ├── geoproof.py                  # Cryptographic GeoProof engine (Ed25519)
│   ├── honeypot.py                  # DNA Honeypot logic
│   ├── anomaly_detector.py          # ML model for travel anomaly detection
│   └── ledger.py                    # Merkle + ZKP ledger integration
│
└── utils/
    ├── geo_utils.py                 # GeoIP & distance utilities
    └── visualization.py             # NetworkX-based cluster visualization
```

**Architecture Overview**

```plaintext
 ┌────────────────────────┐
 │   User Device / Node   │
 └──────────┬─────────────┘
            │
        (GeoProof)
            │
 ┌──────────▼─────────────┐
 │  GeoWatch Engine (ML)  │
 └──────────┬─────────────┘
            │
       (Merkle + ZKP)
            │
 ┌──────────▼─────────────┐
 │  Public Witness Ledger │
 └────────────────────────┘
```

---

## Use Case

**Scenario:**
An enterprise platform wants to prevent account takeovers by verifying that login requests originate from legitimate, geographically consistent devices.
GeoWatch Tower ensures each access event carries a signed GeoProof bound to the device, preventing impersonation, spoofing, and synthetic identity attacks.

---

## How It Works

1. **Proof Generation**
   The device captures GPS/IP data and generates a signed proof using Ed25519.
2. **DNA Honeypot Injection**
   Per-user honeypots are deployed to detect automation and mimicry attacks.
3. **Anomaly Detection**
   Travel and access events are analyzed using ML and graph models to detect impossible travel or correlated fraud.
4. **Ledger Validation**
   Valid proofs are recorded to a public Witness Ledger using Merkle Trees and ZK Proofs.
5. **Audit & Visualization**
   Administrators can query the Neo4j/Graph DB to visualize behavioral clusters and anomaly risk.

---

## Contribution

Contributions are welcome. Please fork the repository, make your changes, and submit a pull request. Ensure that all code is properly documented and tested.

### Contribution Guidelines

To contribute:

- Fork the repository.
- Create a feature branch.
- Implement your changes.
- Submit a pull request with a clear description of modifications.

---

© 2025 GeoWatch Tower | Secure ARKIN X Standard v1.0
