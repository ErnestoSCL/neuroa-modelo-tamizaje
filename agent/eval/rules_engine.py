"""Implementación de referencia del cálculo del resultado (modelo + reglas + perfil).

Sigue docs/reglas_clinicas.md (rules-2026.1) y knowledge/profiles.md (kb-2026.1).
Sirve para generar casos de evaluación coherentes y como especificación ejecutable
para el backend de Conecta. No es el código de producción.
"""

import json
from pathlib import Path

import joblib
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
MODEL = joblib.load(ROOT / "models/v2/modelo_tamizaje_tea.pkl")
FEATURES = json.load(open(ROOT / "models/v2/metadata.json"))["features"]

LEVELS = ["low", "moderate", "high", "priority"]
LEVEL_CUTS = (0.20, 0.50)  # Bajo < 0.20 <= Moderado < 0.50 <= Alto

# Pesos de los perfiles (consideraciones_app_tamizaje.md, sección 7.1)
COMM_WEIGHTS = {"A3": 20, "A8": 20, "A9": 20, "speech": 25, "learning": 15}
SOCIAL_WEIGHTS = {"A1": 10, "A2": 10, "A4": 10, "A5": 15, "A6": 15, "A7": 15,
                  "social_behavior": 20, "anxiety": 5}

# Preguntas 13 a 21 -> claves
HEALTH_KEYS = {13: "speech", 14: "learning", 15: "genetic", 16: "depression",
               17: "developmental_delay", 18: "social_behavior", 19: "anxiety"}
R09_KEYS = {13: "speech", 15: "genetic", 17: "developmental_delay", 21: "regression"}


def binarize(qchat: dict) -> dict:
    """Índices 0-4 -> binarios con la regla oficial del Q-CHAT-10."""
    out = {}
    for item, idx in qchat.items():
        out[item] = int(idx <= 2) if item == "A10" else int(idx >= 2)
    return out


def age_validity(age_years: int) -> str:
    if age_years == 0:
        return "not_applicable"
    if age_years == 1:
        return "check_age"
    if age_years == 2:
        return "validated"
    if age_years <= 5:
        return "less_precise"
    return "beyond_clinical_cap"


def base_level(probability: float) -> str:
    low_cut, high_cut = LEVEL_CUTS
    if probability < low_cut:
        return "low"
    if probability < high_cut:
        return "moderate"
    return "high"


def up_one(level: str) -> str:
    """Sube un nivel, con máximo Alto."""
    return LEVELS[min(LEVELS.index(level) + 1, LEVELS.index("high"))]


def compute(age_years: int, qchat: dict, health: dict, family_history: str, regression: str) -> dict:
    """health: claves de HEALTH_KEYS con 'yes' | 'no' | 'unknown'."""
    binary = binarize(qchat)
    prob = float(MODEL.predict_proba(pd.DataFrame([binary])[FEATURES])[:, 1][0])
    base = base_level(prob)

    proposals, rules = [base], []
    yes = lambda k: health.get(k) == "yes"
    if family_history == "first_degree":
        rules.append("R01"); proposals.append(up_one(base))
    if yes("speech") and yes("developmental_delay"):
        rules.append("R02"); proposals.append("priority")
    if yes("genetic"):
        rules.append("R03"); proposals.append(up_one(base))
    validity = age_validity(age_years)
    if validity != "validated":
        rules.append("R04")
    if regression == "yes":
        rules.append("R05"); proposals.append("priority")
    if yes("developmental_delay") and not yes("speech"):
        rules.append("R06"); proposals.append(up_one(base))
    if yes("depression"):
        rules.append("R07")
    if family_history == "other":
        rules.append("R08")
    answers_r09 = {**health, "regression": regression}
    unknown_keys = [k for k in R09_KEYS.values() if answers_r09.get(k) == "unknown"]
    if unknown_keys:
        rules.append("R09")
    n_unknown = sum(v == "unknown" for v in health.values()) + (regression == "unknown") + (family_history == "unknown")
    if n_unknown >= 3:
        rules.append("R09b")
    final = max(proposals, key=LEVELS.index)

    def pct(weights):
        total = 0
        for k, w in weights.items():
            v = binary.get(k) if k.startswith("A") else int(health.get(k) == "yes")
            total += w * (v or 0)
        return total

    comm, soc = pct(COMM_WEIGHTS), pct(SOCIAL_WEIGHTS)
    if comm < 20 and soc < 20:
        profile = "none"
    elif abs(comm - soc) < 10:
        profile = "mixed"
    else:
        profile = "communication" if comm > soc else "social"

    return {
        "probability": round(prob, 3),
        "age_validity": validity,
        "base_level": base,
        "final_level": final,
        "triggered_rules": rules,
        "profile": {"name": profile, "communication_pct": comm, "social_pct": soc},
    }
