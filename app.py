import os
from dotenv import load_dotenv
from flask import (
    Flask,
    render_template,
    request,
    Response,
    stream_with_context,
    jsonify,
)
import openai

load_dotenv()

# Strip whitespace/newlines to avoid invalid auth header
api_key = (os.getenv("OPENAI_API_KEY") or "").strip()
openai.api_key = api_key

# Pass explicit key to client to avoid relying on env formatting
client = openai.OpenAI(api_key=api_key)

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    content = request.json["message"]
    generation = request.json.get("generation", "Millennials")
    
    # Store in Flask session or global for the stream endpoint
    global current_message, current_generation
    current_message = content
    current_generation = generation
    
    return jsonify(success=True)


@app.route("/stream", methods=["GET"])
def stream():
    def generate():
        global current_message, current_generation
        
        # Create system prompt based on selected generation
        system_prompt = f"Translate the following text into {current_generation} slang. Use the language, phrases, and expressions commonly associated with {current_generation}."
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": current_message}
        ]

        with client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            stream=True,
            temperature=0,
        ) as stream:
            for chunk in stream:
                if chunk.choices[0].delta and chunk.choices[0].delta.content:
                    yield f"data: {chunk.choices[0].delta.content}\n\n"
                if chunk.choices[0].finish_reason == "stop":
                    break

    return Response(stream_with_context(generate()), mimetype="text/event-stream")



