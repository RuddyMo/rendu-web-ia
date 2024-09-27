from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sklearn.linear_model import LinearRegression, LogisticRegression
import uvicorn
import numpy as np
import pandas as pd
from loguru import logger

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)


note_model = LinearRegression()
year_model = LinearRegression()
garage_model = LogisticRegression()

is_note_model_trained = False
is_year_model_trained = False
is_garage_model_trained = False

class NotePredictionData(BaseModel):
    surface: float
    prix: float
    ville: str

class YearPredictionData(BaseModel):
    ville: str

class GaragePredictionData(BaseModel):
    prix: float
    ville: str

# Entraînement du modèle de prédiction de la note
@app.post("/training-note")
async def train_note_model():
    global is_note_model_trained
    df = pd.read_csv('/Users/ruddy/Documents/ecole/M2/webinteIA/rendu-web-ia/appartements.csv')
    df['ville_encoded'] = df['ville'].astype('category').cat.codes
    X = df[['surface', 'prix', 'ville_encoded']]
    y = df['note']
    note_model.fit(X, y)
    is_note_model_trained = True
    return {"message": "Modèle de prédiction de la note entraîné."}

# Prédiction de la note
@app.post("/predict-note")
async def predict_note(data: NotePredictionData):
    if not is_note_model_trained:
        raise HTTPException(status_code=400, detail="Modèle non entraîné.")
    
    ville_mapping = {'Paris': 0, 'Lyon': 1, 'Marseille': 2}[data.ville]
    
    ville_clean = data.ville.strip().lower()
    
    if ville_clean not in ville_mapping:
        raise HTTPException(status_code=400, detail=f"Ville '{data.ville}' non supportée.")
    
    ville_encoded = ville_mapping[ville_clean]
    X_new = np.array([[data.surface, data.prix, ville_encoded]])
    
    predicted_note = note_model.predict(X_new)[0]
    return {"predicted_note": predicted_note}


# Entraînement du modèle de prédiction de l'année
@app.post("/training-year")
async def train_year_model():
    global is_year_model_trained
    df = pd.read_csv('/Users/ruddy/Documents/ecole/M2/webinteIA/rendu-web-ia/appartements.csv')
    df['ville_encoded'] = df['ville'].astype('category').cat.codes
    X = df[['ville_encoded']]
    y = df['annee']
    year_model.fit(X, y)
    is_year_model_trained = True
    return {"message": "Modèle de prédiction de l'année entraîné."}

# Prédiction de l'année
@app.post("/predict-year")
async def predict_year(data: YearPredictionData):
    if not is_year_model_trained:
        raise HTTPException(status_code=400, detail="Modèle non entraîné.")
    
    ville_clean = data.ville.strip().lower()
    ville_mapping = {'Paris': 0, 'Lyon': 1, 'Marseille': 2}[ville_clean]

    X_new = np.array([[ville_mapping]])
    predicted_year = year_model.predict(X_new)[0]
    return {"predicted_year": predicted_year}

# Entraînement du modèle de prédiction du garage
@app.post("/training-garage")
async def train_garage_model():
    global is_garage_model_trained
    df = pd.read_csv('/Users/ruddy/Documents/ecole/M2/webinteIA/rendu-web-ia/appartements.csv')
    df['ville_encoded'] = df['ville'].astype('category').cat.codes
    X = df[['prix', 'ville_encoded']]
    y = df['garage']
    garage_model.fit(X, y)
    is_garage_model_trained = True
    return {"message": "Modèle de prédiction du garage entraîné."}

# Prédiction du garage
@app.post("/predict-garage")
async def predict_garage(data: GaragePredictionData):
    if not is_garage_model_trained:
        raise HTTPException(status_code=400, detail="Modèle non entraîné.")
    ville_encoded = {'Paris': 0, 'Lyon': 1, 'Marseille': 2}[data.ville]
    X_new = np.array([[data.prix, ville_encoded]])
    has_garage = garage_model.predict(X_new)[0]
    return {"has_garage": bool(has_garage)}

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=5001)
