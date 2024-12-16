from flask import Flask, request, jsonify
from flask_cors import CORS
from ChatbotAI import ChatbotAI
from applicationinsights import TelemetryClient
import time
from datetime import datetime, timezone

app = Flask(__name__)
CORS(app)
chatbot = ChatbotAI()

telemetry_client = TelemetryClient('3be60c3e-3cae-4c94-81ed-a420e0696f16')


@app.route("/chat", methods=["POST"])
def chat():
    try:
        telemetry_client.track_event('Chat Request Received-2')
        start_time = datetime.now(timezone.utc).isoformat()
        request_start_time = time.time()


        user_input = request.json["message"]
        user_lang = request.json["lang"]

        response = chatbot.multilingual_chatbot_response(user_input, user_lang)

         # Calculate request duration
        duration = (time.time() - request_start_time) * 1000  # Convert to milliseconds

        # Log the request event
        telemetry_client.track_request(
            name="POST /chat",
            url=request.url,
            success=True,
            start_time=start_time,
            duration=duration,
            response_code="200",
            properties={
                "user_input": user_input,
                "user_lang": user_lang,
                "response": response
            }
        )

        response_time = time.time() - request_start_time
        telemetry_client.track_metric('Response Time', response_time)

        telemetry_client.track_event('Chat Processed', {
            'user_input': user_input,
            'user_lang': user_lang,
            'response': response
        })
        return jsonify({"response": response})
    
    except Exception as e:
        duration = (time.time() - request_start_time) * 1000  # Convert to milliseconds

        # Log the failed request
        telemetry_client.track_request(
            name="POST /chat",
            url=request.url,
            success=False,
            start_time=start_time,
            duration=duration,
            response_code="500",
            properties={"error": str(e)}
        )

        telemetry_client.track_exception()
        telemetry_client.track_event('Failed requests', {'error_message': str(e)})

        return jsonify({"error": "An error occurred while processing your request"}), 500
    finally:
        telemetry_client.flush();

if __name__ == "__main__":
    app.run(debug=True)
