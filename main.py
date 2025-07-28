from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse, Gather
from src.rss_parser import RSSParser
from src.openai_client import OpenAIClient

app = Flask(__name__)

def get_news():
    try:
        parser = RSSParser("https://news.smol.ai/rss.xml")
        parser.parse_feed()
        title = parser.get_feed_title()
        latest_news = parser.get_latest_entries(1)

        ai = OpenAIClient()
        summary = ai.summarize_text(latest_news, max_length=50)

        print(summary)

        return title, summary
    
    except Exception as e:
        print(f"Error fetching news: {e}")
        return "AI News", "Unable to fetch news at this time."

@app.route("/", methods=['GET', 'POST'])
def news_update():
    title, summary = get_news()
    
    twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say>Good morning! Here is the latest news from {title}. {summary}</Say>    
    <Gather input="speech dtmf" action="/process_speech" method="POST">
        <Say>Would you like a morning call again tomorrow? You can say yes or no. Or press 1 for yes, press 2 for no.</Say>
    </Gather>
    <Say>We didn't receive any input. Goodbye!</Say>
</Response>"""

    return twiml

@app.route("/process_speech", methods=['POST'])
def process_speech():
     # Get the speech result from the request
    command = request.form.get('SpeechResult')
    digits = request.form.get('Digits')

    print("command", command)

    # Determine the response message
    if digits:
        if digits == "1":
            message = "Great! You pressed 1. You'll receive another morning call tomorrow."
        elif digits == "2":
            message = "You pressed 2. No problem, you won't receive a call tomorrow."
        else:
            message = f"You pressed {digits}. I didn't understand that option."
    elif command:
        speech_lower = command.lower()
        if any(word in speech_lower for word in ["yes", "yeah", "sure", "okay", "yep"]):
            message = "Great! I heard you say yes. You'll receive another morning call tomorrow."
        elif any(word in speech_lower for word in ["no", "nope", "stop", "cancel", "don't"]):
            message = "I heard you say no. You won't receive a call tomorrow."
        else:
            message = f"You said: {command}. I'll assume that's a no for tomorrow's call."
    else:
        message = "I didn't receive any input. You won't receive a call tomorrow by default."

    twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say>{message}</Say>
    <Say>Thank you for calling. Have a great day!</Say>
</Response>"""

    return twiml



@app.route("/x", methods=['GET', 'POST'])
def x_news_update():
    title, summary = get_news()
    
    # Start our TwiML response
    resp = VoiceResponse()
    resp.say(f"Good morning! Here is the latest news from {title}. {summary}")

    # Gather speech input
    gather = Gather(input='speech dtmf', action='/process_speech', method='POST')
    gather.say("Would you like a morning call again tomorrow? You can say yes or no. Or press 1 for yes, press 2 for no.")
    
    resp.append(gather)

    resp.say('We didn\'t receive any input. Goodbye!')

    return str(resp)


@app.route("/xprocess_speech", methods=['POST'])
def x_process_speech():
    # Start our TwiML response
    resp = VoiceResponse()

    # Get the speech result from the request
    command = request.form.get('SpeechResult')
    digits = request.form.get('Digits')

    print("command", command)

    # Digit pressed
    if digits:
        if digits == "1":
            resp.say("Great! You pressed 1. You'll receive another morning call tomorrow.")

        elif digits == "2":
            resp.say("You pressed 2. No problem, you won't receive a call tomorrow.")

        else:
            resp.say(f"You pressed {digits}. I didn't understand that option.")
    
    # speech received
    elif command and command != 'No command recognized':
        speech_lower = command.lower()
        
        if any(word in speech_lower for word in ["yes", "yeah", "sure", "okay", "yep"]):
            resp.say("Great! I heard you say yes. You'll receive another morning call tomorrow.")
        elif any(word in speech_lower for word in ["no", "nope", "stop", "cancel", "don't"]):
            resp.say("I heard you say no. You won't receive a call tomorrow.")
        else:
            resp.say(f"You said: {command}. I'll assume that's a no for tomorrow's call.")
    
    # No input received
    else:
        resp.say("I didn't receive any input. You won't receive a call tomorrow by default.")

    resp.say("Thank you for calling. Have a great day!")
    
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True, port=3000)
