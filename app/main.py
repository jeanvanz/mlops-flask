from flask import Flask, jsonify, request
import joblib
import json
import os

app = Flask(__name__)

MODEL_PATH = os.path.join("models", "model.joblib")
METRICS_PATH = os.path.join("models", "metrics.json")

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError("O arquivo 'model.joblib' não foi encontrado na pasta 'models/'.")
model = joblib.load(MODEL_PATH)

if os.path.exists(METRICS_PATH):
    with open(METRICS_PATH, "r") as f:
        metrics = json.load(f)
else:
    metrics = {}

@app.route('/', methods=['GET'])
def hello_world():
    return jsonify({"message": "Hello World, Flask API is running!"})

@app.route('/health-check', methods=['GET'])
def health():
    return jsonify({"status": "OK"})

@app.route('/user/<name>', methods=['GET'])
def get_user(name):
    return jsonify({"message": f"Olá, {name}! Seja bem-vindo à API Flask."})

@app.route('/echo', methods=['POST'])
def echo_data():
    data = request.get_json()
    return jsonify({
        "received_data": data,
        "message": "Dados recebidos com sucesso!"
    })

@app.route('/metrics', methods=['GET'])
def get_metrics():
    """Retorna as métricas do modelo treinado"""
    return jsonify(metrics)

@app.route('/predict', methods=['GET'])
def predict():
    try:
        size_param = request.args.get("size")
        bedrooms_param = request.args.get("bedrooms")

        try:
            size = float(size_param)
        except ValueError:
            return jsonify({"erro": "O parâmetro 'size' deve ser um número."}), 400

        try:
            bedrooms = int(float(bedrooms_param))
        except ValueError:
            return jsonify({"erro": "O parâmetro 'bedrooms' deve ser um inteiro."}), 400

        entrada = [[float(size), int(bedrooms)]]
        preco_previsto = model.predict(entrada)[0]

        return jsonify({
            "size": size,
            "bedrooms": bedrooms,
            "preco_previsto": round(float(preco_previsto), 2),
            "r2": metrics.get("r2")
        })

    except Exception as e:
        return jsonify({"erro": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
