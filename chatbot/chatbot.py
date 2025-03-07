from flask import Flask, render_template, request, session
from datetime import datetime
import google.generativeai as genai
from textblob import TextBlob

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Add this for template time function
@app.context_processor
def utility_processor():
    def now():
        return datetime.now()
    return dict(now=now)

# Configure Gemini API correctly
try:
    genai.configure(api_key='AIzaSyDQtd7b_sXfg0L495CQ8gdz5fNirGL7uiU')
    model = genai.GenerativeModel('gemini-pro')
except Exception as e:
    print(f"Error initializing Gemini: {e}")

def analyze_sentiment(text):
    blob = TextBlob(text)
    return 'Positive' if blob.sentiment.polarity > 0 else 'Negative' if blob.sentiment.polarity < 0 else 'Neutral'

def get_bot_response(user_input):
    try:
        conversation = model.start_chat(history=[])
        response = conversation.send_message(
            f"""As a mental health support chatbot:
            User message: {user_input}
            User's mood: {analyze_sentiment(user_input)}
            
            Please provide a supportive, empathetic response."""
        )
        return response.text
    except Exception as e:
        print(f"Gemini API Error: {e}")
        return "I'm here to help and listen. Would you like to tell me more?"

@app.route("/", methods=["GET", "POST"])
def home():
    if 'chat_history' not in session:
        session['chat_history'] = []
    
    if request.method == "POST":
        user_input = request.form["message"]
        sentiment = analyze_sentiment(user_input)
        bot_response = get_bot_response(user_input)
        
        session['chat_history'].extend([
            {'type': 'user', 'text': user_input, 'time': datetime.now()},
            {'type': 'bot', 'text': f"{bot_response}", 'time': datetime.now()}
        ])
        session.modified = True
    
    return render_template("index.html", chat_history=session['chat_history'])

if __name__ == "__main__":
    app.run(debug=True, port=5001)  # Changed port to avoid conflict with main app
