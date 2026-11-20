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
import requests # Assicurati di averlo in cima al file, se manca

# ... (il resto del tuo codice, come la classe DatiUtente, rimane uguale)

@app.post("/confronta")
async def confronta_offerte(dati: DatiUtente):
    # 1. Prepariamo i dati per l'API esterna
    # SwitchAI ha bisogno di: commodity (LUCE o GAS), consumo annuo e zona.
    # Usiamo un consumo di esempio se non fornito, e una zona fissa (es. "NORD").
    # In futuro potresti aggiungere un campo "zona" al tuo form.
    
    if dati.tipo_fornitura == 'fibra':
        # Per la fibra lasciamo le offerte di esempio per ora
        return {"risultati": [
            {"fornitore": "Fastweb", "offerta": "NeXXt Casa", "prezzo1": "26.95 €/mese", "prezzo2": "-"},
            {"fornitore": "Iliad", "offerta": "Fibra Smart", "prezzo1": "15.99 €/mese", "prezzo2": "-"},
        ]}

    # Mappiamo il tipo di fornitura
    commodity = "LUCE" if dati.tipo_fornitura in ['luce', 'duale'] else "GAS"
    
    # Consumo di esempio (in futuro potresti prenderlo da un campo del form)
    consumo_annuo = 3200 if commodity == "LUCE" else 1400 
    zona = "NORD" # Zona di esempio

    # 2. Chiamiamo l'API di SwitchAI per ottenere le top 3 offerte
    try:
        payload = {
            "commodity": commodity,
            "yearly_consumption_kwh": consumo_annuo,
            "zone": zona,
            "current_annual_spend": 900 # Spesa annua di esempio
        }
        
        # L'endpoint per il calcolo del risparmio e delle top 3 offerte
        risposta_api = requests.post(
            "https://www.switchai.it/api/analyze", # Endpoint corretto
            json=payload,
            timeout=20 # Timeout per non bloccare il server
        )
        risposta_api.raise_for_status() # Controlla se ci sono errori HTTP
        dati_api = risposta_api.json()

        # 3. Adattiamo la risposta dell'API al nostro formato (fornitore, offerta, prezzo1, prezzo2)
        risultati_finali = []
        for offerta in dati_api.get('best_offers', []):
            risultati_finali.append({
                "fornitore": offerta.get('supplier_name', 'N/D'),
                "offerta": offerta.get('offer_name', 'Offerta'),
                "prezzo1": f"{offerta.get('price_kwh', 0)} €/kWh",
                "prezzo2": f"{offerta.get('price_smc', 0)} €/Smc" if commodity == "GAS" else "-"
            })

        return {"risultati": risultati_finali}

    except requests.exceptions.RequestException as e:
        # Se l'API esterna fallisce, restituiamo un errore chiaro
        print(f"Errore nella chiamata all'API esterna: {e}")
        return {"risultati": [], "errore": "Impossibile recuperare le offerte aggiornate al momento."}    
