from helper.twilio_api import send_message
from helper.openai_api import text_complition
from helper.main import get_weather_info
from helper.trial import chat_endpoint

from flask import Flask, request
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

# Dictionary to store user states
user_states = {}

text = "Welcome!!\nChoose a Service:\n1) ChatGPT\n2) Value Health Solutions\n3) Weather Guide\n\n -->Type 'exit' to come out of current Service!! "

@app.route('/')
def home():
    return 'All is well...'

@app.route('/twilio/receiveMessage', methods=['POST'])
def receiveMessage():
    try:
        # Extract incoming parameters from Twilio
        message_body = request.form['Body']
        sender_id = request.form['From']

        if sender_id not in user_states:
            # If the user is new, send the home message
            user_states[sender_id] = 'home'
            send_message(sender_id, text)

        else:
            user_state = user_states[sender_id]

            if message_body.lower() == 'exit':
                # If the user types "exit", return to the home message
                user_states[sender_id] = 'home'
                send_message(sender_id, text)
                return 'OK', 200

            if user_state == 'home':
                # Check user input to choose the next state
                if message_body.lower() == '1':
                    user_states[sender_id] = 'text_completion'
                    send_message(sender_id, 'Go ahead and ask questions!!')

                elif message_body.lower() == '2':
                    user_states[sender_id] = 'chat_endpoint'
                    send_message(sender_id, 'Go ahead and ask questions!!')

                elif message_body.lower() == '3':
                    user_states[sender_id] = 'weather_info'
                    send_message(sender_id, 'Go ahead and ask questions!!')

                else:
                    # Handle unrecognized input
                    send_message(sender_id, "Unrecognized input.\n"+text)
                    return 'OK', 200

            # Perform the corresponding action based on the current state
            if user_state == 'text_completion':
                result = text_complition(message_body)
                if result['status'] == 1:
                    send_message(sender_id, result['response'])

            elif user_state == 'chat_endpoint':
                result = chat_endpoint(message_body)
                if result['status'] == 1:
                    send_message(sender_id, result['response'])

            elif user_state == 'weather_info':
                result = get_weather_info(message_body)
                if result['status'] == 1:
                    send_message(sender_id, result['response'])

    except Exception as e:
        print(e)

    return 'OK', 200

if __name__ == '__main__':
    app.run(debug=True)
