from flask import Flask, render_template, request
import os
import base64
from openai import OpenAI

# Initialize Flask app
app = Flask(__name__)

# Initialize OpenAI client using environment variable
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

@app.route("/", methods=["GET"])
def index():
    # Render page with empty values to avoid Jinja errors
    return render_template("index.html", result=None, suggestions=None)

@app.route("/solve", methods=["POST"])
def solve():
    image_file = request.files.get("image")
    
    if not image_file:
        return render_template("index.html", result="No image uploaded!", suggestions=None)
    
    # Convert image to base64
    image_bytes = base64.b64encode(image_file.read()).decode()

    try:
        # Call OpenAI Vision + GPT to solve math problem
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

    except Exception as e:
        answer = f"Error solving the problem: {str(e)}"

    return render_template("index.html", result=answer, suggestions="Try similar questions: 2+2, 3+5")

if __name__ == "__main__":
    # Use PORT environment variable on Render
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)                    ]
                }
            ]
        )

        answer = response.choices[0].message.content

    except Exception as e:
        answer = f"Error solving the problem: {str(e)}"

    return render_template("index.html", result=answer, suggestions="Try similar questions: 2+2, 3+5")

if __name__ == "__main__":
    # Use PORT environment variable on Render
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
