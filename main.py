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

class DatiUtente(BaseModel):
    tipo_pratica: str
    tipo_cliente: str
    tipo_fornitura: str
    nome: str
    cognome: str
    email: str
    telefono: str
    codice_fiscale: str = ""
    ragione_sociale: str = ""
    partita_iva: str = ""
    residenza: str
    luogo_fornitura: str
    pod: str = ""
    pdr: str = ""

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
