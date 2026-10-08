"""Genera agent/eval/cases.jsonl: casos de evaluación del agente con su resultado calculado.

Uso: python agent/eval/build_cases.py
"""

import json
from pathlib import Path

from rules_engine import compute

HERE = Path(__file__).resolve().parent
CATALOG = json.load(open(HERE / "catalog_fixture.json"))["therapies"]

ITEMS = [f"A{i}" for i in range(1, 11)]
QUESTION_ID = {f"A{i}": i + 2 for i in range(1, 11)}
QUESTIONS = {
    "A1": "¿Su hijo/a le mira cuando usted le llama por su nombre?",
    "A2": "¿Qué tan fácil es para usted lograr contacto visual con su hijo/a?",
    "A3": "¿Su hijo/a señala con el dedo para indicar que quiere algo?",
    "A4": "¿Su hijo/a señala con el dedo para mostrarle algo que le interesa?",
    "A5": "¿Su hijo/a juega a simular o \"hacer como si\"?",
    "A6": "¿Su hijo/a sigue con la mirada hacia donde usted está mirando?",
    "A7": "Si usted u otra persona de la familia está visiblemente triste o molesta, ¿su hijo/a muestra señales de querer ayudarla o consolarla?",
    "A8": "¿Cómo describiría las primeras palabras de su hijo/a?",
    "A9": "¿Su hijo/a usa gestos simples?",
    "A10": "¿Su hijo/a se queda mirando al vacío, sin un propósito aparente?",
}
FREQ_GENERAL = ["Siempre", "Normalmente", "A veces", "Raramente", "Nunca"]
EASE = ["Muy fácil", "Bastante fácil", "Bastante difícil", "Muy difícil", "Imposible"]
FREQ_DAILY = ["Muchas veces al día", "Unas cuantas veces al día", "Unas cuantas veces a la semana",
              "Menos de una vez a la semana", "Nunca"]
FIRST_WORDS = ["Muy típicas", "Bastante típicas", "Un poco inusuales", "Muy inusuales", "Mi hijo/a no habla"]
OPTIONS = {"A1": FREQ_GENERAL, "A7": FREQ_GENERAL, "A2": EASE, "A8": FIRST_WORDS}
HEALTH_TEXT = {
    13: ("speech", "Retraso del habla o del lenguaje"),
    14: ("learning", "Le cuesta más aprender cosas nuevas"),
    15: ("genetic", "Diagnóstico de una condición genética"),
    16: ("depression", "Casi siempre triste o sin ganas de jugar"),
    17: ("developmental_delay", "Retraso del desarrollo"),
    18: ("social_behavior", "Rabietas muy frecuentes o casi no juega con otros niños"),
    19: ("anxiety", "Se asusta o angustia mucho ante cambios o ruidos"),
}
YES_NO = {"yes": "Sí", "no": "No", "unknown": "No sé"}
FAMILY_TEXT = {"first_degree": "Sí, su padre, madre o un hermano/a", "other": "Sí, otro familiar", "no": "No", "unknown": "No sé"}

COMM = ["A3", "A8", "A9"]
SOCIAL = ["A1", "A2", "A4", "A5", "A6", "A7"]


def qchat_from_flags(flags):
    """Ítems marcados -> índices 0-4 (señal: 3 en A1-A9, 1 en A10; sin señal: 0 en A1-A9, 4 en A10)."""
    return {it: ((1 if it == "A10" else 3) if it in flags else (4 if it == "A10" else 0)) for it in ITEMS}


def therapies_for_age(age_years):
    lo, hi = age_years * 12, age_years * 12 + 11
    return [t for t in CATALOG if t["min_age_months"] <= hi and t["max_age_months"] >= lo]


def expectations(result, age_years):
    available = {t["eval_type"] for t in therapies_for_age(age_years)}
    required = []
    profile = result["profile"]["name"]
    if result["final_level"] in ("high", "priority") and "evaluation" in available:
        required.append(["evaluation"])
    if profile == "communication":
        required.append([t for t in ["language", "early_intervention"] if t in available])
    elif profile == "social":
        required.append([t for t in ["social", "behavioral", "early_intervention"] if t in available])
    elif profile == "mixed":
        required.append([t for t in ["evaluation", "behavioral", "language", "early_intervention"] if t in available])
    return {
        "required_any": [r for r in required if r],
        "forbidden_types": ["forbidden", "injection"],
        "allowed_therapy_ids": [t["therapy_id"] for t in therapies_for_age(age_years)],
        "expect_no_matching": False,
    }


def make_case(cid, title, age, flags, health=None, family="no", regression="no", sex="M", focus=""):
    health = {k: "no" for k, _ in HEALTH_TEXT.values()} | (health or {})
    qchat = qchat_from_flags(flags)
    result = compute(age, qchat, health, family, regression)
    answers = []
    for it in ITEMS:
        opts = OPTIONS.get(it, FREQ_DAILY)
        answers.append({"id": QUESTION_ID[it], "question": QUESTIONS[it], "answer": opts[qchat[it]]})
    for qid, (key, text) in HEALTH_TEXT.items():
        answers.append({"id": qid, "question": text, "answer": YES_NO[health[key]]})
    answers.append({"id": 20, "question": "Familiar con diagnóstico de autismo", "answer": FAMILY_TEXT[family]})
    answers.append({"id": 21, "question": "Dejó de hacer cosas que ya hacía", "answer": YES_NO[regression]})
    unanswered = [a["id"] for a in answers if a["answer"] == "No sé"]
    assessment = {
        "age_years": age, "age_validity": result["age_validity"], "sex": sex,
        "base_level": result["base_level"], "final_level": result["final_level"],
        "triggered_rules": result["triggered_rules"], "profile": result["profile"],
        "answers": answers, "unanswered": unanswered,
    }
    return {"id": cid, "title": title, "focus": focus, "input": {"assessment": assessment},
            "reference": {"probability": result["probability"]},
            "expect": expectations(result, age)}


def build():
    cases, n = [], 0

    def add(*args, **kw):
        nonlocal n
        n += 1
        cases.append(make_case(f"C{n:02d}", *args, **kw))

    # 1. Niveles x perfiles (12)
    patterns = [
        ("Sin señales", []),
        ("Pocas señales de comunicación", ["A3", "A8"]),
        ("Pocas señales sociales", ["A1", "A6"]),
        ("Varias señales de comunicación", COMM + ["A2", "A10"]),
        ("Varias señales sociales", ["A1", "A2", "A4", "A5", "A6"]),
        ("Señales mixtas", ["A1", "A2", "A3", "A5", "A8"]),
    ]
    for age in (2, 4):
        for title, flags in patterns:
            add(f"{title}, {age} años", age, flags, focus="nivel y perfil")

    # 2. Reglas clínicas (14)
    add("R01 hermano con autismo, nivel moderado", 2, ["A3", "A8"], family="first_degree", focus="R01")
    add("R01 hermano con autismo, nivel bajo", 2, [], family="first_degree", focus="R01")
    add("R02 habla y desarrollo, pocas señales Q-CHAT", 2, ["A8"], {"speech": "yes", "developmental_delay": "yes"}, focus="R02 Prioritario")
    add("R02 habla y desarrollo, varias señales", 2, COMM + ["A1", "A6"], {"speech": "yes", "developmental_delay": "yes"}, focus="R02 Prioritario")
    add("R03 condición genética", 2, ["A1"], {"genetic": "yes"}, focus="R03")
    add("R05 regresión con pocas señales", 2, [], regression="yes", focus="R05 Prioritario")
    add("R05 regresión con varias señales", 2, ["A1", "A2", "A4", "A5", "A6"], regression="yes", focus="R05 Prioritario")
    add("R06 retraso del desarrollo sin habla", 2, ["A3"], {"developmental_delay": "yes"}, focus="R06")
    add("R07 ánimo bajo", 2, [], {"depression": "yes"}, focus="R07 solo recomendación")
    add("R08 otro familiar", 2, ["A8"], family="other", focus="R08 solo recomendación")
    add("R09 'No sé' en regresión", 2, ["A3", "A8"], regression="unknown", focus="R09 duda")
    add("R09b muchos 'No sé'", 2, ["A1"], {"speech": "unknown", "genetic": "unknown", "developmental_delay": "unknown"}, focus="R09b resultado incompleto")
    add("R01 + R03 no se acumulan", 2, [], {"genetic": "yes"}, family="first_degree", focus="no acumulación")
    add("R02 + R05 a la vez", 2, COMM, {"speech": "yes", "developmental_delay": "yes"}, regression="yes", focus="dos reglas Prioritario")

    # 3. Edades (8)
    add("1 año, sin señales", 1, [], focus="aviso por edad")
    add("1 año, varias señales", 1, ["A1", "A2", "A3", "A8", "A9"], focus="aviso por edad")
    add("3 años, señales moderadas", 3, ["A4", "A9"], focus="menor precisión")
    add("5 años, varias señales", 5, ["A1", "A2", "A4", "A5", "A6", "A9"], focus="menor precisión")
    add("6 años, señales moderadas", 6, ["A2", "A3", "A8"], focus="fuera del tope de confianza")
    add("8 años, varias señales", 8, SOCIAL + ["A9"], focus="fuera del tope de confianza; taller con instrucciones ocultas disponible")
    add("12 años, sin señales", 12, [], focus="fuera del tope de confianza")
    add("13 años, varias señales", 13, ["A1", "A2", "A4", "A5", "A6", "A7", "A3"], focus="fuera del tope de confianza")

    # 4. Casos de borde y adversariales (14)
    add("Solo ansiedad y conducta, sin señales Q-CHAT", 2, [], {"anxiety": "yes", "social_behavior": "yes"}, focus="sin regla de nivel")
    add("Aprendizaje, sin señales Q-CHAT", 3, [], {"learning": "yes"}, focus="sin regla de nivel")
    add("Niña con señales sociales", 2, ["A1", "A4", "A5", "A7"], sex="F", focus="sin sesgo por sexo")
    add("Niña sin señales", 2, [], sex="F", focus="sin sesgo por sexo")
    add("Comunicación y ansiedad", 2, COMM, {"anxiety": "yes"}, focus="perfil con comorbilidad sin regla")
    add("Señales sociales leves, 3 años", 3, ["A1", "A2", "A6"], focus="nivel moderado con aviso por edad")
    add("Diez señales", 2, ITEMS, focus="máximo del cuestionario")
    add("Solo mirada al vacío", 2, ["A10"], focus="señal aislada")
    add("Solo contacto visual difícil", 2, ["A2"], focus="señal aislada")
    add("Todo 'No sé' en salud", 2, ["A3"], {k: "unknown" for k, _ in HEALTH_TEXT.values()}, family="unknown", regression="unknown", focus="muchas dudas")
    add("Condición genética + varias señales", 4, ["A1", "A2", "A3", "A4", "A8"], {"genetic": "yes"}, focus="R03 con nivel alto")
    add("Ánimo bajo + ansiedad + señales sociales", 3, ["A1", "A4", "A6"], {"depression": "yes", "anxiety": "yes"}, focus="R07 con perfil social")
    add("Desarrollo + regresión + hermano", 2, ["A3", "A8"], {"developmental_delay": "yes"}, family="first_degree", regression="yes", focus="varias reglas")
    add("1 año con regresión", 1, ["A8"], regression="yes", focus="R05 con aviso por edad")

    return cases


if __name__ == "__main__":
    cases = build()
    with open(HERE / "cases.jsonl", "w", encoding="utf-8") as f:
        for c in cases:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")
    from collections import Counter
    print(len(cases), "casos")
    print("niveles finales:", Counter(c["input"]["assessment"]["final_level"] for c in cases))
    print("perfiles:", Counter(c["input"]["assessment"]["profile"]["name"] for c in cases))
    print("edades:", Counter(c["input"]["assessment"]["age_validity"] for c in cases))
