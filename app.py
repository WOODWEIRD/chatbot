from flask import Flask, request, jsonify
from flask_cors import CORS
from ChatbotAI import ChatbotAI

app = Flask(__name__)
CORS(app)
chatbot = ChatbotAI()


@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json["message"]
    user_lang = request.json["lang"]
    return jsonify({"response": chatbot.multilingual_chatbot_response(user_input, user_lang)})

if __name__ == "__main__":
    app.run(debug=True)
