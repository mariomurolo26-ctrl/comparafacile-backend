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

# CONTROLLA CHE QUESTO URL SIA IDENTICO A QUELLO IN SUPABASE -> PROJECT SETTINGS -> API -> PROJECT URL
SUPABASE_URL = "https://bqyyhpmxavtuvxlnowdp.supabase.co"
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJxeXlocG14YXZ0dXZ4bG5vd2RwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTUwOTU3NTgsImV4cCI6MjExMDY3MTc1OH0.pkBektrwI8yZE0f1SvW6RHMePqNGYLqkq5XAj_h1Qps")

class DatiUtente(BaseModel):
    tipo_servizio: str
    tipo_fornitura: str = "luce"
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
    privacy_accettata: bool = False
    consenso_marketing: bool = False

@app.get("/")
def home():
    return {"status": "Backend AI Energia attivo"}

@app.post("/confronta")
async def confronta_offerte(dati: DatiUtente):
    # 1. TELEFONIA: resta fissa come richiesto
    if dati.tipo_servizio == "telefonia":
        return {
            "risultati": [
                {"fornitore": "WindTre", "offerta": "Fibra Tutto Incluso", "prezzo": "20.00 €/mese"},
                {"fornitore": "Fastweb", "offerta": "Fibra Tutto Incluso", "prezzo": "23.95 €/mese"}
            ]
        }

    # 2. ENERGIA: legge SOLO da Supabase (ilike ignora maiuscole/minuscole su luce, gas, dual)
    filtro = f"tipo_servizio=ilike.energia&tipo_fornitura=ilike.{dati.tipo_fornitura}&attiva=eq.true"
    
    try:
        async with httpx.AsyncClient() as client:
            res = await client.get(
                f"{SUPABASE_URL}/rest/v1/offerte?{filtro}&select=fornitore,offerta,prezzo",
                headers={
                    "apikey": SUPABASE_KEY,
                    "Authorization": f"Bearer {SUPABASE_KEY}"
                },
                timeout=10.0
            )
            if res.status_code == 200:
                offerte_db = res.json()
                return {"risultati": offerte_db}
            else:
                raise HTTPException(status_code=400, detail=f"Errore Supabase: {res.text}")
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Errore connessione Supabase: {str(e)}")

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
