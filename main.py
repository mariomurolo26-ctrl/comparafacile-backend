from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random

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

@app.post("/confronta")
async def confronta_offerte(dati: DatiUtente):
    if dati.tipo_servizio == 'telefonia':
        # Telefonia: Wind e Fastweb fissi come richiesto
        offerte = [
            {"fornitore": "WindTre", "offerta": "Wind Smart Unlimited", "prezzo": "9.99 €/mese", "tipo": "Mobile"},
            {"fornitore": "Fastweb", "offerta": "Fastweb Mobile", "prezzo": "7.95 €/mese", "tipo": "Mobile"}
        ]
    else:
        # Energia: Prezzi dinamici (variano a ogni chiamata per simulare il mercato)
        base_luce = round(random.uniform(0.10, 0.16), 4)
        base_gas = round(random.uniform(0.40, 0.55), 4)
        
        offerte = [
            {"fornitore": "Enel Energia", "offerta": "Fix Tutto", "prezzo": f"{base_luce + 0.01} €/kWh", "tipo": "Luce"},
            {"fornitore": "Eni Plenitude", "offerta": "Trend Casa", "prezzo": f"{base_luce + 0.02} €/kWh", "tipo": "Luce"},
            {"fornitore": "A2A", "offerta": "Click", "prezzo": f"{base_luce} €/kWh", "tipo": "Luce"},
            {"fornitore": "Edison", "offerta": "Energia Mia", "prezzo": f"{base_gas} €/Smc", "tipo": "Gas"}
        ]
        # Ordiniamo per prezzo crescente per mostrare le migliori
        offerte = sorted(offerte, key=lambda x: float(x["prezzo"].split()[0]))
    
    return {"risultati": offerte}
