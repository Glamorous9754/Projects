import tkinter as tk
from langchain_huggingface import HuggingFaceEndpoint
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Setting up the Hugging Face model endpoint with your API key
repo_id = "mistralai/Mistral-7B-Instruct-v0.3"
api_key = os.getenv("HUGGINGFACE_API_KEY")  # Ensure that your .env file has HUGGINGFACE_API_KEY
llm = HuggingFaceEndpoint(repo_id=repo_id, max_length=128, temperature=0.7, token=api_key)

# Initialize conversation buffer to retain context
conversation_buffer = []

# Define prompt guidelines for concise, goal-focused responses
PROMPT_GUIDELINES = """
Please keep your responses compact and relevant. Respond only based on the following topics:
- Trip planning based on RV specifications.
- Suggested routes for specific terrains (e.g., hills, beaches).
- Finding nearby campgrounds, RV parks, or fuel stations.
- Locating RV technicians and repair services.
- Informing users about route constraints (e.g., low bridges, diesel availability).
"""

# Function to handle calling the language model
def llm_invoke(prompt):
    try:
        # Generate the response from the Hugging Face model
        return llm(prompt)
    except Exception as e:
        return f"Error generating response: {str(e)}"

# Function to handle sending messages
def on_send():
    user_input = input_box.get("1.0", tk.END).strip()  # Get user input
    input_box.delete("1.0", tk.END)  # Clear the input box after sending

    if user_input.lower() in ["exit", "quit", "bye"]:
        output_area.config(state="normal")
        output_area.insert(tk.END, "\nAsk Emily: Safe travels! If you need further assistance, I’m here!\n")
        output_area.config(state="disabled")
        root.quit()
        return

    # Add user input to conversation buffer and display it
    conversation_buffer.append(f"You: {user_input}")
    output_area.config(state="normal")
    output_area.insert(tk.END, f"\nYou: {user_input}\n")
    output_area.config(state="disabled")

    # Prepare prompt with buffer memory
    conversation_history = "\n".join(conversation_buffer[-6:])  # Limit memory to last 6 interactions
    prompt = f"{PROMPT_GUIDELINES}\n\nConversation history:\n{conversation_history}\n\nUser input: {user_input}"

    # Send prompt to the LLM and get the response
    response = llm_invoke(prompt)

    # Display the LLM response and add to conversation buffer
    conversation_buffer.append(f"Ask Emily: {response}")
    output_area.config(state="normal")
    output_area.insert(tk.END, f"Ask Emily: {response}\n")
    output_area.config(state="disabled")

# Set up the GUI interface
root = tk.Tk()
root.title("Ask Emily - AI Trip Planner")

# Set up display area for conversation history
output_area = tk.Text(root, wrap="word", width=80, height=20)
output_area.insert(tk.END,
                   "Ask Emily: Hello! I'm Ask Emily, your AI-powered Trip Planner, Travel Advisor, GPS, and RV Technician Finder.\n")
output_area.insert(tk.END,
                   "Ask Emily: I can help plan your journey, find RV-safe routes, and locate nearby campgrounds or technicians.\n")
output_area.insert(tk.END, "Ask Emily: Let me know how I can assist you with your trip!\n")
conversation_buffer.append(
    "Ask Emily: Hello! I'm Ask Emily, your AI-powered Trip Planner, Travel Advisor, GPS, and RV Technician Finder.")
output_area.config(state="disabled")  # Disable output area for editing
output_area.pack(padx=10, pady=10)

# Set up text input for user messages
input_box = tk.Text(root, wrap="word", height=3, width=60)
input_box.pack(padx=10, pady=(0, 10))

# Set up send button
send_button = tk.Button(root, text="Send", command=on_send)
send_button.pack(pady=(0, 10))

# Run the application
root.mainloop()
