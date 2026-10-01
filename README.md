# Neuroa — Modelo de tamizaje de TEA (Q-CHAT-10)

Modelo de Machine Learning que estima el riesgo de Trastorno del Espectro Autista (TEA) a partir de las 10 preguntas del Q-CHAT-10 que responden los padres, **validado con diagnósticos clínicos reales**.

## Contenido

| Ruta | Qué es |
|---|---|
| `notebooks/desarrollo_modelo_ml_v2.ipynb` | Notebook completo y ejecutado: auditoría del dataset anterior, EDA, preprocesamiento, 30 modelos (10 algoritmos × 3 variantes), selección, calibración, umbral, test clínico, SHAP, sesgos y exportación |
| `models/v2/modelo_tamizaje_tea.pkl` | Modelo final (scikit-learn 1.6.1): Regresión Logística sobre A1–A10, calibrada |
| `models/v2/metadata.json` | Variables, umbral, métricas, pesos de los perfiles y versiones |
| `data/raw/` | Datasets públicos usados (ver abajo) |
| `docs/consideraciones_app_tamizaje.md` | Consideraciones para construir la aplicación de tamizaje |
| `docs/arquitectura_conecta.md` | Arquitectura técnica de Conecta y su integración con el SGT y el panel interno |

## Datos

| Archivo | Origen | n | Edad | Etiqueta | Uso |
|---|---|---|---|---|---|
| `nz_toddler_autism_2018.csv` | Thabtah (2018), Kaggle "Autism Screening for Toddlers" | 1054 | 12–36 meses | Regla Q-CHAT-10 (suma ≥ 4) | Entrenamiento |
| `saudi_toddler_autism.csv` | Kaggle "ASD Screening Data for Toddlers in Saudi Arabia" | 506 | 12–36 meses | Regla Q-CHAT-10 (suma ≥ 4) | Entrenamiento |
| `polish_qchat_mendeley.sav` | Niedźwiecka et al. (2020), Mendeley Data | 252 | 18–24 meses | Diagnóstico clínico (ADOS-2 / ADI-R / DSM-5) | Validación (50 %) y test (50 %) |
| `dataset_anterior_kaggle.csv` | CSV de Kaggle usado en la versión 1 | 1985 | — | — | Solo auditoría (sección 1.1) |

## Resultado (test clínico, 126 niños con diagnóstico real)

| Método | AUC | Sensibilidad | Especificidad |
|---|---|---|---|
| **Modelo v2** (umbral de `metadata.json`) | **0.960** | **0.925** | **0.847** |
| Regla oficial Q-CHAT-10 (suma ≥ 4) | 0.964 | 0.791 | 0.932 |

El modelo prioriza la detección (sensibilidad) a cambio de algo más de falsos positivos. Rinde igual que el Q-CHAT-10 con corte en 3. Sus ventajas son el riesgo graduado y calibrado, la explicación por pregunta y un pipeline listo para reentrenarse con diagnósticos clínicos locales. Limitaciones y detalles: sección 7 del notebook.

## Uso

```python
import json, joblib, pandas as pd

modelo = joblib.load("models/v2/modelo_tamizaje_tea.pkl")
meta = json.load(open("models/v2/metadata.json"))

# A1–A9: 1 si la opción elegida es la 3, 4 o 5; A10: 1 si es la 1, 2 o 3
respuestas = pd.DataFrame([{"A1": 1, "A2": 1, "A3": 0, "A4": 1, "A5": 1, "A6": 1, "A7": 1, "A8": 0, "A9": 0, "A10": 1}])
prob = modelo.predict_proba(respuestas[meta["features"]])[:, 1][0]
riesgo = prob >= meta["umbral"]
```

La probabilidad está calibrada en una muestra con 54 % de TEA, así que sobreestima el riesgo poblacional: en la aplicación conviene mostrar niveles de riesgo, no el porcentaje exacto.

## Reproducir el notebook

```bash
pip install -r requirements.txt
cd notebooks
jupyter nbconvert --to notebook --execute --inplace desarrollo_modelo_ml_v2.ipynb
```
