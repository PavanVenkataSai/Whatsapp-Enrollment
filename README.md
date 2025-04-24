
# WhatsApp-OpenAI Connection
Hi everyone, this is repository for my personal demo project on connecting Twilio and OpenAI to provide answers to all the users questions using OpenAI GPT-3. This is written in `Python` and served with `Flask`. This bot can only handle:
* text messgaes


### What you will need
There are couple of things that you need before you get started following this repository.
* OpenAI API key, since it is open to all, you can create an account [here](https://openai.com/) and access the key.
* You need a Twilio project, you can get `Account SID` and `Auth Token` for that project, we will need this to make requests. You can get it from [here](https://console.twilio.com/).
* API requesting application like Postman, Insomnia, etc.
* NGROK for local testing.

### How to use it
To replicate the work of this repository and run it locally, you need to follow these steps:
* create a `.env` file inside the root directory, create these environmental variables:
    ```
    TWILIO_ACCOUNT_SID=YOUR ACCOUNT SID
    TWILIO_AUTH_TOKEN=YOUR AUTH TOKEN
    OPENAI_API_KEY=YOUR OPENAI API KEY
    FROM=whatsapp:+14155238886
    ```
This FROM variable in the .env file is same for the Twilio WhatsApp Sandbox.
* create a virtual environment and activate it before installing the packages
* install all the required dependencies from the `requirements.txt` file
```python
pip install -r requirements.txt
```
* run the server with either of the following commands
```python
python run.py
```
```python
gunicorn run:app
```
* start NGROK engine on the same port as the python application is running.
* provide the NGROk urlon `Twilio WhatsApp Sandbox` for all incoming request.
* test the setup using your WhatsApp


* [LinkedIn](https://www.linkedin.com/in/pavanai/)

