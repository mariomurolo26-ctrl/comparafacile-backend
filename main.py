from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests # <-- Usiamo questa libreria standard invece di supabase

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Le tue chiavi
SUPABASE_URL = "https://bqyyhpmxatvuxvlnwdwp.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJxeXlocG14YXZ0dXZ4bG5vd2RwIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc5NTA5NTc1OCwiZXhwIjoyMTEwNjcxNzU4fQ.Jgdn4QNHBJEwCD-A1jInJtOG5D-8OxRJRzbjKPI7o6E"

class DatiUtente(BaseModel):
    tipo_fornitura: str
    nome: str
    cognome: str
    email: str
    telefono: str
    codice_fiscale: str
    residenza: str
    luogo_fornitura: str
    pod: str = ""
    pdr: str = ""

class DatiScelta(BaseModel):
    dati_utente: DatiUtente
    offerta_scelta: str

@app.post("/confronta")
async def confronta_offerte(dati: DatiUtente):
    if dati.tipo_fornitura == 'fibra':
        offerte = [
            {"fornitore": "Fastweb", "offerta": "NeXXt Casa", "prezzo1": "26.95 €/mese", "prezzo2": "-"},
            {"fornitore": "Iliad", "offerta": "Fibra Smart", "prezzo1": "15.99 €/mese", "prezzo2": "-"},
        ]
    else:
        offerte = [
            {"fornitore": "Enel Energia", "offerta": "Fix Tutto", "prezzo1": "0.12 €/kWh", "prezzo2": "0.45 €/Smc"},
            {"fornitore": "Eni Plenitude", "offerta": "Trend Casa", "prezzo1": "0.14 €/kWh", "prezzo2": "0.50 €/Smc"},
            {"fornitore": "A2A", "offerta": "Click", "prezzo1": "0.15 €/kWh", "prezzo2": "0.48 €/Smc"},
        ]
    return {"risultati": offerte}

@app.post("/scegli")
async def scegli_offerta(dati: DatiScelta):
    u = dati.dati_utente
    
    # Prepariamo i dati
    payload = {
        "nome": u.nome, "cognome": u.cognome, "email": u.email,
        "telefono": u.telefono, "codice_fiscale": u.codice_fiscale,
        "residenza": u.residenza, "luogo_fornitura": u.luogo_fornitura,
        "pod": u.pod, "pdr": u.pdr, "tipo_fornitura": u.tipo_fornitura,
        "offerta_scelta": dati.offerta_scelta
    }

    # Chiamata diretta alle API REST di Supabase
    url = f"{SUPABASE_URL}/rest/v1/lead_scelte"
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal"
    }

    try:
        # Facciamo la richiesta HTTP
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code in [201, 204]:
            print(f"\n⭐ LEAD SALVATO SU SUPABASE! {u.nome} ha scelto: {dati.offerta_scelta}")
            return {"status": "success"}
        else:
            print(f"\n❌ ERRORE SUPABASE: Codice {response.status_code}")
            print(f"Dettagli: {response.text}")
            return {"status": "error", "details": response.text}
            
    except Exception as e:
        print(f"\n❌ ERRORE DI RETE: {e}")
        return {"status": "error", "details": str(e)}
