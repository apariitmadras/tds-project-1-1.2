from flask import Flask, request, jsonify
from flask_cors import CORS
from rag.qa_engine import get_answer
import json

app = Flask(__name__)
CORS(app)

# Load once at startup
with open("data/knowledge_base.json") as f:
    KB = json.load(f)

@app.route('/api/', methods=['POST'])
def api():
    data = request.get_json()
    question = data.get("question")
    if not question:
        return jsonify({"error": "No question provided"}), 400
    
    result = get_answer(question, KB)
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
