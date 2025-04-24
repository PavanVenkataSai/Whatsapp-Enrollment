from helper.twilio_api import send_message

from helper.openai_api import text_complition
from helper.main import get_weather_info
from helper.trial import chat_endpoint


from flask import Flask, request
from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)


@app.route('/')
def home():
    return 'All is well...'


@app.route('/twilio/receiveMessage', methods=['POST'])
def receiveMessage():
    try:
        # Extract incomng parameters from Twilio
        message = request.form['Body']
        sender_id = request.form['From']

        # Get response from Openai
        result = get_weather_info(message)
        print(result)
        if result['status'] == 1:
            send_message(sender_id, result['response'])
    except:
        print('hii')
        pass
    return 'OK', 200
