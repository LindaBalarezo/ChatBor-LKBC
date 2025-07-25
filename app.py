import os
from flask import Flask, render_template, request, jsonify, session
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = "Linda2003"  

# Variables de entorno
endpoint = os.getenv("ENDPOINT_URL")
deployment = os.getenv("DEPLOYMENT_NAME")
subscription_key = os.getenv("AZURE_OPENAI_API_KEY")

# Cliente Azure OpenAI
client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=subscription_key,
    api_version="2024-12-01-preview"
)

@app.route("/")
def home():
    session["chat_history"] = [
        {
            "role": "system",
            "content": "Eres un asistente amigable que responde preguntas de forma clara, útil y en español. Sé conversacional, breve si es posible, y evita respuestas vacías."
        }
    ]
    return render_template("chat.html")

@app.route("/send", methods=["POST"])
def send():
    try:
        user_message = request.json.get("message", "").strip()
        if not user_message:
            return jsonify({"reply": "Por favor, escribe algo."})

        chat_history = session.get("chat_history", [
            {
                "role": "system",
                "content": "Eres un asistente amigable que responde preguntas de forma clara, útil y en español."
            }
        ])

        chat_history.append({"role": "user", "content": user_message})
        chat_history = chat_history[-10:]

        response = client.chat.completions.create(
            model=deployment,
            messages=chat_history,
            max_completion_tokens=512  
        )

        reply = response.choices[0].message.content.strip() if response.choices else "Lo siento, no entendí tu mensaje. ¿Puedes reformularlo?"

        chat_history.append({"role": "assistant", "content": reply})
        session["chat_history"] = chat_history

        return jsonify({"reply": reply})

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"reply": f"Error del servidor: {str(e)}"}), 500
    
    # Ruta para reiniciar conversación
@app.route("/new_conversation", methods=["POST"])
def new_conversation():
    session["chat_history"] = [
        {
            "role": "system",
            "content": (
              "Eres un asistente amigable que responde preguntas de forma clara, útil y en español."
            )
        }
    ]
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(debug=True)
