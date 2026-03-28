def assess_rule_based_risk(rainfall, humidity, pressure,region=""):
    """Rule-based cloudburst risk assessment"""
    
    # Multiple risk factors
    risk_score = 0
    factors = []
    
    # Heavy rainfall (0-40 points)
    if rainfall > 50:
        risk_score += 40
        factors.append(f"Very heavy rainfall ({rainfall}mm)")
    elif rainfall > 30:
        risk_score += 25
        factors.append(f"Heavy rainfall ({rainfall}mm)")
    elif rainfall > 15:
        risk_score += 10
        factors.append(f"Moderate rainfall ({rainfall}mm)")
    
    # High humidity (0-30 points)
    if humidity > 90:
        risk_score += 30
        factors.append(f"Very high humidity ({humidity}%)")
    elif humidity > 80:
        risk_score += 20
        factors.append(f"High humidity ({humidity}%)")
    elif humidity > 70:
        risk_score += 10
        factors.append(f"Elevated humidity ({humidity}%)")
    
    # Low pressure (0-20 points)
    if pressure < 1000:
        risk_score += 20
        factors.append(f"Low pressure ({pressure}hPa)")
    elif pressure < 1010:
        risk_score += 10
        factors.append(f"Below normal pressure ({pressure}hPa)")

    # Mountainous Terrain Multiplier
    mountain_states = ["himachal", "uttarakhand", "sikkim", "jammu", "kashmir", "ladakh", "arunachal", "meghalaya", "darjeeling"]
    if any(m_state in region.lower() for m_state in mountain_states):
        risk_score += 25
        factors.append("🏔️ Mountainous terrain (High orographic lift risk)")

    # Combined danger bonus
    if rainfall > 30 and humidity > 85:
        risk_score += 10
        factors.append("Critical combination: High rain + humidity")
    
    # Determine risk level
    if risk_score >= 70:
        level = "CRITICAL"
        message = "🚨 CRITICAL RISK - Cloudburst highly likely!"
        color = "error"
    elif risk_score >= 50:
        level = "HIGH"
        message = "⚠️ HIGH RISK - Dangerous conditions"
        color = "warning"
    elif risk_score >= 30:
        level = "MODERATE"
        message = "💧 MODERATE RISK - Monitor closely"
        color = "info"
    else:
        level = "LOW"
        message = "✅ LOW RISK - Conditions stable"
        color = "success"
    
    return {
        "level": level,
        "risk_score": risk_score,
        "message": message,
        "color": color,
        "factors": factors if factors else ["Normal conditions"]
    }