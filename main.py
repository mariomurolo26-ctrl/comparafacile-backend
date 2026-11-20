import os
import httpx
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

SUPABASE_URL = "https://bqyyhpmxatvuxvlnwdwp.supabase.co"
# Incolla qui la tua chiave SUPABASE (anon public o service_role) oppure impostala su Render in Environment Variables
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJxeXlocG14YXZ0dXZ4bG5vd2RwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTUwOTU3NTgsImV4cCI6MjExMDY3MTc1OH0.pkBektrwI8yZE0f1SvW6RHMePqNGYLqkq5XAj_h1Qps")

class DatiUtente(BaseModel):
    tipo_servizio: str
    tipo_fornitura: str = "luce"  # luce, gas, dual
    tipo_cliente: str
    tipo_pratica: str
    nome: str
    cognome: str
    ragione_sociale: str = ""
    partita_iva: str = ""
    email: str
    telefono: str
    codice_fiscale: str = ""
    residenza: str
    pod: str = ""
    pdr: str = ""

class DatiSalvataggio(DatiUtente):
    nome_file_bolletta: str = "Nessun file caricato"
    offerta_scelta: str

@app.get("/")
def home():
    return {"status": "Backend AI Energia attivo"}

@app.post("/confronta")
async def confronta_offerte(dati: DatiUtente):
    # Costruisce il filtro per Supabase
    if dati.tipo_servizio == "telefonia":
        filtro = "tipo_servizio=eq.telefonia&attiva=eq.true"
    else:
        filtro = f"tipo_servizio=eq.energia&tipo_fornitura=eq.{dati.tipo_fornitura}&attiva=eq.true"

    # 1. Legge le offerte che hai inserito tu su Supabase
    try:
        async with httpx.AsyncClient() as client:
            res = await client.get(
                f"{SUPABASE_URL}/rest/v1/offerte?{filtro}&select=fornitore,offerta,prezzo",
                headers={
                    "apikey": SUPABASE_KEY,
                    "Authorization": f"Bearer {SUPABASE_KEY}"
                },
                timeout=8.0
            )
            if res.status_code == 200:
                offerte_db = res.json()
                if len(offerte_db) > 0:
                    return {"risultati": offerte_db}
    except Exception as e:
        print("Errore lettura Supabase:", e)

    # 2. Offerte di backup divise per Luce, Gas, Dual e Telefonia (se la tabella su Supabase è ancora vuota)
    if dati.tipo_servizio == 'telefonia':
        offerte = [
            {"fornitore": "WindTre", "offerta": "Fibra Wind", "prezzo": "20.00 €/mese"},
            {"fornitore": "Fastweb", "offerta": "Fastweb Fibra", "prezzo": "23.95 €/mese"}
        ]
    elif dati.tipo_fornitura == 'gas':
        offerte = [
            {"fornitore": "Edison", "offerta": "Energia Mia Gas", "prezzo": "0.4500 €/Smc"},
            {"fornitore": "Eni Plenitude", "offerta": "Trend Casa Gas", "prezzo": "0.4700 €/Smc"},
            {"fornitore": "A2A", "offerta": "Click Gas", "prezzo": "0.4850 €/Smc"}
        ]
    elif dati.tipo_fornitura == 'dual':
        offerte = [
            {"fornitore": "Enel Energia", "offerta": "Fix Tutto Dual", "prezzo": "0.135 €/kWh + 0.46 €/Smc"},
            {"fornitore": "Eni Plenitude", "offerta": "Trend Casa Luce & Gas", "prezzo": "0.145 €/kWh + 0.47 €/Smc"},
            {"fornitore": "A2A", "offerta": "Click Luce + Gas", "prezzo": "0.125 €/kWh + 0.48 €/Smc"}
        ]
    else: # Solo Luce
        offerte = [
            {"fornitore": "A2A", "offerta": "Click Luce", "prezzo": "0.1200 €/kWh"},
            {"fornitore": "Enel Energia", "offerta": "Fix Tutto Luce", "prezzo": "0.1350 €/kWh"},
            {"fornitore": "Eni Plenitude", "offerta": "Trend Casa Luce", "prezzo": "0.1450 €/kWh"}
        ]

    return {"risultati": offerte}

@app.post("/salva")
async def salva_richiesta(dati: DatiSalvataggio):
    payload = dati.dict()
    try:
        async with httpx.AsyncClient() as client:
            res = await client.post(
                f"{SUPABASE_URL}/rest/v1/lead_ai_energia",
                headers={
                    "apikey": SUPABASE_KEY,
                    "Authorization": f"Bearer {SUPABASE_KEY}",
                    "Content-Type": "application/json",
                    "Prefer": "return=minimal"
                },
                json=payload,
                timeout=10.0
            )
            if res.status_code in [200, 201]:
                return {"status": "ok"}
            else:
                raise HTTPException(status_code=400, detail=res.text)
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
