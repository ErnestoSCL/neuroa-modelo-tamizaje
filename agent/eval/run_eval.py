"""Ejecuta el set de evaluación del agente.

Modos:
  python agent/eval/run_eval.py --mock
      Agente simulado (reglas fijas, como el texto de respaldo). Sirve para probar
      el circuito completo sin gastar en un modelo.
  python agent/eval/run_eval.py --deployment <nombre>
      Modelo real en Azure OpenAI. Requiere las variables de entorno
      AZURE_OPENAI_ENDPOINT y AZURE_OPENAI_API_KEY y el paquete openai >= 1.40.
  python agent/eval/run_eval.py --openai <modelo>
      Modelo real en la API de OpenAI (solo para evaluar con los casos ficticios;
      en producción se usa Azure en Brazil South). Requiere OPENAI_API_KEY.

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
PROMPT_VERSION = "prompt-2026.3"
USAGE = {}


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


def search_therapies_tool(**kw):
    """Respuesta de la herramienta tal como la ve el agente."""
    rows = search_therapies(**kw)
    return {"therapies": rows, "truncated": len(rows) >= 20}


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
def llm_agent(case, client, deployment):
    tools = [{"type": "function", "function": {"name": t["name"], "description": t["description"],
                                                "parameters": t["input_schema"]}}
             for t in json.load(open(AGENT / "tools.json"))]
    schema = json.load(open(AGENT / "output_schema.json"))
    schema = {k: v for k, v in schema.items() if k not in ("$schema", "title", "description")}
    messages = [{"role": "system", "content": system_prompt()},
                {"role": "user", "content": json.dumps(case["input"], ensure_ascii=False)}]
    returned, called = set(), False
    usage = {"input": 0, "cached": 0, "output": 0}
    for _ in range(4):
        resp = client.chat.completions.create(
            model=deployment, messages=messages, tools=tools,
            response_format={"type": "json_schema", "json_schema": {"name": "AgentOutput", "schema": schema, "strict": False}},
            max_completion_tokens=1500)
        msg = resp.choices[0].message
        if resp.usage:
            usage["input"] += resp.usage.prompt_tokens
            usage["output"] += resp.usage.completion_tokens
            det = getattr(resp.usage, "prompt_tokens_details", None)
            usage["cached"] += (getattr(det, "cached_tokens", 0) or 0) if det else 0
        if msg.tool_calls:
            messages.append(msg.model_dump(exclude_none=True))
            for call in msg.tool_calls:
                called = True
                result = search_therapies_tool(**json.loads(call.function.arguments))
                returned |= {r["therapy_id"] for r in result["therapies"]}
                messages.append({"role": "tool", "tool_call_id": call.id, "content": json.dumps(result, ensure_ascii=False)})
            continue
        USAGE.update(usage)
        return json.loads(msg.content), returned, called
    raise RuntimeError("El agente no terminó en 4 turnos")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mock", action="store_true")
    ap.add_argument("--deployment", help="nombre del despliegue en Azure OpenAI")
    ap.add_argument("--openai", help="modelo de la API de OpenAI (por ejemplo, gpt-4.1-mini)")
    ap.add_argument("--limit", type=int, help="correr solo los primeros N casos")
    args = ap.parse_args()
    client, model = None, None
    if args.openai:
        from openai import OpenAI
        client, model = OpenAI(), args.openai
    elif args.deployment:
        from openai import AzureOpenAI
        client = AzureOpenAI(azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
                             api_key=os.environ.get("AZURE_OPENAI_API_KEY"), api_version="2024-10-21")
        model = args.deployment
    elif not args.mock:
        ap.error("indique --mock, --openai <modelo> o --deployment <nombre>")
    mode = "mock" if args.mock else model
    (HERE / "results").mkdir(exist_ok=True)
    totals = {"cases": 0, "valid": 0, "case_ok": 0, "errors": {}}
    with open(HERE / "results" / f"{mode}.jsonl", "w", encoding="utf-8") as f:
        for case in load_cases()[: args.limit]:
            t0 = time.time()
            USAGE.clear()
            try:
                out, returned, called = mock_agent(case) if args.mock else llm_agent(case, client, model)
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
                                "validation": v, "case_checks": e, "usage": dict(USAGE), "output": out}, ensure_ascii=False) + "\n")
    print(json.dumps(totals, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
