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
    nome_file_bolletta: str = ""

@app.post("/confronta")
async def confronta_offerte(dati: DatiUtente):
    if dati.tipo_servizio == 'telefonia':
        offerte = [
            {"fornitore": "WindTre", "offerta": "Wind Smart Unlimited", "prezzo": "9.99 €/mese"},
            {"fornitore": "Fastweb", "offerta": "Fastweb Mobile", "prezzo": "7.95 €/mese"}
        ]
    else:
        # Generiamo prezzi casuali ma li arrotondiamo a 4 decimali
        base_luce = round(random.uniform(0.09, 0.15), 4)
        base_gas = round(random.uniform(0.38, 0.50), 4)
        
        offerte = [
            {"fornitore": "A2A", "offerta": "Click", "prezzo": f"{round(base_luce, 4)} €/kWh"},
            {"fornitore": "Enel Energia", "offerta": "Fix Tutto", "prezzo": f"{round(base_luce + 0.01, 4)} €/kWh"},
            {"fornitore": "Eni Plenitude", "offerta": "Trend Casa", "prezzo": f"{round(base_luce + 0.015, 4)} €/kWh"},
            {"fornitore": "Estra", "offerta": "Estra Energia", "prezzo": f"{round(base_luce + 0.02, 4)} €/kWh"},
            {"fornitore": "Centro Asta", "offerta": "Asta Conveniente", "prezzo": f"{round(base_luce + 0.025, 4)} €/kWh"},
            {"fornitore": "Edison", "offerta": "Energia Mia", "prezzo": f"{round(base_gas, 4)} €/Smc"}
        ]
        # Ordiniamo per prezzo crescente (dal più conveniente al più caro)
        offerte = sorted(offerte, key=lambda x: float(x["prezzo"].split()[0]))
    
    return {"risultati": offerte}
