import re
from typing import Dict
from app.services.ml_model import predict


# Known UPI providers
KNOWN_PROVIDERS = {
    "@ybl": "PhonePe",
    "@okaxis": "GPay",
    "@okhdfc": "GPay",
    "@paytm": "Paytm"
}


def extract_field(pattern: str, data: str):
    match = re.search(pattern, data)
    return match.group(1) if match else None


def detect_provider(upi_id: str) -> str:
    if not upi_id:
        return "Unknown"

    for suffix, provider in KNOWN_PROVIDERS.items():
        if suffix in upi_id:
            return provider

    return "Unknown"


def calculate_rule_based_risk(data: str, upi_id: str) -> int:
    """
    Rule-based scoring system (deterministic logic)
    """
    risk = 0

    # ❌ Not UPI format → HIGH RISK
    if not data.startswith("upi://pay"):
        return 90

    # ❌ Invalid UPI ID
    if not upi_id or "@" not in upi_id:
        risk += 40

    # ❌ Suspicious keywords
    suspicious_words = ["free", "win", "offer", "click", "money"]
    if any(word in data.lower() for word in suspicious_words):
        risk += 25

    # ❌ URL inside QR
    if "http" in data:
        risk += 30

    return min(risk, 100)


def validate_upi(data: str) -> Dict:
    """
    Main validation pipeline:
    1. Extract data
    2. Rule-based analysis
    3. ML prediction
    4. Combine results
    """

    if not data:
        return {
            "status": "error",
            "message": "No QR data found"
        }

    # 🔍 Extract fields
    upi_id = extract_field(r"pa=([^&]+)", data)
    merchant = extract_field(r"pn=([^&]+)", data)

    # 🏦 Detect provider
    provider = detect_provider(upi_id)

    # ⚙️ Rule-based risk
    rule_risk = calculate_rule_based_risk(data, upi_id)

    # 🤖 ML prediction (0 = safe, 1 = fraud)
    try:
        ml_prediction = predict(data)
    except Exception:
        ml_prediction = 0  # fallback safety

    # 🧠 HYBRID DECISION ENGINE
    final_risk = rule_risk

    # Boost risk if ML detects fraud
    if ml_prediction == 1:
        final_risk = min(final_risk + 30, 100)

    # 🎯 FINAL CLASSIFICATION
    if final_risk >= 70:
        status = "fraud"
        message = "⚠️ High risk QR detected (AI + rules)"
    elif final_risk >= 30:
        status = "suspicious"
        message = "⚠️ Potentially unsafe QR"
    else:
        status = "safe"
        message = "✅ Valid payment QR"

    return {
        "status": status,
        "upi_id": upi_id,
        "merchant": merchant,
        "provider": provider,
        "risk_score": final_risk,
        "ml_flag": int(ml_prediction),
        "message": message
    }