from flask import Flask, render_template, request, jsonify
import os
from groq import Groq

app = Flask(__name__)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

GYM_INFO = """
You are a helpful assistant for "FitZone Gym".
Hours: Mon-Sat, 6 AM to 10 PM. Sunday: 7 AM to 12 PM.
Memberships: Monthly ₹1,500, Quarterly ₹4,000, Annual ₹14,000.
Facilities: Free weights, cardio machines, group classes (Zumba, Yoga, HIIT), personal training.
Personal training: ₹500 per session, book in advance.
Location: Station Road, Latur.
Contact: 9876501234
Only answer questions about FitZone Gym. If asked something unrelated, politely redirect to gym topics.
"""

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {"role": "system", "content": GYM_INFO},
            {"role": "user", "content": user_message}
        ]
    )

    bot_reply = response.choices[0].message.content
    return jsonify({"reply": bot_reply})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port, debug=False)
    