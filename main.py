from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from supabase import create_client
import os

app = FastAPI()

# Configurazione CORS corretta (Risolve l'errore di connessione del browser)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False, # IMPORTANTE: Deve essere False
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inserisci qui le tue chiavi di Supabase (controlla che siano tra le virgolette!)
SUPABASE_URL = "https://bqyyhpmxatvuxvlnwdwp.supabase.co"
SUPABASE_KEY = "sb_secret_JIWFEvD6Y3-zSnbcmE8apw_bDmjs7hn"

SUPABASE_POOLER_URL = "postgresql://postgres.bqyyhpmxatvuxvlnwdwp:Fastenergy2026@aws-1-eu-west-1.pooler.supabase.com:5432/postgres"

supabase = create_client(SUPABASE_POOLER_URL, SUPABASE_KEY)


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
    # QUI C'ERA L'ERRORE: Ora creiamo correttamente la variabile 'offerte'
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
    data = {
        "nome": u.nome, "cognome": u.cognome, "email": u.email,
        "telefono": u.telefono, "codice_fiscale": u.codice_fiscale,
        "residenza": u.residenza, "luogo_fornitura": u.luogo_fornitura,
        "pod": u.pod, "pdr": u.pdr, "tipo_fornitura": u.tipo_fornitura,
        "offerta_scelta": dati.offerta_scelta
    }
    
    try:
        supabase.table('lead_scelte').insert(data).execute()
        print(f"\n⭐ LEAD SALVATO SU SUPABASE! {u.nome} ha scelto: {dati.offerta_scelta}")
        return {"status": "success"}
    except Exception as e:
        print(f"Errore salvataggio Supabase: {e}")
        return {"status": "error"}
