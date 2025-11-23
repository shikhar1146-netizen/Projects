import openai

# ---------------------------
# CONFIG
# ---------------------------
openai.api_key = "YOUR_API_KEY"

SYSTEM_MESSAGE = """
You are a Legal Information Assistant.
You DO NOT provide legal advice.
You ONLY provide:
- general legal information
- explanations of legal terms
- guidance on where to find official resources
- suggestions to consult a licensed attorney

Never tell the user what they should do.
Never interpret laws in a way that applies to their personal situation.
Always include a disclaimer.
"""

DISCLAIMER = (
    "\n\nDISCLAIMER: I am not a lawyer. This is general legal information, "
    "not legal advice. For advice about your specific situation, consult a licensed attorney."
)


# ---------------------------
# RESPONSE FUNCTION
# ---------------------------

def get_legal_info(query):
    """Get a safe general-legal-information response from OpenAI."""
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_MESSAGE},
            {"role": "user", "content": query}
        ],
        max_tokens=300
    )

    return response.choices[0].message["content"] + DISCLAIMER


# ---------------------------
# MAIN CHAT LOOP
# ---------------------------

def run_chat():
    print("🔹 Legal Information Assistant")
    print("🔹 Type 'quit' to exit\n")

    while True:
        user_input = input("You: ")

        if user_input.lower() in ["quit", "exit"]:
            print("Goodbye!")
            break

        answer = get_legal_info(user_input)
        print("\nAI:", answer, "\n")


# ---------------------------
# START
# ---------------------------
if __name__ == "__main__":
    run_chat()


