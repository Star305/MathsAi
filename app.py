from flask import Flask, render_template, request
import base64
from openai import OpenAI

client = OpenAI(api_key="YOUR_API_KEY")

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/solve", methods=["POST"])
def solve():
    image = request.files["image"]
    image_bytes = base64.b64encode(image.read()).decode()

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Solve this math problem step by step and suggest 2 similar questions."},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_bytes}"}}
                ]
            }
        ]
    )

    answer = response.choices[0].message.content

    return render_template("index.html", result=answer, suggestions="See above")

if __name__ == "__main__":
    app.run(debug=True)
