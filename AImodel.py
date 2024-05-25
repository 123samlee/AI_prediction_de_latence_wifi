from flask import Flask, request, jsonify
import joblib

app = Flask(__name__)

# Charger le modèle SVM
svm_model = joblib.load('svm_model.pkl')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    rssi = data['RSSI']
    distance = data['Distance']
    latence_predite = svm_model.predict([[rssi, distance]])
    return jsonify({'latence_predite': latence_predite[0]})

@app.route('/')  # Ajouter cette route pour l'URL racine
def index():
    return "Bienvenue sur l'API de prédiction de latence!"

if __name__ == '__main__':
    app.run(debug=True)
