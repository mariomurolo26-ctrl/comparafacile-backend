import os
import httpx
from fastapi import FastAPI
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
# Qui su Render (backend) puoi mettere la chiave ANON o SERVICE_ROLE nelle Environment Variables
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "INSERISCI_LA_TUA_CHIAVE_SUPABASE")

class DatiUtente(BaseModel):
    tipo_servizio: str
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

@app.get("/")
def home():
    return {"status": "Backend AI Energia attivo"}

@app.post("/confronta")
async def confronta_offerte(dati: DatiUtente):
    # 1. Prova a leggere le offerte reali aggiornate da Supabase
    try:
        async with httpx.AsyncClient() as client:
            res = await client.get(
                f"{SUPABASE_URL}/rest/v1/offerte?tipo_servizio=eq.{dati.tipo_servizio}&attiva=eq.true&select=fornitore,offerta,prezzo",
                headers={
                    "apikey": SUPABASE_KEY,
                    "Authorization": f"Bearer {SUPABASE_KEY}"
                },
                timeout=5.0
            )
            if res.status_code == 200:
                offerte_db = res.json()
                if len(offerte_db) > 0:
                    return {"risultati": offerte_db}
    except Exception as e:
        print("Fallback alle offerte statiche:", e)

    # 2. Fallback se non hai ancora creato la tabella 'offerte' su Supabase
    if dati.tipo_servizio == 'telefonia':
        offerte = [
            {"fornitore": "WindTre", "offerta": "Fibra Wind", "prezzo": "20.00 €/mese"},
            {"fornitore": "Fastweb", "offerta": "Fastweb Fibra", "prezzo": "23.95 €/mese"}
        ]
    else:
        offerte = [
            {"fornitore": "A2A", "offerta": "Click Luce", "prezzo": "0.1200 €/kWh"},
            {"fornitore": "Enel Energia", "offerta": "Fix Tutto", "prezzo": "0.1350 €/kWh"},
            {"fornitore": "Eni Plenitude", "offerta": "Trend Casa", "prezzo": "0.1450 €/kWh"},
            {"fornitore": "Estra", "offerta": "Estra Energia", "prezzo": "0.1500 €/kWh"},
            {"fornitore": "Edison", "offerta": "Energia Mia Gas", "prezzo": "0.4500 €/Smc"}
        ]
    return {"risultati": offerte}
