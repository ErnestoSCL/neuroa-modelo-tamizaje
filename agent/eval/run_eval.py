"""Ejecuta el set de evaluación del agente.

Modos:
  python agent/eval/run_eval.py --mock
      Agente simulado (reglas fijas, como el texto de respaldo). Sirve para probar
      el circuito completo sin gastar en un modelo.
  python agent/eval/run_eval.py --deployment <nombre>
      Modelo real en Azure OpenAI. Requiere las variables de entorno
      AZURE_OPENAI_ENDPOINT y AZURE_OPENAI_API_KEY (o identidad administrada)
      y el paquete openai >= 1.40.

Salida: agent/eval/results/<modo>.jsonl y un resumen en pantalla.
"""

import argparse
import json
import os
import time
from pathlib import Path

from check_output import CATALOG, check_case, validate

HERE = Path(__file__).resolve().parent
AGENT = HERE.parent
ROOT = AGENT.parent
PROMPT_VERSION = "prompt-2026.1"


def load_cases():
    return [json.loads(l) for l in open(HERE / "cases.jsonl", encoding="utf-8")]


def search_therapies(age_years, district="", modality="any", keywords=None, **_):
    """Simula la herramienta del backend sobre el catálogo de prueba."""
    lo, hi = age_years * 12, age_years * 12 + 11
    rows = [t for t in CATALOG.values() if t["min_age_months"] <= hi and t["max_age_months"] >= lo]
    if modality in ("in_person", "virtual"):
        rows = [t for t in rows if t["modality"] in (modality, "both")]
    if keywords:
        kws = [k.lower() for k in keywords]
        rows = [t for t in rows if any(k in (t["name"] + " " + t["description"]).lower() for k in kws)]
    rows.sort(key=lambda t: t["district"] != district)
    return [{k: v for k, v in t.items() if k != "eval_type"} for t in rows[:20]]


def system_prompt():
    parts = [(AGENT / "system_prompt.md").read_text(encoding="utf-8")]
    kb = ROOT / "knowledge"
    for name in json.load(open(kb / "version.json"))["files"]:
        parts.append(f"\n\n# knowledge/{name}\n\n" + (kb / name).read_text(encoding="utf-8"))
    return "".join(parts)


# ---------- agente simulado ----------
PROFILE_KEYWORDS = {
    "communication": ["lenguaje", "habla", "fonoaudiolog"],
    "social": ["social", "juego", "aba", "denver"],
    "mixed": ["evaluación", "interdisciplinaria", "estimulación"],
    "none": ["estimulación"],
}
NEVER = ["dieta", "suplemento", "desintoxicación", "quelación"]


def mock_agent(case):
    a = case["input"]["assessment"]
    rows = search_therapies(a["age_years"], a["district"])
    kws = PROFILE_KEYWORDS[a["profile"]["name"]] + (["evaluación"] if a["final_level"] in ("high", "priority") else [])
    chosen = [t for t in rows if any(k in (t["name"] + t["description"]).lower() for k in kws)
              and not any(n in (t["name"] + t["description"]).lower() for n in NEVER)
              and "IMPORTANTE PARA EL ASISTENTE" not in t["description"]]
    out = {
        "summary": "Gracias por responder. Este es un resultado orientativo basado en sus respuestas. "
                   "Le explicamos qué significa y cuáles pueden ser los siguientes pasos para acompañar el desarrollo de su hijo/a.",
        "profile_explanation": "Las señales aparecieron sobre todo en el área indicada en su resultado, según sus respuestas.",
        "next_steps": ["Converse este resultado con su pediatra en el próximo control CRED o en su establecimiento de salud.",
                       "Si lo desea, contacte a alguno de los centros afiliados que ofrecen las terapias sugeridas."],
        "suggested_therapies": [{"therapy_id": t["therapy_id"], "reason": "Puede ayudar a fortalecer las áreas donde aparecieron señales."} for t in chosen],
        "no_matching_therapies": not chosen,
    }
    return out, {t["therapy_id"] for t in rows}, True


# ---------- agente real (Azure OpenAI) ----------
def azure_agent(case, client, deployment):
    tools = [{"type": "function", "function": {"name": t["name"], "description": t["description"],
                                                "parameters": t["input_schema"]}}
             for t in json.load(open(AGENT / "tools.json"))]
    schema = json.load(open(AGENT / "output_schema.json"))
    schema = {k: v for k, v in schema.items() if k not in ("$schema", "title", "description")}
    messages = [{"role": "system", "content": system_prompt()},
                {"role": "user", "content": json.dumps(case["input"], ensure_ascii=False)}]
    returned, called = set(), False
    for _ in range(4):
        resp = client.chat.completions.create(
            model=deployment, messages=messages, tools=tools,
            response_format={"type": "json_schema", "json_schema": {"name": "AgentOutput", "schema": schema, "strict": False}},
            max_tokens=1500)
        msg = resp.choices[0].message
        if msg.tool_calls:
            messages.append(msg.model_dump(exclude_none=True))
            for call in msg.tool_calls:
                called = True
                rows = search_therapies(**json.loads(call.function.arguments))
                returned |= {r["therapy_id"] for r in rows}
                messages.append({"role": "tool", "tool_call_id": call.id, "content": json.dumps(rows, ensure_ascii=False)})
            continue
        return json.loads(msg.content), returned, called
    raise RuntimeError("El agente no terminó en 4 turnos")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mock", action="store_true")
    ap.add_argument("--deployment")
    args = ap.parse_args()
    client = None
    if not args.mock:
        from openai import AzureOpenAI
        client = AzureOpenAI(azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
                             api_key=os.environ.get("AZURE_OPENAI_API_KEY"), api_version="2024-10-21")
    mode = "mock" if args.mock else args.deployment
    (HERE / "results").mkdir(exist_ok=True)
    totals = {"cases": 0, "valid": 0, "case_ok": 0, "errors": {}}
    with open(HERE / "results" / f"{mode}.jsonl", "w", encoding="utf-8") as f:
        for case in load_cases():
            t0 = time.time()
            try:
                out, returned, called = mock_agent(case) if args.mock else azure_agent(case, client, args.deployment)
                v, e = validate(out, returned, called), check_case(out, case)
            except Exception as ex:  # noqa: BLE001
                out, v, e = None, [f"EXC {type(ex).__name__}: {ex}"], []
            totals["cases"] += 1
            totals["valid"] += not v
            totals["case_ok"] += not v and not e
            for err in v + e:
                key = err.split(" ")[0]
                totals["errors"][key] = totals["errors"].get(key, 0) + 1
            f.write(json.dumps({"id": case["id"], "prompt_version": PROMPT_VERSION, "seconds": round(time.time() - t0, 2),
                                "validation": v, "case_checks": e, "output": out}, ensure_ascii=False) + "\n")
    print(json.dumps(totals, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
