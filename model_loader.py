import joblib
import os
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PALABRAS_PROHIBIDAS = {
    "imbecil","imbécil","idiota","pendejo","puta","puto",
    "verga","mierda","hdp","hijo de puta","chingada",
    "estúpido","tarado","cabron","basura","escoria"
}

class ToxicityModel:
    def __init__(self):
        self.model = joblib.load(
            os.path.join(BASE_DIR, "modelo_toxicidad_es.pkl")
        )
        self.vectorizer = joblib.load(
            os.path.join(BASE_DIR, "vectorizador_tfidf_es.pkl")
        )
        self.umbral = 0.85  

    def limpiar(self, texto: str) -> str:
        texto = str(texto)
        texto = re.sub(r"http\S+|@\w+", "", texto)
        texto = re.sub(r"[^a-zA-ZáéíóúñÁÉÍÓÚ0-9\s]", " ", texto)
        texto = texto.lower()
        texto = re.sub(r"\s+", " ", texto)
        return texto.strip()

    def contiene_palabras_prohibidas(self, texto: str) -> bool:
        return any(p in texto for p in PALABRAS_PROHIBIDAS)

    def predict(self, texto: str):
        texto_limpio = self.limpiar(texto)

     
        if self.contiene_palabras_prohibidas(texto_limpio):
            return 1, 0.99

     
        X = self.vectorizer.transform([texto_limpio])
        prob = float(self.model.predict_proba(X)[0][1])

        toxicidad = 1 if prob >= self.umbral else 0
        return toxicidad, prob
