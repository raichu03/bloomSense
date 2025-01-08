import ollama

SYSTEM_PROMPT = """You are a reading assistant that answers questions strictly based on the provided text snippet. Respond concisely and only using the given context. If the answer isn't clear from the context, simply say you don't know"""

conversation_history = []

def update_context(context):
    """Updates the system context"""
    for item in conversation_history:
        if item['role'] == 'system':
            item['content'] = context
    


def conversationAI(prompt: str, context: str):
    """Function to have conversation with the bot"""
    ### Adding System Prompt ###
    if not conversation_history:
        conversation_history.append({
            "role": "system",
            "content": SYSTEM_PROMPT + " \n " + context,
        })
    else:
        update_context(context)
    
    ### Adding User Prompt ###
    conversation_history.append({
        "role": "user",
        "content": prompt,
    })

    ### Prompting the Model ###
    response = ollama.chat(
        model="llama3.2",
        messages=conversation_history
    )
    
    ### Adding Assistant Responst ###
    conversation_history.append({
        "role": "assistant",
        "content": response["message"]["content"],
    })
    
    return response["message"]["content"]
    