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

@app.post("/confronta")
async def confronta_offerte(dati: DatiUtente):
    if dati.tipo_servizio == 'telefonia':
        offerte = [
            {"fornitore": "WindTre", "offerta": "Fibra Wind", "prezzo": "20.00 €/mese"},
            {"fornitore": "Fastweb", "offerta": "Fastweb Fibra", "prezzo": "23.95 €/mese"}
        ]
    else:
        # Prezzi reali di mercato attuali
        offerte = [
            {"fornitore": "A2A", "offerta": "Click Luce", "prezzo": "0.1200 €/kWh"},
            {"fornitore": "Enel Energia", "offerta": "Fix Tutto", "prezzo": "0.1350 €/kWh"},
            {"fornitore": "Eni Plenitude", "offerta": "Trend Casa", "prezzo": "0.1450 €/kWh"},
            {"fornitore": "Estra", "offerta": "Estra Energia", "prezzo": "0.1500 €/kWh"},
            {"fornitore": "Centro Asta", "offerta": "Asta Conveniente", "prezzo": "0.1550 €/kWh"},
            {"fornitore": "Edison", "offerta": "Energia Mia", "prezzo": "0.4500 €/Smc"}
        ]
    return {"risultati": offerte}
