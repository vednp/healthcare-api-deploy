from flask import Flask, jsonify, request
from hugchat import hugchat
from hugchat.login import Login
from flask_cors import CORS
from dotenv import load_dotenv
load_dotenv()
import os
PASS = os.getenv("PASS")

app = Flask(__name__)
CORS(app)

@app.route('/prompt', methods=['GET', 'POST'])
def process_prompt():
    try:
        if request.method == 'GET':
            return jsonify({'message': 'Use a POST request to send a prompt'}), 400

        # Get the prompt from the POST request data
        data = request.get_json()
        prompt = data.get('prompt')

        if not prompt:
            return jsonify({'error': 'Prompt not provided'}), 400

        # Log in to huggingface and grant authorization to huggingchat
        sign = Login(email="pahuneved@gmail.com", passwd=PASS)
        cookies = sign.login()

        # Save cookies to the local directory
        cookie_path_dir = "./cookies_snapshot"
        sign.saveCookiesToDir(cookie_path_dir)

        # Create a ChatBot
        chatbot = hugchat.ChatBot(cookies=cookies.get_dict())

        # Query the chatbot with the received prompt
        query_result = chatbot.query(f'Give detailed information on the of {prompt} and its symptomps, cure and prevention ')

        response_data = {
            'result': 'success',
            'text': str(query_result)
        }

        return jsonify(response_data)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
