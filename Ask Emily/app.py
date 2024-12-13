from flask import Flask, render_template, request, jsonify
from langchain_huggingface import HuggingFaceEndpoint
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Setting up the Hugging Face model endpoint
repo_id = "mistralai/Mistral-7B-Instruct-v0.3"
api_key = os.getenv("HUGGINGFACE_API_KEY")
llm = HuggingFaceEndpoint(repo_id=repo_id, max_length=128, temperature=0.7, token=api_key)

app = Flask(__name__)

# Define prompt guidelines for concise, goal-focused responses
PROMPT_GUIDELINES = """
Please keep your responses compact and relevant. Respond only based on the following topics:
- Trip planning based on RV specifications.
- Suggested routes for specific terrains (e.g., hills, beaches).
- Finding nearby campgrounds, RV parks, or fuel stations.
- Locating RV technicians and repair services.
- Informing users about route constraints (e.g., low bridges, diesel availability).
"""

# Initialize conversation buffer
conversation_buffer = []


# Route to render the main HTML page
@app.route('/')
def index():
    return render_template('index.html')


# API endpoint to handle user queries
@app.route('/query', methods=['POST'])
def query():
    user_input = request.json.get('input')

    # Update conversation buffer and prompt
    conversation_buffer.append(f"You: {user_input}")
    conversation_history = "\n".join(conversation_buffer[-6:])
    prompt = f"{PROMPT_GUIDELINES}\n\nConversation history:\n{conversation_history}\n\nUser input: {user_input}"

    # Get response from LLM
    try:
        response = llm(prompt)
    except Exception as e:
        response = f"Error: {str(e)}"

    # Update conversation buffer with the response
    conversation_buffer.append(f"Ask Emily: {response}")

    return jsonify({"response": response})


if __name__ == '__main__':
    app.run(debug=True)
