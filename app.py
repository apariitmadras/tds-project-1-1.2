from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import openai
import os

app = Flask(__name__)
CORS(app)

# Load context data (from both sources)
with open("context.json", "r") as f:
    context_data = json.load(f)

# Combine both sources into one context string
context_text = "\n\n".join([item["text"] for item in context_data])

# Set your OpenAI API key (you can also use environment variable)
openai.api_key = os.getenv("OPENAI_API_KEY", "sk-...")  # Replace with your real key or set in Render

@app.route('/')
def home():
    return "TDS Virtual TA API is live."

@app.route('/api/', methods=['POST'])
def api():
    try:
        data = request.get_json()
        question = data.get("question", "")

        if not question:
            return jsonify({"error": "No question provided"}), 400

        # OpenAI ChatCompletion
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful virtual TA for the TDS course at IIT Madras. Answer questions using the course content and discussions."},
                {"role": "user", "content": f"Context:\n{context_text}\n\nQuestion:\n{question}"}
            ]
        )

        answer = response.choices[0].message["content"].strip()

        return jsonify({
            "answer": answer,
            "links": [
                {"text": "Course content", "url": "https://tds.s-anand.net/#/2025-01/"},
                {"text": "Discourse", "url": "https://discourse.onlinedegree.iitm.ac.in/c/courses/tds-kb/34"}
            ]
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
