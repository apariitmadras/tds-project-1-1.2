from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import openai

app = Flask(__name__)
CORS(app)

openai.api_key = "YOUR_OPENAI_KEY"  # Replace this securely

with open("context.json", "r") as f:
    data = json.load(f)
    CONTEXT = data["context"]

@app.route('/')
def home():
    return "API is live. Use /api/ to send requests."

@app.route('/api/', methods=['POST'])
def api():
    try:
        question = request.json.get("question")
        if not question:
            return jsonify({"error": "No question provided."}), 400

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Answer based on TDS IITM course content."},
                {"role": "user", "content": f"Context:\n{CONTEXT}\n\nQuestion: {question}"}
            ]
        )

        answer = response.choices[0].message["content"]
        return jsonify({"answer": answer, "links": ["https://tds.s-anand.net", "https://discourse.onlinedegree.iitm.ac.in/c/courses/tds-kb/34"]})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
