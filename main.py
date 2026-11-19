from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from supabase import create_client
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inserisci qui l'URL e la chiave del tuo progetto Supabase
SUPABASE_URL = "https://bqyyhpmxavtuvxlnowdp.supabase.co"
SUPABASE_KEY = "sb_secret_JIWFEvD6Y3-zSnbcmE8apw_bDmjs7hn"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

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
    # ... (la logica delle offerte rimane identica, non toccarla) ...
    # [Copia qui la parte di codice delle offerte che avevi già]
    return {"risultati": offerte}

@app.post("/scegli")
async def scegli_offerta(dati: DatiScelta):
    u = dati.dati_utente
    # Inseriamo i dati nella tabella 'lead_scelte' di Supabase
    data = {
        "nome": u.nome, "cognome": u.cognome, "email": u.email,
        "telefono": u.telefono, "codice_fiscale": u.codice_fiscale,
        "residenza": u.residenza, "luogo_fornitura": u.luogo_fornitura,
        "pod": u.pod, "pdr": u.pdr, "tipo_fornitura": u.tipo_fornitura,
        "offerta_scelta": dati.offerta_scelta
    }
    supabase.table('lead_scelte').insert(data).execute()
    print(f"\n⭐ LEAD SALVATO SU SUPABASE! {u.nome} ha scelto: {dati.offerta_scelta}")
    return {"status": "success"}
