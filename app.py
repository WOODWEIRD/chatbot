from flask import Flask, request, jsonify
from flask_cors import CORS
from ChatbotAI import ChatbotAI
from applicationinsights import TelemetryClient
import time

app = Flask(__name__)
CORS(app)
chatbot = ChatbotAI()

telemetry_client = TelemetryClient('3be60c3e-3cae-4c94-81ed-a420e0696f16;IngestionEndpoint=https://eastus-8.in.applicationinsights.azure.com/;LiveEndpoint=https://eastus.livediagnostics.monitor.azure.com/;ApplicationId=761e0322-d49c-4f48-85d5-265ce89b7cbe')


@app.route("/chat", methods=["POST"])
def chat():
    try:
        telemetry_client.track_event('Chat Request Received')
        start_time = time.time()

        user_input = request.json["message"]
        user_lang = request.json["lang"]

        response = chatbot.multilingual_chatbot_response(user_input, user_lang)
        response_time = time.time() - start_time
        telemetry_client.track_metric('Response Time', response_time)

        telemetry_client.track_event('Chat Processed', {
            'user_input': user_input,
            'user_lang': user_lang,
            'response': response
        })

        telemetry_client.flush()

        return jsonify({"response": response})
    
    except Exception as e:

        telemetry_client.track_exception()
        telemetry_client.track_event('Error Occurred', {'error_message': str(e)})
        telemetry_client.flush()

        return jsonify({"error": "An error occurred while processing your request"}), 500

if __name__ == "__main__":
    app.run(debug=True)
