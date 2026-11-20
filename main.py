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
    # Questa è una lista di fornitori REALI con prezzi simulati per il momento
    # In futuro, qui andrai a leggere i prezzi veri da un database o da un'API
    
    if dati.tipo_fornitura == 'fibra':
        offerte = [
            {"fornitore": "Fastweb", "offerta": "NeXXt Casa", "prezzo1": "26.95 €/mese", "prezzo2": "-"},
            {"fornitore": "Iliad", "offerta": "Fibra Smart", "prezzo1": "15.99 €/mese", "prezzo2": "-"},
            {"fornitore": "TIM", "offerta": "Fibra Premium", "prezzo1": "29.90 €/mese", "prezzo2": "-"},
        ]
    else:
        offerte = [
            {"fornitore": "Enel Energia", "offerta": "Fix Tutto", "prezzo1": "0.11 €/kWh", "prezzo2": "0.42 €/Smc"},
            {"fornitore": "Eni Plenitude", "offerta": "Trend Casa", "prezzo1": "0.12 €/kWh", "prezzo2": "0.45 €/Smc"},
            {"fornitore": "A2A", "offerta": "Click", "prezzo1": "0.13 €/kWh", "prezzo2": "0.46 €/Smc"},
            {"fornitore": "Edison", "offerta": "Energia Mia", "prezzo1": "0.14 €/kWh", "prezzo2": "0.48 €/Smc"},
            {"fornitore": "Sorgenia", "offerta": "Next Energy", "prezzo1": "0.15 €/kWh", "prezzo2": "0.49 €/Smc"},
            {"fornitore": "Iren", "offerta": "Smart Casa", "prezzo1": "0.16 €/kWh", "prezzo2": "0.50 €/Smc"},
        ]
    
    # Simuliamo che il server ordini le offerte per prezzo più basso
    offerte_ordinate = sorted(offerte, key=lambda x: float(x["prezzo1"].split()[0]))
    
    return {"risultati": offerte_ordinate}
