# Pino AI

App interna de **Pino Productions** / **Aitana Eventos** (Villa Elisa, La Plata, Argentina).
Streamlit + Gemini, 100% gratuita para arrancar.

📄 El plan de negocio completo está en [`BUSINESS_PLAN.md`](./BUSINESS_PLAN.md). Empezá por ahí.

## ⚠️ Primero: seguridad

Este repo tenía una API key de Gemini escrita directamente en el código y ya quedó en el
historial de git. Si todavía no lo hiciste:

1. Andá a [Google AI Studio](https://aistudio.google.com/apikey) y **borrá/regenerá** esa key.
2. Generá una nueva y guardala solo como secreto (nunca en el código), como se explica abajo.

## Qué incluye la app

- **Asistente (`app.py`)**: chat general con contexto de tu negocio.
- **Generador de Contenido**: posts, captions y hashtags para Instagram.
- **Cotizador**: presupuestos automáticos con combos y descuentos, y mensaje de WhatsApp listo.
- **CRM de Clientes**: seguimiento de consultas, estados, y exportación a CSV.

## Cómo correrla en tu compu

```bash
python -m venv .venv
source .venv/bin/activate   # en Windows: .venv\Scripts\activate
pip install -r requirements.txt

cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# Editá .streamlit/secrets.toml y pegá tu API key de https://aistudio.google.com/apikey

streamlit run app.py
```

## Cómo publicarla gratis (Streamlit Community Cloud)

1. Subí este repo a GitHub (ya lo está).
2. Entrá a [share.streamlit.io](https://share.streamlit.io) con tu cuenta de GitHub.
3. "New app" → elegí este repo → archivo principal `app.py`.
4. En **Settings → Secrets**, pegá:
   ```
   GEMINI_API_KEY = "tu-key-nueva"
   ```
5. Deploy. Te da una URL pública que podés usar desde el celular.

## Estructura del proyecto

```
app.py                          # Asistente / página principal
pages/
  1_📅_Generador_Contenido.py   # Contenido para Instagram
  2_💰_Cotizador.py             # Presupuestos automáticos
  3_📋_CRM_Clientes.py          # Seguimiento de clientes
utils/
  gemini_client.py              # Configuración compartida de Gemini
  crm_db.py                     # Base de datos del CRM (SQLite local)
config/
  precios.json                  # Precios editables de servicios
data/
  crm.db                        # Se crea sola al usar el CRM (no se sube a git)
BUSINESS_PLAN.md                # Plan de negocio completo
```

## Datos importantes a personalizar

- `config/precios.json`: tiene precios de **ejemplo**. Editalos con tus valores reales.
- `utils/gemini_client.py`: tiene el contexto de marca que usa la IA en todas las páginas
  (nombres, ubicación, equipo). Actualizalo si cambia algo del negocio.
